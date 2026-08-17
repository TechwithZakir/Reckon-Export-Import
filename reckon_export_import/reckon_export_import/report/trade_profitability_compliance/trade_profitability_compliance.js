frappe.query_reports["Trade Profitability and Compliance"] = {
	filters: [
		{ fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
		{ fieldname: "shipment_type", label: __("Shipment Type"), fieldtype: "Select", options: "\nImport Shipment\nExport Shipment" },
	],
};
