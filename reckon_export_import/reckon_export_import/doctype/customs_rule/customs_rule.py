import frappe
from frappe import _
from frappe.model.document import Document


class CustomsRule(Document):
	def validate(self):
		if self.effective_to and self.effective_to < self.effective_from:
			frappe.throw(_("Effective To cannot be before Effective From."))
		if self.status == "Active" and (not self.last_verified_date or not self.verified_by):
			frappe.throw(_("Active customs rules require a verification date and reviewer."))
		if self.status == "Active" and not (self.source_url or "").lower().startswith("https://"):
			frappe.throw(_("Active customs rules require an HTTPS official source URL."))


@frappe.whitelist()
def get_applicable_rules(country, direction, hs_code=None, on_date=None):
	from frappe.utils import getdate, nowdate

	on_date = getdate(on_date or nowdate())
	filters = {"country": country, "status": "Active", "effective_from": ["<=", on_date], "trade_direction": ["in", [direction, "Both"]]}
	rules = frappe.get_list("Customs Rule", filters=filters, fields=["name", "rule_type", "title", "hs_code_pattern", "requirement", "severity", "authority", "source_url", "reference_no", "version", "effective_from", "effective_to"], order_by="severity desc, title asc")
	return [rule for rule in rules if (not rule.effective_to or getdate(rule.effective_to) >= on_date) and (not rule.hs_code_pattern or (hs_code or "").startswith(rule.hs_code_pattern.rstrip("*")))]
