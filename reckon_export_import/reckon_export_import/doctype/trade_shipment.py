from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document


class TradeShipment(Document):
	order_doctype: str

	def validate(self):
		self._validate_orders()
		self._validate_dates()

	def on_submit(self):
		if self.status == "Draft":
			self.db_set("status", "Planned")

	def on_cancel(self):
		self.db_set("status", "Cancelled")

	def _validate_orders(self):
		for row in self.orders:
			if row.order_doctype != self.order_doctype:
				frappe.throw(
					_("Row {0}: {1} shipments may only contain {2} records.").format(
						row.idx, self.shipment_direction.lower(), self.order_doctype
					)
				)

	def _validate_dates(self):
		if self.estimated_departure_date and self.estimated_arrival_date:
			if self.estimated_arrival_date < self.estimated_departure_date:
				frappe.throw(_("Estimated arrival cannot be before estimated departure."))

	@property
	def shipment_direction(self) -> str:
		return "Import" if self.order_doctype == "Purchase Order" else "Export"


@frappe.whitelist()
def set_shipment_status(doctype: str, name: str, status: str):
	allowed_doctypes = {"Import Shipment", "Export Shipment"}
	if doctype not in allowed_doctypes:
		frappe.throw(_("Invalid shipment type."))

	doc = frappe.get_doc(doctype, name)
	doc.check_permission("write")
	transitions = {
		"Planned": {"Booked"},
		"Booked": {"In Transit"},
		"In Transit": {"Arrived"},
		"Arrived": {"Customs Clearance", "Delivered"},
		"Customs Clearance": {"Received", "Delivered"},
		"Received": {"Financially Closed"},
		"Delivered": {"Financially Closed"},
	}
	if status not in transitions.get(doc.status, set()):
		frappe.throw(_("Status cannot move from {0} to {1}.").format(doc.status, status))
	doc.db_set("status", status)
	return doc.status
