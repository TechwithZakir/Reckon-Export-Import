import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class LCAmendment(Document):
	def validate(self):
		if self.approval_date and self.approval_date < self.request_date:
			frappe.throw(_("Approval Date cannot be before Request Date."))
		duplicate = frappe.db.exists("LC Amendment", {"trade_lc": self.trade_lc, "amendment_no": self.amendment_no, "name": ["!=", self.name]})
		if duplicate:
			frappe.throw(_("Amendment Number must be unique for this LC."))

	def on_submit(self):
		if self.status != "Approved":
			frappe.throw(_("Only an Approved amendment can be submitted."))
		lc = frappe.get_doc("Trade LC", self.trade_lc)
		updates = {"status": "Amended"}
		for source, target in (("new_lc_amount", "lc_amount"), ("new_latest_shipment_date", "latest_shipment_date"), ("new_expiry_date", "expiry_date")):
			if self.get(source) is not None:
				updates[target] = self.get(source)
		if "lc_amount" in updates:
			updates["available_amount"] = flt(updates["lc_amount"]) - flt(lc.utilized_amount)
		lc.db_set(updates)
