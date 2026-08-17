import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("Declaration"), "fieldname": "name", "fieldtype": "Link", "options": "Customs Declaration", "width": 145}, {"label": _("Direction"), "fieldname": "declaration_type", "fieldtype": "Data", "width": 80}, {"label": _("Shipment Type"), "fieldname": "shipment_type", "fieldtype": "Data", "width": 110}, {"label": _("Shipment"), "fieldname": "shipment", "fieldtype": "Dynamic Link", "options": "shipment_type", "width": 140},
		{"label": _("Country"), "fieldname": "country", "fieldtype": "Link", "options": "Country", "width": 100}, {"label": _("HS Code"), "fieldname": "hs_code", "fieldtype": "Data", "width": 90}, {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Applicable Rules"), "fieldname": "applicable_rules", "fieldtype": "Int", "width": 105}, {"label": _("Blocking Rules"), "fieldname": "blocking_rules", "fieldtype": "Int", "width": 100}, {"label": _("OCR Awaiting Review"), "fieldname": "ocr_review", "fieldtype": "Int", "width": 125}, {"label": _("Checklist Gaps"), "fieldname": "checklist_gaps", "fieldtype": "Int", "width": 100}, {"label": _("Compliance"), "fieldname": "compliance", "fieldtype": "Data", "width": 100},
	]
	doc_filters = {"docstatus": ["<", 2]}
	if filters.country: doc_filters["country"] = filters.country
	data = frappe.get_list("Customs Declaration", filters=doc_filters, fields=["name", "declaration_type", "shipment_type", "shipment", "country", "hs_code", "status"])
	result = []
	for row in data:
		rules = frappe.get_all("Customs Rule", filters={"country": row.country, "status": "Active", "trade_direction": ["in", [row.declaration_type, "Both"]]}, fields=["hs_code_pattern", "severity"])
		applicable = [rule for rule in rules if not rule.hs_code_pattern or (row.hs_code or "").startswith(rule.hs_code_pattern.rstrip("*"))]
		row.applicable_rules = len(applicable)
		row.blocking_rules = sum(rule.severity == "Blocking" for rule in applicable)
		row.ocr_review = frappe.db.count("OCR Document Capture", {"shipment_type": row.shipment_type, "shipment": row.shipment, "status": ["in", ["Queued", "Processing", "Needs Review", "Failed"]]})
		checklists = frappe.get_all("Document Checklist", filters={"shipment_type": row.shipment_type, "shipment": row.shipment, "status": ["not in", ["Complete", "Cancelled"]]}, pluck="name")
		row.checklist_gaps = len(checklists)
		row.compliance = _("Attention") if row.blocking_rules or row.ocr_review or row.checklist_gaps else _("Clear")
		if not filters.only_attention or row.compliance == _("Attention"):
			result.append(row)
	return columns, result
