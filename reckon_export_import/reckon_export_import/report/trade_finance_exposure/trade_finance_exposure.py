from __future__ import annotations

import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("LC Type"), "fieldname": "lc_type", "fieldtype": "Data", "width": 80},
		{"label": _("LC"), "fieldname": "name", "fieldtype": "Link", "options": "Trade LC", "width": 145},
		{"label": _("LC Number"), "fieldname": "lc_number", "fieldtype": "Data", "width": 145},
		{"label": _("Party"), "fieldname": "party", "fieldtype": "Dynamic Link", "options": "party_type", "width": 170},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("LC Amount"), "fieldname": "lc_amount", "fieldtype": "Currency", "options": "currency", "width": 125},
		{"label": _("Utilized"), "fieldname": "utilized_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Available"), "fieldname": "available_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Utilization %"), "fieldname": "utilization", "fieldtype": "Percent", "width": 105},
		{"label": _("Expiry"), "fieldname": "expiry_date", "fieldtype": "Date", "width": 100},
		{"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 80},
	]
	doc_filters = {"docstatus": ["<", 2], "status": ["not in", ["Closed", "Cancelled"]]}
	if filters.company:
		doc_filters["company"] = filters.company
	if filters.lc_type:
		doc_filters["lc_type"] = filters.lc_type
	data = frappe.get_list("Trade LC", filters=doc_filters, fields=["name", "lc_type", "lc_number", "party_type", "party", "status", "lc_amount", "utilized_amount", "available_amount", "expiry_date", "currency"], order_by="expiry_date asc")
	for row in data:
		row.utilization = (row.utilized_amount or 0) * 100 / row.lc_amount if row.lc_amount else 0
	return columns, data
