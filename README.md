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

## Roadmap

The MVP foundation is complete. The detailed [Phase 2 and Phase 3 product
roadmap](ROADMAP.md) covers operational automation, Bangladesh-first customs
rules, integrations, portals, mobile updates, OCR, advanced analytics,
electronic filing, live tracking, and multi-country localization.

The roadmap distinguishes features that can be delivered entirely inside
Frappe from integrations that require institution agreements, authorized APIs,
sandbox credentials, regulatory approval, or external service contracts.

### Phase 2 implementation status

The repository now includes the Phase 2 operational foundation: LC amendments
and discrepancies, multimodal bookings and schedule legs, tiered demurrage and
storage tariffs, verified customs rules, OCR review records, provider-neutral
integration contracts, mobile milestone updates, and profitability/compliance
reporting. Live bank, carrier, and OCR connections remain provider-specific and
require authorized credentials and service agreements before activation.

## MVP 0.2.0

The MVP includes Trade LC, unified printable trade documents, customs
declarations, container tracking, cost sheets, Landed Cost Voucher integration,
export realisation, document checklists, dashboards, lifecycle actions, and
deadline alerts. Forms use two-column sections for efficient data entry; child
tables remain full-width for readability.
