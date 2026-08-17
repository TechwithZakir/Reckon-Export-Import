# Changelog

## 0.2.1 - 2026-08-17

- Force-reload the standard Export Import Workspace after installation and
  migration so renamed labels and newly added MVP links replace stale database
  content.

## 0.2.0 - 2026-08-17

First MVP release for Frappe/ERPNext 15 and 16.

### Added

- Import and Export Shipment control records with guided status actions
- Trade LC management with utilization and expiry controls
- Commercial Invoice, Packing List, Bill of Lading, and Air Waybill through Trade Document
- Trade-document item lines and standard Jinja print format
- Customs declarations and calculated duty/tax totals
- Container tracking, milestones, last-free-date, and demurrage information
- Shipment Cost Sheet with estimated/actual variance
- Draft Landed Cost Voucher generation from Import Shipment Purchase Receipts
- Export Realisation with net receipt and outstanding calculations
- Shipment document checklists with completion percentage
- Workspace navigation and shipment dashboard links
- Daily LC-expiry and container-free-day email alerts
- Two-column layouts across operational forms

### Upgrade

```bash
bench --site your-site.local migrate
bench --site your-site.local clear-cache
bench build --app reckon_export_import
bench restart
```
