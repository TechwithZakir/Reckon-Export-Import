import frappe


WORKSPACE_NAME = "Reckon Export Import"


def sync_workspace():
	"""Force the standard Workspace to match the app's exported JSON.

	Frappe can preserve a database copy of an existing Workspace during an app
	upgrade, particularly after the Workspace was opened in edit mode. Reloading
	the standard document makes new shortcuts and cards reliably available on
	both Frappe 15 and 16.
	"""
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
