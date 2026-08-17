import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class TradeDocument(Document):
	def validate(self):
		if self.issue_date and self.expiry_date and self.expiry_date < self.issue_date:
			frappe.throw(_("Expiry Date cannot be before Issue Date."))
		for row in self.items:
			row.amount = flt(row.quantity) * flt(row.rate)
		if self.document_type == "Commercial Invoice":
			self.document_amount = sum(flt(row.amount) for row in self.items)
