app_name = "reckon_export_import"
app_title = "Reckon Export Import"
app_publisher = "Reckon"
app_description = "Import and export management for ERPNext"
app_email = "support@example.com"
app_license = "GPL-3.0-or-later"

required_apps = ["erpnext"]

fixtures = [
	{"dt": "Role", "filters": [["name", "in", [
		"Import Manager",
		"Export Manager",
		"Trade Finance Officer",
		"Trade Documentation Officer",
	]]]},
]

