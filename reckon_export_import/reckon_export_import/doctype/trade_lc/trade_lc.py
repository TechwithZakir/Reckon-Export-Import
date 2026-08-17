import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class TradeLC(Document):
	def validate(self):
		if self.issue_date and self.expiry_date and self.expiry_date < self.issue_date:
			frappe.throw(_("LC Expiry Date cannot be before Issue Date."))
		if flt(self.utilized_amount) > flt(self.lc_amount) * (1 + flt(self.positive_tolerance) / 100):
			frappe.throw(_("Utilized Amount exceeds the LC amount and tolerance."))
		self.available_amount = flt(self.lc_amount) - flt(self.utilized_amount)

