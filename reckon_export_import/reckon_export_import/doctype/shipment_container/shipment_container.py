import re

import frappe
from frappe import _
from frappe.model.document import Document


class ShipmentContainer(Document):
	def validate(self):
		self.container_no = (self.container_no or "").replace(" ", "").upper()
		if self.container_no and not re.fullmatch(r"[A-Z]{4}[0-9]{7}", self.container_no):
			frappe.throw(_("Container Number must contain four letters followed by seven digits."))

