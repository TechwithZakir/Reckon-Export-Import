import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("Shipment Type"), "fieldname": "shipment_type", "fieldtype": "Data", "width": 120},
		{"label": _("Shipment"), "fieldname": "shipment", "fieldtype": "Dynamic Link", "options": "shipment_type", "width": 150},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 115},
		{"label": _("Goods Value"), "fieldname": "goods_value", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Estimated Cost"), "fieldname": "estimated_cost", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Actual Cost"), "fieldname": "actual_cost", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Cost Variance"), "fieldname": "cost_variance", "fieldtype": "Currency", "options": "currency", "width": 115},
		{"label": _("Cost %"), "fieldname": "cost_percent", "fieldtype": "Percent", "width": 85},
		{"label": _("Open Discrepancies"), "fieldname": "open_discrepancies", "fieldtype": "Int", "width": 130},
		{"label": _("Missing Documents"), "fieldname": "missing_documents", "fieldtype": "Int", "width": 125},
		{"label": _("Compliance"), "fieldname": "compliance", "fieldtype": "Data", "width": 105},
		{"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 80},
	]
	data = []
	for doctype in ("Import Shipment", "Export Shipment"):
		if filters.shipment_type and filters.shipment_type != doctype:
			continue
		doc_filters = {"docstatus": ["<", 2]}
		if filters.company:
			doc_filters["company"] = filters.company
		for row in frappe.get_list(doctype, filters=doc_filters, fields=["name", "status", "goods_value", "estimated_cost", "actual_cost", "currency"]):
			open_discrepancies = frappe.db.count("LC Discrepancy", {"shipment_type": doctype, "shipment": row.name, "status": ["not in", ["Waived", "Resolved", "Rejected"]]})
			checklists = frappe.get_all("Document Checklist", filters={"shipment_type": doctype, "shipment": row.name}, pluck="completion_percentage")
			missing_documents = sum(1 for completion in checklists if flt(completion) < 100)
			actual = flt(row.actual_cost)
			goods = flt(row.goods_value)
			data.append({"shipment_type": doctype, "shipment": row.name, "status": row.status, "goods_value": goods, "estimated_cost": row.estimated_cost, "actual_cost": actual, "cost_variance": actual - flt(row.estimated_cost), "cost_percent": actual * 100 / goods if goods else 0, "open_discrepancies": open_discrepancies, "missing_documents": missing_documents, "compliance": _("Attention") if open_discrepancies or missing_documents else _("Clear"), "currency": row.currency})
	return columns, data
