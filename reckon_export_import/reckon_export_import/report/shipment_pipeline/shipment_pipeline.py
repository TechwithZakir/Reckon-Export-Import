from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import date_diff, getdate, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("Type"), "fieldname": "shipment_type", "fieldtype": "Data", "width": 90},
		{"label": _("Shipment"), "fieldname": "shipment", "fieldtype": "Dynamic Link", "options": "doctype", "width": 145},
		{"label": _("Party"), "fieldname": "party", "fieldtype": "Data", "width": 170},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 125},
		{"label": _("Mode"), "fieldname": "shipment_mode", "fieldtype": "Data", "width": 85},
		{"label": _("ETA"), "fieldname": "eta", "fieldtype": "Date", "width": 100},
		{"label": _("Days to ETA"), "fieldname": "days_to_eta", "fieldtype": "Int", "width": 95},
		{"label": _("Goods Value"), "fieldname": "goods_value", "fieldtype": "Currency", "options": "currency", "width": 125},
		{"label": _("Actual Cost"), "fieldname": "actual_cost", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 80},
	]
	data = []
	for kind, doctype, party_field in (("Import", "Import Shipment", "supplier"), ("Export", "Export Shipment", "customer")):
		if filters.shipment_type and filters.shipment_type != kind:
			continue
		doc_filters = {}
		if filters.company:
			doc_filters["company"] = filters.company
		if filters.status:
			doc_filters["status"] = filters.status
		rows = frappe.get_list(doctype, filters=doc_filters, fields=[
			"name", party_field, "status", "shipment_mode", "estimated_arrival_date",
			"goods_value", "actual_cost", "currency",
		], order_by="estimated_arrival_date asc, modified desc")
		for row in rows:
			eta = getdate(row.estimated_arrival_date) if row.estimated_arrival_date else None
			data.append({
				"shipment_type": kind, "doctype": doctype, "shipment": row.name,
				"party": row.get(party_field), "status": row.status,
				"shipment_mode": row.shipment_mode, "eta": eta,
				"days_to_eta": date_diff(eta, getdate(nowdate())) if eta else None,
				"goods_value": row.goods_value, "actual_cost": row.actual_cost,
				"currency": row.currency,
			})
	chart = {
		"data": {"labels": [], "datasets": [{"name": _("Shipments"), "values": []}]},
		"type": "bar",
	}
	counts = {}
	for row in data:
		counts[row["status"]] = counts.get(row["status"], 0) + 1
	chart["data"]["labels"] = list(counts)
	chart["data"]["datasets"][0]["values"] = list(counts.values())
	return columns, data, None, chart
