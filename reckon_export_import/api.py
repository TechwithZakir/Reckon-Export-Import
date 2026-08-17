from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import now_datetime


@frappe.whitelist(allow_guest=False)
def get_portal_shipments():
	"""Return a deliberately small party-scoped view for existing ERPNext portal users."""
	if frappe.session.user == "Guest":
		frappe.throw(_("Authentication required."), frappe.PermissionError)
	contact = frappe.db.get_value("Contact", {"user": frappe.session.user}, "name")
	if not contact:
		return []
	party_links = frappe.get_all(
		"Dynamic Link",
		filters={"parenttype": "Contact", "parent": contact, "link_doctype": ["in", ["Customer", "Supplier"]]},
		fields=["link_doctype", "link_name"],
	)
	results = []
	for link in party_links:
		doctype = "Export Shipment" if link.link_doctype == "Customer" else "Import Shipment"
		party_field = "customer" if link.link_doctype == "Customer" else "supplier"
		for row in frappe.get_all(
			doctype,
			filters={party_field: link.link_name, "docstatus": ["<", 2]},
			fields=["name", "status", "shipment_mode", "estimated_departure_date", "estimated_arrival_date"],
			order_by="modified desc",
		):
			results.append({"shipment_type": doctype, **row})
	return results


@frappe.whitelist()
def update_mobile_milestone(tracking_unit, status, event_time=None, latitude=None, longitude=None, notes=None):
	doc = frappe.get_doc("Shipment Container", tracking_unit)
	doc.check_permission("write")
	allowed = {"Picked Up", "Gate In", "Loaded", "Departed", "In Transit", "Arrived", "Discharged", "Released", "Out for Delivery", "Delivered", "Empty Returned"}
	if status not in allowed:
		frappe.throw(_("Invalid mobile milestone."))
	doc.status = status
	if status == "Departed" and not doc.actual_departure:
		doc.actual_departure = event_time or now_datetime()
	if status == "Arrived" and not doc.actual_arrival:
		doc.actual_arrival = event_time or now_datetime()
	location = ", ".join(value for value in (str(latitude or ""), str(longitude or "")) if value)
	doc.add_comment("Info", _("Mobile milestone: {0}{1}{2}").format(status, f" at {location}" if location else "", f" — {notes}" if notes else ""))
	doc.save()
	return {"name": doc.name, "status": doc.status, "modified": doc.modified}
