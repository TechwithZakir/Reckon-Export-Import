def get_data():
	return {
		"fieldname": "shipment",
		"non_standard_fieldnames": {"Export Realisation": "export_shipment"},
		"transactions": [
			{"label": "Trade Finance", "items": ["Trade LC", "LC Discrepancy", "Export Realisation"]},
			{"label": "Documents", "items": ["Trade Document", "Document Checklist"]},
			{"label": "Logistics", "items": ["Shipment Booking", "Shipment Container", "Customs Declaration"]},
			{"label": "Costs", "items": ["Shipment Cost Sheet"]},
		],
	}
