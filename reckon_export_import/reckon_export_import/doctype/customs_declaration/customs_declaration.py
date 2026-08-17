import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CustomsDeclaration(Document):
	def validate(self):
		if self.release_date and self.filing_date and self.release_date < self.filing_date:
			frappe.throw(_("Release Date cannot be before Filing Date."))
		self.total_customs_payable = sum(flt(value) for value in (
			self.customs_duty, self.vat_tax, self.regulatory_duty, self.other_tax
		))

