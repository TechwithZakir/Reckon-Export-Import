import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class LCDiscrepancy(Document):
	def validate(self):
		if self.due_date and self.due_date < self.detected_date:
			frappe.throw(_("Resolution Due Date cannot be before Detected Date."))
		if self.status == "Resolved" and not self.resolution:
			frappe.throw(_("Resolution is required before closing a discrepancy."))
		if self.status == "Waived" and not self.waived_by:
			self.waived_by, self.waiver_date = frappe.session.user, now_datetime()
