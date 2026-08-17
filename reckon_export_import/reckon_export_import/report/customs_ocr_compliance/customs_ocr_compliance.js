frappe.query_reports["Customs and Document Compliance"] = { filters: [
	{ fieldname: "country", label: __("Country"), fieldtype: "Link", options: "Country", default: "Bangladesh" },
	{ fieldname: "only_attention", label: __("Only Requiring Attention"), fieldtype: "Check", default: 1 },
] };
