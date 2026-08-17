frappe.query_reports["LC Amendment and Discrepancy Analysis"] = { filters: [
	{ fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
	{ fieldname: "lc_type", label: __("LC Type"), fieldtype: "Select", options: "\nImport\nExport" },
] };
