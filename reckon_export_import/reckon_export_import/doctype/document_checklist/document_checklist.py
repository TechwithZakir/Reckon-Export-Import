from frappe.model.document import Document


class DocumentChecklist(Document):
	def validate(self):
		mandatory = [row for row in self.items if row.mandatory]
		verified = [row for row in mandatory if row.status in ("Verified", "Waived")]
		self.completion_percentage = (len(verified) / len(mandatory) * 100) if mandatory else 100

