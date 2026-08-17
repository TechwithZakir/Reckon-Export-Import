frappe.query_reports["Demurrage and Storage Exposure"] = { filters: [
	{ fieldname: "shipment_mode", label: __("Mode"), fieldtype: "Select", options: "\nSea\nAir\nRoad\nLand\nRail\nCourier\nMultimodal" },
	{ fieldname: "only_at_risk", label: __("Only At Risk / Overdue"), fieldtype: "Check", default: 1 },
] };
