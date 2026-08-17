frappe.ui.form.on("Shipment Container", {
	setup(frm) {
		frm.set_query("shipment", () => ({
			filters: { docstatus: ["<", 2] },
		}));
	},

	shipment(frm) {
		if (!frm.doc.shipment_type || !frm.doc.shipment) return;
		frappe.db.get_value(frm.doc.shipment_type, frm.doc.shipment, [
			"shipment_mode", "port_of_loading", "port_of_discharge",
			"estimated_departure_date", "estimated_arrival_date",
		]).then(({ message: values }) => {
			if (!values) return;
			frm.set_value("shipment_mode", values.shipment_mode);
			frm.set_value("port_of_loading", frm.doc.port_of_loading || values.port_of_loading);
			frm.set_value("port_of_discharge", frm.doc.port_of_discharge || values.port_of_discharge);
			frm.set_value("etd", frm.doc.etd || values.estimated_departure_date);
			frm.set_value("eta", frm.doc.eta || values.estimated_arrival_date);
		});
	},
});
