frappe.query_reports["Trade Deadline Monitor"] = {
	filters: [
		{ fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
		{ fieldname: "horizon", label: __("Due Within (Days)"), fieldtype: "Int", default: 30, reqd: 1 },
		{ fieldname: "include_overdue", label: __("Include Overdue"), fieldtype: "Check", default: 1 },
	],
};
