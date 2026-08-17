import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("LC"), "fieldname": "name", "fieldtype": "Link", "options": "Trade LC", "width": 140}, {"label": _("LC Number"), "fieldname": "lc_number", "fieldtype": "Data", "width": 140},
		{"label": _("Type"), "fieldname": "lc_type", "fieldtype": "Data", "width": 70}, {"label": _("Party"), "fieldname": "party", "fieldtype": "Data", "width": 150}, {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": _("LC Amount"), "fieldname": "lc_amount", "fieldtype": "Currency", "options": "currency", "width": 120}, {"label": _("Amendments"), "fieldname": "amendment_count", "fieldtype": "Int", "width": 90}, {"label": _("Amendment Charges"), "fieldname": "amendment_charges", "fieldtype": "Currency", "options": "currency", "width": 135},
		{"label": _("Open Findings"), "fieldname": "open_findings", "fieldtype": "Int", "width": 100}, {"label": _("Critical Findings"), "fieldname": "critical_findings", "fieldtype": "Int", "width": 110}, {"label": _("Discrepancy Fees"), "fieldname": "discrepancy_fees", "fieldtype": "Currency", "options": "currency", "width": 125}, {"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 75},
	]
	doc_filters = {"docstatus": ["<", 2]}
	if filters.company: doc_filters["company"] = filters.company
	if filters.lc_type: doc_filters["lc_type"] = filters.lc_type
	data = frappe.get_list("Trade LC", filters=doc_filters, fields=["name", "lc_number", "lc_type", "party", "status", "lc_amount", "currency"])
	for row in data:
		amendments = frappe.get_all("LC Amendment", filters={"trade_lc": row.name, "docstatus": ["<", 2]}, fields=["charges"])
		findings = frappe.get_all("LC Discrepancy", filters={"trade_lc": row.name}, fields=["status", "severity", "fee"])
		open_rows = [item for item in findings if item.status not in {"Waived", "Resolved", "Rejected"}]
		row.update({"amendment_count": len(amendments), "amendment_charges": sum(flt(item.charges) for item in amendments), "open_findings": len(open_rows), "critical_findings": sum(item.severity == "Critical" for item in open_rows), "discrepancy_fees": sum(flt(item.fee) for item in findings)})
	return columns, data
