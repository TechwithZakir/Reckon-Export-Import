from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document


class TradeShipment(Document):
	order_doctype: str

	def validate(self):
		self._validate_orders()
		self._validate_dates()

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

