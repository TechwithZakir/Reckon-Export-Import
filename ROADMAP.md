# Product Roadmap

This roadmap describes planned work after the MVP. It is directional rather
than a release-date commitment. Features should remain compatible with Frappe
and ERPNext 15 and 16 unless a future compatibility note says otherwise.

## Design principles

- ERPNext remains the source of truth for parties, orders, invoices, stock,
  payments, accounts, users, and portal access.
- Shipment records provide the operational file joining trade, logistics,
  customs, document, cost, and settlement activity.
- External integrations use configurable adapters, background jobs, audit
  logs, idempotency keys, encrypted credentials, and manual fallback paths.
- Country rules are versioned and effective-dated. They assist users but do
  not replace advice from customs, banks, carriers, or legal professionals.
- All automated decisions must retain the source, confidence, rule version,
  result, user override, and approval history.

## Phase 2 — Operational control and assisted automation

### 2.1 LC amendments and discrepancy handling

**Scope**

- Add immutable LC amendment records with amendment number, bank reference,
  requested/approved dates, amount and date changes, charges, clauses, and
  attached advice.
- Recalculate the current LC position from the original LC plus approved
  amendments without losing historical terms.
- Add document-presentation and discrepancy cases covering discrepancy type,
  severity, responsible party, waiver status, bank response, fees, resolution,
  and aging.
- Add approval workflow, amendment comparison, expiry alerts, discrepancy
  queues, and audit-ready print views.

**Acceptance criteria**

- Users can reconstruct LC terms as of any date.
- Approved amendments update available exposure exactly once.
- Open discrepancies appear on the module dashboard and block closure unless
  waived or resolved by an authorized user.

### 2.2 Shipment booking and schedules

**Scope**

- Add bookings with carrier, forwarder, service, mode, route legs, booking and
  carrier references, cut-off dates, planned capacity, rate validity, and
  confirmation status.
- Support multiple schedule legs for Sea, Air, Road/Land, Rail, Courier, and
  Multimodal shipments.
- Track planned versus revised versus actual departure/arrival milestones.
- Provide calendar, delay, rollover, missed-cut-off, and unconfirmed-booking
  views.

**Acceptance criteria**

- One shipment may have multiple booking revisions and transport legs.
- A confirmed schedule can populate tracking milestones without overwriting
  actual events.
- Delays and missed operational cut-offs are visible and alertable.

### 2.3 Demurrage, detention, and storage calculations

**Scope**

- Add effective-dated charge tariffs by carrier, terminal, port, equipment
  type, direction, currency, and free-day rule.
- Support calendar or working days, tiered daily rates, combined or separate
  demurrage/detention, holidays, negotiated free days, tax, waivers, and caps.
- Calculate accrued, estimated, invoiced, disputed, waived, and approved
  amounts from discharge, gate-out, delivery, and empty-return events.
- Allow reviewed charges to flow into Shipment Cost Sheet.

**Acceptance criteria**

- Every amount includes an explainable day-by-day calculation.
- Recalculation preserves approved snapshots and records tariff changes.
- Missing milestone or tariff data produces an actionable exception rather
  than a silent zero.

### 2.4 Country-specific customs rules

**Bangladesh-first scope**

- Build a versioned customs-rule engine with Bangladesh as the first preferred
  localization: HS code guidance, document requirements, restricted/prohibited
  item flags, valuation inputs, duty/tax components, exemptions, bond/EPZ
  scenarios, and import/export procedure checklists.
- Store official source URL, issuing authority, circular/SRO reference,
  publication date, effective dates, last verification date, and reviewer.
- Use scheduled source monitoring to flag possible changes for human review;
  never silently activate scraped rules.
- Add declaration-time rule snapshots so historical filings remain
  reproducible after rules change.

**Data-source policy**

- Prefer official Bangladesh Customs/NBR, Bangladesh Bank, CCI&E, BIDA, BEPZA,
  BSTI, Plant Quarantine, and other competent-authority publications.
- Mark third-party material as secondary and require verification against an
  official source before activation.

**Acceptance criteria**

- Each recommendation identifies the country, rule version, effective date,
  and official source.
- Users can review and approve rule updates before they affect transactions.
- The rules engine supports additional country packs without changing core
  shipment code.

### 2.5 Bank and shipping-line integrations

Integrations are possible where the institution exposes an authorized API,
host-to-host channel, EDI/SFTP service, webhook, or supported aggregator.
Screen scraping and shared interactive credentials are out of scope.

**Bank adapter capabilities**

- Import LC/application status, amendments, SWIFT advice metadata, charges,
  document-presentation responses, statements, and export proceeds.
- Submit approved requests only when the bank contract and API permit it.
- Match bank transactions to Trade LC, Shipment Cost Sheet, Payment Entry, and
  Export Realisation records, leaving accounting posting under ERPNext control.

**Carrier/forwarder adapter capabilities**

- Retrieve quotations, booking confirmations, schedules, bills/airway bills,
  tracking events, free-time data, invoices, and exception notices.
- Normalize provider-specific events into internal milestone codes while
  retaining the original payload and provider event ID.

**Architecture and security**

- Define a provider interface and separate adapter package for every provider.
- Store secrets with Frappe Password fields or an external secret manager;
  never store secrets in source control or logs.
- Use background queues, rate limiting, retries with backoff, idempotency,
  webhook signature checks, correlation IDs, health status, and replay tools.
- Start with CSV/Excel and secure file exchange as fallback connectors before
  institution-specific real-time APIs.

### 2.6 Existing customer and supplier portals

**Scope**

- Extend ERPNext's existing Website User and portal permissions rather than
  introducing separate identities.
- Customers see only their export shipments, approved milestones, documents,
  action requests, and collection status appropriate for external sharing.
- Suppliers see only their import shipments, booking/document requests, and
  approved status information.
- Add portal-safe comments and file exchange with malware scanning, file-type
  limits, audit trails, and configurable internal/external visibility.

**Acceptance criteria**

- Desk-only notes, costs, margins, bank data, and unrelated parties never leak
  through portal endpoints.
- Portal access is covered by automated permission tests.

### 2.7 Mobile milestone updates

**Scope**

- Deliver responsive Frappe forms or a focused PWA for authorized operators.
- Support scan/search, milestone update, timestamp, location with consent,
  photo/file proof, notes, exception reason, and offline queueing.
- Prevent event regression and duplicates while allowing supervisor-approved
  corrections.

**Acceptance criteria**

- Common milestone updates take no more than a few taps.
- Offline submissions synchronize idempotently and show conflicts clearly.

### 2.8 OCR-based document capture

**Scope**

- Create an OCR provider interface supporting self-hosted and contracted cloud
  services based on deployment privacy requirements.
- Classify and extract common fields from invoices, packing lists, bills of
  lading, airway bills, certificates, customs papers, and bank advice.
- Present side-by-side source and extracted values with confidence, validation,
  correction, duplicate detection, and approval before record creation.
- Retain provider, model/version, processing consent, hash, confidence, user
  edits, and final disposition.

**Acceptance criteria**

- OCR never posts accounting or submits trade documents without human approval.
- Low-confidence and inconsistent values are highlighted rather than accepted.

### 2.9 Profitability and compliance analytics

**Scope**

- Analyze estimated versus actual logistics cost, landed cost, margin by
  shipment/order/party/lane/mode, delay cost, demurrage leakage, FX impact,
  export realization aging, LC utilization, and provider performance.
- Add compliance indicators for missing/expired documents, unresolved
  discrepancies, overdue actions, rule exceptions, and manual overrides.
- Provide company, date, currency, country, mode, party, and carrier filters
  with drill-through to supporting records.

**Acceptance criteria**

- Financial metrics document their currency and conversion basis.
- Dashboard totals reconcile with report detail and authorized ERPNext records.

## Phase 2 recommended delivery sequence

1. LC amendments and discrepancies
2. Booking, schedules, and multimodal legs
3. Demurrage/detention tariffs and calculations
4. Bangladesh customs rules foundation
5. Profitability and compliance analytics
6. Portal and mobile workflows
7. OCR capture
8. First bank and carrier adapters after provider access is confirmed

## Phase 3 — Connected trade platform

### 3.1 Electronic customs filing

- Introduce a filing-provider adapter, declaration validation, submission
  package, digital-signature handoff, acknowledgements, query/response cycles,
  assessment, payment references, release status, cancellation, and amendment.
- Retain the exact submitted payload, attachments, schema version, credentials
  used, response, timestamp, and human approval.
- Gate development on an authorized national single-window/customs interface,
  certification requirements, sandbox access, and legal approval.
- Always provide export/manual filing packages when electronic submission is
  unavailable.

### 3.2 Live vessel and container tracking APIs

- Add provider-neutral tracking subscriptions for vessel, container, airway
  bill, vehicle, rail consignment, and courier references.
- Ingest webhook or polling events, normalize locations and milestones, retain
  raw evidence, deduplicate events, and calculate ETA confidence and delay.
- Reconcile provider events with user-entered milestones; automated data must
  not silently replace confirmed actual events.
- Track subscription cost, API quota, stale feeds, provider health, and consent.

### 3.3 Trade-finance exposure management

- Consolidate LC outstanding exposure, guarantees, documentary collections,
  export receivables, bank limits, margins, contingent liabilities, currency
  risk, maturities, and utilization by company, bank, party, and country.
- Add sanctioned/blocked-party integration hooks, concentration thresholds,
  limit approvals, stress scenarios, and alerts.
- Reconcile exposure to ERPNext accounts while keeping operational and
  accounting definitions explicit.

### 3.4 Automated document checking

- Combine templates, structured data, OCR output, LC terms, amendments,
  country rules, and cross-document comparison.
- Detect missing documents, inconsistent names/numbers/amounts/dates/weights,
  late presentation, tolerance breaches, and required-clause omissions.
- Produce explainable findings with rule/source, severity, confidence,
  suggested action, reviewer decision, waiver, and audit history.
- Treat automation as decision support; submission and discrepancy acceptance
  remain controlled human actions.

### 3.5 Multi-country localization packs

- Package versioned customs rules, document checklists, terminology, duty/tax
  logic, regulatory sources, filing adapters, calendars, and translations by
  jurisdiction.
- Keep localization packages separate from the core app with declared core
  version compatibility, maintainer, authority sources, tests, and update feed.
- Require effective-dated fixtures and regression cases for every supported
  procedure and major rule change.

## Phase 3 prerequisites

- Stable provider-adapter and country-rule interfaces from Phase 2
- Institution agreements, API credentials, sandbox access, and data-processing
  terms for every connected service
- Threat modeling, privacy review, retention policy, incident procedures, and
  integration observability
- Automated permission, audit, calculation, localization, and integration tests
- Named business owners for customs, finance, logistics, and compliance rules

## Out of scope without explicit authorization

- Bypassing bank, carrier, customs, or portal access controls
- Treating web-scraped regulatory material as automatically authoritative
- Autonomous customs filings, financial postings, discrepancy waivers, or
  legally binding submissions without configured approval
- Storing external-service credentials, full OCR documents, or sensitive API
  payloads in logs or source control

