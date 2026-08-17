app_name = "reckon_export_import"
app_title = "Reckon Export Import"
app_publisher = "Reckon"
app_description = "Import and export management for ERPNext"
app_email = "support@example.com"
app_license = "GPL-3.0-or-later"

required_apps = ["erpnext"]

after_install = "reckon_export_import.install.sync_workspace"
after_migrate = "reckon_export_import.install.sync_workspace"

fixtures = [
	{"dt": "Role", "filters": [["name", "in", [
		"Import Manager",
		"Export Manager",
		"Trade Finance Officer",
		"Trade Documentation Officer",
	]]]},
	{"dt": "Print Format", "filters": [["name", "=", "Trade Document Standard"]]},
]

scheduler_events = {
	"daily": ["reckon_export_import.alerts.send_trade_deadline_alerts"],
}
