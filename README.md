# Reckon Export Import

Trade operations for ERPNext, covering import/export shipments, letters of credit,
shipping documents, customs clearance, containers, landed costs, and export
realisation.

## Compatibility

- Frappe Framework 15 / ERPNext 15
- Frappe Framework 16 / ERPNext 16
- Python 3.10 through 3.14 (subject to the selected Frappe release)

The app uses ERPNext as the source of truth for orders, stock, invoices,
payments, and general-ledger entries. It adds an operational layer that links
those records into a shipment file.

## Development install

```bash
bench get-app https://github.com/TechwithZakir/Reckon-Export-Import
bench --site your-site.local install-app reckon_export_import
bench --site your-site.local migrate
```

After updating an existing installation, run:

```bash
bench --site your-site.local migrate
bench --site your-site.local clear-cache
bench build --app reckon_export_import
```

Then open `/app/reckon-export-import`. Do not use
`/app/reckon_export_import`; Frappe Desk routes use hyphens.

## Initial roadmap

1. Import Shipment and Export Shipment control records
2. Trade LC and amendments
3. Trade-document checklists and document generation
4. Containers and logistics milestones
5. Customs declarations and shipment costs
6. Landed Cost Voucher and Export Realisation integration
