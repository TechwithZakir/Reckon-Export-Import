frappe.ui.form.on("Shipment Cost Sheet", {
	refresh(frm) {
		if (frm.doc.docstatus !== 1 || frm.doc.shipment_type !== "Import Shipment") return;
		if (frm.doc.landed_cost_voucher) {
			frm.add_custom_button(__("Open Landed Cost Voucher"), () =>
				frappe.set_route("Form", "Landed Cost Voucher", frm.doc.landed_cost_voucher));
			return;
		}
		frm.add_custom_button(__("Create Landed Cost Voucher"), () => {
			frappe.call({
				method: "reckon_export_import.reckon_export_import.doctype.shipment_cost_sheet.shipment_cost_sheet.create_landed_cost_voucher",
				args: { source_name: frm.doc.name },
				freeze: true,
				freeze_message: __("Creating Landed Cost Voucher..."),
				callback: (r) => r.message && frappe.set_route("Form", "Landed Cost Voucher", r.message),
			});
		}, __("Create"));
	},
});
