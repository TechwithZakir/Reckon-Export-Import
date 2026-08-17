frappe.query_reports["Shipment Pipeline"] = {
	filters: [
		{ fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
		{ fieldname: "shipment_type", label: __("Shipment Type"), fieldtype: "Select", options: "\nImport\nExport" },
		{ fieldname: "status", label: __("Status"), fieldtype: "Data" },
	],
};
