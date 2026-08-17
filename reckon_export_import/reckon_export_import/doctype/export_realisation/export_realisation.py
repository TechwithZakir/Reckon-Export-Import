from frappe.model.document import Document
from frappe.utils import flt


class ExportRealisation(Document):
	def validate(self):
		self.net_realised_amount = flt(self.amount_received) - flt(self.bank_charges)
		self.outstanding_amount = flt(self.invoice_amount) - flt(self.net_realised_amount)
		self.status = "Fully Realised" if self.outstanding_amount <= 0 else ("Partially Realised" if self.amount_received else "Pending")

