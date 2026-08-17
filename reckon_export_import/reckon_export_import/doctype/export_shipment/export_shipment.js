frappe.ui.form.on("Export Shipment", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.docstatus !== 1) return;
		const next = {
			Planned: "Booked",
			Booked: "In Transit",
			"In Transit": "Arrived",
			Arrived: "Delivered",
			Delivered: "Financially Closed",
		}[frm.doc.status];
		if (next) {
			frm.add_custom_button(__(next), () => {
				frappe.call({
					method: "reckon_export_import.reckon_export_import.doctype.trade_shipment.set_shipment_status",
					args: { doctype: frm.doctype, name: frm.doc.name, status: next },
					freeze: true,
					callback: () => frm.reload_doc(),
				});
			}, __("Update Status"));
		}
	},
});

