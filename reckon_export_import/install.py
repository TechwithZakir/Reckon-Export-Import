import json

import frappe


WORKSPACE_NAME = "Reckon Export Import"


def sync_workspace():
	"""Force the standard Workspace to match the app's exported JSON.

	Frappe can preserve a database copy of an existing Workspace during an app
	upgrade, particularly after the Workspace was opened in edit mode. Reloading
	the standard document makes new shortcuts and cards reliably available on
	both Frappe 15 and 16.
	"""
	_sync_home_page_insights()
	frappe.reload_doc(
		"reckon_export_import",
		"workspace",
		"reckon_export_import",
		force=True,
	)
	if frappe.db.exists("Workspace", WORKSPACE_NAME):
		frappe.db.set_value(
			"Workspace",
			WORKSPACE_NAME,
			{"label": "Export Import", "title": "Export Import", "is_hidden": 0},
			update_modified=False,
		)
	frappe.clear_cache()


def _sync_home_page_insights():
	"""Create the standard cards and charts referenced by the module workspace."""
	for spec in _number_cards():
		_upsert("Number Card", spec["name"], spec)
	for spec in _dashboard_charts():
		_upsert("Dashboard Chart", spec["name"], spec)


def _upsert(doctype, name, values):
	meta = frappe.get_meta(doctype)
	values = {key: value for key, value in values.items() if key == "name" or meta.has_field(key)}
	if frappe.db.exists(doctype, name):
		doc = frappe.get_doc(doctype, name)
		doc.update(values)
		doc.flags.ignore_permissions = True
		doc.save()
	else:
		doc = frappe.get_doc({"doctype": doctype, **values})
		doc.flags.ignore_permissions = True
		doc.insert()


def _number_cards():
	return [
		_count_card("Active Import Shipments", "Import Shipment", [["Import Shipment", "status", "not in", ["Financially Closed", "Cancelled"], False]], "Blue"),
		_count_card("Active Export Shipments", "Export Shipment", [["Export Shipment", "status", "not in", ["Financially Closed", "Cancelled"], False]], "Green"),
		_count_card("LCs Expiring in 30 Days", "Trade LC", [["Trade LC", "expiry_date", "Timespan", "next 30 days", False], ["Trade LC", "status", "not in", ["Closed", "Cancelled"], False]], "Orange"),
		_count_card("Overdue Export Collections", "Export Realisation", [["Export Realisation", "status", "=", "Overdue", False]], "Red"),
	]


def _count_card(name, document_type, filters, color):
	return {
		"name": name, "label": name, "type": "Document Type", "document_type": document_type,
		"function": "Count", "aggregate_function_based_on": "", "filters_json": json.dumps(filters),
		"is_public": 1, "show_percentage_stats": 1, "stats_time_interval": "Monthly", "color": color,
	}


def _dashboard_charts():
	return [
		_group_chart("Import Shipment Status", "Import Shipment", "status", "Donut"),
		_group_chart("Export Shipment Status", "Export Shipment", "status", "Donut"),
		_group_chart("LC Portfolio by Status", "Trade LC", "status", "Bar"),
		_group_chart("Export Collection Status", "Export Realisation", "status", "Bar"),
	]


def _group_chart(name, document_type, group_by, chart_type):
	return {
		"name": name, "chart_name": name, "chart_type": "Group By", "document_type": document_type,
		"group_by_type": "Count", "group_by_based_on": group_by, "number_of_groups": 10,
		"type": chart_type, "is_public": 1, "timespan": "Last Year", "time_interval": "Monthly",
		"filters_json": "[]", "show_values_over_chart": 1,
	}
