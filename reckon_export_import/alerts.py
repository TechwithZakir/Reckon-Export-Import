from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import add_days, getdate, nowdate


def send_trade_deadline_alerts():
	"""Send one concise daily digest to trade users when deadlines are near."""
	today = getdate(nowdate())
	lcs = frappe.get_all(
		"Trade LC",
		filters={"docstatus": ["<", 2], "expiry_date": ["between", [today, add_days(today, 7)]]},
		fields=["name", "lc_number", "expiry_date", "party"],
		order_by="expiry_date asc",
	)
	tracking_units = frappe.get_all(
		"Shipment Container",
		filters={"last_free_date": ["between", [today, add_days(today, 3)]], "status": ["not in", ["Delivered", "Empty Returned"]]},
		fields=["name", "container_no", "last_free_date", "shipment"],
		order_by="last_free_date asc",
	)
	if not lcs and not tracking_units:
		return

	recipients = frappe.get_all(
		"Has Role",
		filters={"role": ["in", ["Import Manager", "Export Manager", "Trade Finance Officer"]], "parenttype": "User"},
		pluck="parent",
	)
	emails = frappe.get_all("User", filters={"name": ["in", recipients], "enabled": 1}, pluck="email")
	if not emails:
		return

	rows = [_("LC {0} ({1}) expires on {2}").format(d.lc_number, d.party, d.expiry_date) for d in lcs]
	rows += [_("Shipment unit {0} last free/storage date is {1}").format(d.container_no, d.last_free_date) for d in tracking_units]
	frappe.sendmail(recipients=list(set(emails)), subject=_("Export Import deadline alerts"), message="<br>".join(rows))
