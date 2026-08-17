import frappe
from frappe import _
from frappe.utils import date_diff, getdate, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("Tracking Unit"), "fieldname": "name", "fieldtype": "Link", "options": "Shipment Container", "width": 150}, {"label": _("Shipment Type"), "fieldname": "shipment_type", "fieldtype": "Data", "width": 110}, {"label": _("Shipment"), "fieldname": "shipment", "fieldtype": "Dynamic Link", "options": "shipment_type", "width": 140},
		{"label": _("Mode"), "fieldname": "shipment_mode", "fieldtype": "Data", "width": 75}, {"label": _("Carrier"), "fieldname": "shipping_line", "fieldtype": "Data", "width": 140}, {"label": _("Unit Type"), "fieldname": "container_type", "fieldtype": "Data", "width": 85}, {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 105},
		{"label": _("Last Free Date"), "fieldname": "last_free_date", "fieldtype": "Date", "width": 105}, {"label": _("Days to / Over Free Date"), "fieldname": "days_to_free", "fieldtype": "Int", "width": 145}, {"label": _("Risk"), "fieldname": "risk", "fieldtype": "Data", "width": 85}, {"label": _("Recorded Charges"), "fieldname": "demurrage_amount", "fieldtype": "Currency", "width": 125},
	]
	doc_filters = {"status": ["not in", ["Delivered", "Empty Returned", "Cancelled"]]}
	if filters.shipment_mode: doc_filters["shipment_mode"] = filters.shipment_mode
	data = frappe.get_list("Shipment Container", filters=doc_filters, fields=["name", "shipment_type", "shipment", "shipment_mode", "shipping_line", "container_type", "status", "last_free_date", "demurrage_amount"])
	today = getdate(nowdate())
	result = []
	for row in data:
		row.days_to_free = date_diff(row.last_free_date, today) if row.last_free_date else None
		row.risk = _("Overdue") if row.days_to_free is not None and row.days_to_free < 0 else (_("At Risk") if row.days_to_free is not None and row.days_to_free <= 3 else _("Normal"))
		if not filters.only_at_risk or row.risk != _("Normal"):
			result.append(row)
	chart = {"data": {"labels": [_("Overdue"), _("At Risk"), _("Normal")], "datasets": [{"values": [sum(row.risk == _("Overdue") for row in result), sum(row.risk == _("At Risk") for row in result), sum(row.risk == _("Normal") for row in result)]}]}, "type": "donut"}
	return columns, result, None, chart
