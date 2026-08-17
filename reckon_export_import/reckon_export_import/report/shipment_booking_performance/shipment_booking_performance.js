frappe.query_reports["Shipment Booking Performance"] = { filters: [
	{ fieldname: "mode", label: __("Mode"), fieldtype: "Select", options: "\nSea\nAir\nRoad\nLand\nRail\nCourier\nMultimodal" },
	{ fieldname: "status", label: __("Booking Status"), fieldtype: "Select", options: "\nDraft\nRequested\nQuoted\nConfirmed\nRolled Over\nCompleted\nCancelled" },
] };
