from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import add_days, date_diff, getdate, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	today = getdate(nowdate())
	end = add_days(today, int(filters.horizon or 30))
	columns = [
		{"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 85},
		{"label": _("Deadline"), "fieldname": "deadline_type", "fieldtype": "Data", "width": 145},
		{"label": _("Reference"), "fieldname": "reference", "fieldtype": "Dynamic Link", "options": "doctype", "width": 150},
		{"label": _("Party / Container"), "fieldname": "subject", "fieldtype": "Data", "width": 180},
		{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 105},
		{"label": _("Days Remaining"), "fieldname": "days_remaining", "fieldtype": "Int", "width": 110},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 125},
		{"label": _("Owner"), "fieldname": "owner", "fieldtype": "Link", "options": "User", "width": 150},
	]
	date_filter = ["<=", end] if filters.include_overdue else ["between", [today, end]]
	common = {"expiry_date": date_filter, "docstatus": ["<", 2], "status": ["not in", ["Closed", "Cancelled"]]}
	if filters.company:
		common["company"] = filters.company
	data = []
	for row in frappe.get_list("Trade LC", filters=common, fields=["name", "lc_number", "party", "expiry_date", "status", "owner"]):
		data.append(_deadline("LC Expiry", "Trade LC", row.name, f"{row.lc_number} · {row.party}", row.expiry_date, row.status, row.owner, today))
	container_filters = {"last_free_date": date_filter, "status": ["not in", ["Delivered", "Empty Returned"]]}
	for row in frappe.get_list("Shipment Container", filters=container_filters, fields=["name", "container_no", "last_free_date", "status", "owner"]):
		data.append(_deadline("Free / Storage Time", "Shipment Container", row.name, row.container_no, row.last_free_date, row.status, row.owner, today))
	data.sort(key=lambda row: row["days_remaining"])
	return columns, data


def _deadline(label, doctype, name, subject, due_date, status, owner, today):
	days = date_diff(due_date, today)
	priority = _("Overdue") if days < 0 else (_("Urgent") if days <= 7 else _("Upcoming"))
	return {"priority": priority, "deadline_type": label, "doctype": doctype, "reference": name,
		"subject": subject, "due_date": due_date, "days_remaining": days, "status": status, "owner": owner}
