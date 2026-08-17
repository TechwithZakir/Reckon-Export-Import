import frappe
from frappe import _
from frappe.utils import date_diff, getdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("Booking"), "fieldname": "name", "fieldtype": "Link", "options": "Shipment Booking", "width": 145},
		{"label": _("Shipment Type"), "fieldname": "shipment_type", "fieldtype": "Data", "width": 115},
		{"label": _("Shipment"), "fieldname": "shipment", "fieldtype": "Dynamic Link", "options": "shipment_type", "width": 145},
		{"label": _("Mode"), "fieldname": "mode", "fieldtype": "Data", "width": 85},
		{"label": _("Carrier"), "fieldname": "carrier", "fieldtype": "Data", "width": 140},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 105},
		{"label": _("Legs"), "fieldname": "leg_count", "fieldtype": "Int", "width": 60},
		{"label": _("Delayed Legs"), "fieldname": "delayed_legs", "fieldtype": "Int", "width": 95},
		{"label": _("Departure Delay"), "fieldname": "departure_delay", "fieldtype": "Int", "width": 110},
		{"label": _("Arrival Delay"), "fieldname": "arrival_delay", "fieldtype": "Int", "width": 100},
		{"label": _("Quoted Freight"), "fieldname": "quoted_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 75},
	]
	doc_filters = {}
	if filters.mode: doc_filters["mode"] = filters.mode
	if filters.status: doc_filters["status"] = filters.status
	data = frappe.get_list("Shipment Booking", filters=doc_filters, fields=["name", "shipment_type", "shipment", "mode", "carrier", "status", "quoted_amount", "currency"])
	for row in data:
		legs = frappe.get_all("Shipment Schedule Leg", filters={"parent": row.name, "parenttype": "Shipment Booking"}, fields=["status", "planned_departure", "revised_departure", "actual_departure", "planned_arrival", "revised_arrival", "actual_arrival"], order_by="sequence asc")
		row.leg_count = len(legs)
		row.delayed_legs = sum(1 for leg in legs if leg.status == "Delayed")
		row.departure_delay = _delay(legs[0].actual_departure, legs[0].revised_departure or legs[0].planned_departure) if legs else 0
		row.arrival_delay = _delay(legs[-1].actual_arrival, legs[-1].revised_arrival or legs[-1].planned_arrival) if legs else 0
	chart = {"data": {"labels": [_("On Schedule"), _("Delayed")], "datasets": [{"values": [sum(not row.delayed_legs for row in data), sum(bool(row.delayed_legs) for row in data)]}]}, "type": "donut"}
	return columns, data, None, chart


def _delay(actual, planned):
	return max(date_diff(getdate(actual), getdate(planned)), 0) if actual and planned else 0
