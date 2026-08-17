def get_data():
	return {
		"fieldname": "shipment",
		"transactions": [
			{"label": "Trade Finance", "items": ["Trade LC", "LC Discrepancy"]},
			{"label": "Documents", "items": ["Trade Document", "Document Checklist"]},
			{"label": "Logistics", "items": ["Shipment Booking", "Shipment Container", "Customs Declaration"]},
			{"label": "Costs", "items": ["Shipment Cost Sheet"]},
		],
	}
