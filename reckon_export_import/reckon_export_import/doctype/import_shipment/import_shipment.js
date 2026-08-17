frappe.ui.form.on("Import Shipment", {
	refresh(frm) {
		add_shipment_actions(frm);
	},
});

function add_shipment_actions(frm) {
	if (frm.is_new() || frm.doc.docstatus !== 1) return;
	const next = {
		Planned: "Booked",
		Booked: "In Transit",
		"In Transit": "Arrived",
		Arrived: "Customs Clearance",
		"Customs Clearance": "Received",
		Received: "Financially Closed",
	}[frm.doc.status];
	if (next) {
		frm.add_custom_button(__(next), () => set_status(frm, next), __("Update Status"));
	}
}

function set_status(frm, status) {
	frappe.call({
		method: "reckon_export_import.reckon_export_import.doctype.trade_shipment.set_shipment_status",
		args: { doctype: frm.doctype, name: frm.doc.name, status },
		freeze: true,
		callback: () => frm.reload_doc(),
	});
}

