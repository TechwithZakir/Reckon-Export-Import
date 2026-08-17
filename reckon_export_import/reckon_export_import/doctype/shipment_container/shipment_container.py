import re

import frappe
from frappe import _
from frappe.model.document import Document


class ShipmentContainer(Document):
	def validate(self):
		self._set_and_validate_mode()
		self.container_no = (self.container_no or "").strip().upper()
		container_types = {"20GP", "40GP", "40HC", "45HC", "20RF", "40RF"}
		if self.shipment_mode == "Sea" and self.container_type in container_types:
			self.container_no = self.container_no.replace(" ", "")
			if not re.fullmatch(r"[A-Z]{4}[0-9]{7}", self.container_no):
				frappe.throw(_("For a standard sea container, Tracking / Unit Reference must contain four letters followed by seven digits."))
		if self.etd and self.eta and self.etd > self.eta:
			frappe.throw(_("Estimated Arrival cannot be before Estimated Departure."))
		if self.actual_departure and self.actual_arrival and self.actual_departure > self.actual_arrival:
			frappe.throw(_("Actual Arrival cannot be before Actual Departure."))

	def _set_and_validate_mode(self):
		if not self.shipment_type or not self.shipment:
			return
		parent_mode = frappe.db.get_value(self.shipment_type, self.shipment, "shipment_mode")
		if not parent_mode:
			return
		if not self.shipment_mode:
			self.shipment_mode = parent_mode
		elif parent_mode != "Multimodal" and self.shipment_mode != parent_mode:
			frappe.throw(
				_("Shipment Mode must be {0} to match shipment {1}.").format(
					frappe.bold(parent_mode), frappe.bold(self.shipment)
				)
			)
