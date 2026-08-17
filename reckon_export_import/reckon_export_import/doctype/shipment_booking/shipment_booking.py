import frappe
from frappe import _
from frappe.model.document import Document


class ShipmentBooking(Document):
	def validate(self):
		parent_mode = frappe.db.get_value(self.shipment_type, self.shipment, "shipment_mode")
		if parent_mode and parent_mode != "Multimodal" and self.mode != parent_mode:
			frappe.throw(_("Booking mode must match the linked shipment mode {0}.").format(parent_mode))
		sequences = [row.sequence for row in self.schedule_legs]
		if len(sequences) != len(set(sequences)):
			frappe.throw(_("Schedule leg sequence numbers must be unique."))
		for row in self.schedule_legs:
			departure = row.revised_departure or row.planned_departure
			arrival = row.revised_arrival or row.planned_arrival
			if departure and arrival and arrival < departure:
				frappe.throw(_("Row {0}: arrival cannot be before departure.").format(row.idx))

	def on_submit(self):
		if self.status != "Confirmed":
			frappe.throw(_("Only a Confirmed booking can be submitted."))
		shipment = frappe.get_doc(self.shipment_type, self.shipment)
		legs = sorted(self.schedule_legs, key=lambda row: row.sequence)
		if legs:
			shipment.db_set({"estimated_departure_date": (legs[0].revised_departure or legs[0].planned_departure), "estimated_arrival_date": (legs[-1].revised_arrival or legs[-1].planned_arrival), "status": "Booked"})
