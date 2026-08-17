import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, date_diff, flt, getdate


class DemurrageTariff(Document):
	def validate(self):
		if self.effective_to and self.effective_to < self.effective_from:
			frappe.throw(_("Effective To cannot be before Effective From."))
		previous_end = 0
		ordered = sorted(self.tiers, key=lambda tier: tier.from_day)
		for index, row in enumerate(ordered):
			if row.from_day != previous_end + 1:
				frappe.throw(_("Tariff tiers must be continuous and start on day 1."))
			if not row.to_day and index != len(ordered) - 1:
				frappe.throw(_("Only the final tariff tier may have an open end day."))
			if row.to_day and row.to_day < row.from_day:
				frappe.throw(_("Tier end day cannot be before its start day."))
			previous_end = row.to_day or previous_end


@frappe.whitelist()
def calculate_charge(tariff, start_date, end_date, extra_free_days=0):
	doc = frappe.get_doc("Demurrage Tariff", tariff)
	doc.check_permission("read")
	start, end = getdate(start_date), getdate(end_date)
	elapsed = max(date_diff(end, start), 0)
	if doc.day_basis == "Working Days":
		elapsed = sum(1 for offset in range(1, elapsed + 1) if add_days(start, offset).weekday() < 5)
	chargeable = max(elapsed - int(doc.free_days or 0) - int(extra_free_days or 0), 0)
	total, breakdown = 0, []
	for row in sorted(doc.tiers, key=lambda tier: tier.from_day):
		upper = row.to_day or chargeable
		days = max(min(chargeable, upper) - row.from_day + 1, 0)
		amount = days * flt(row.daily_rate)
		if days:
			breakdown.append({"from_day": row.from_day, "to_day": upper, "days": days, "daily_rate": row.daily_rate, "amount": amount})
		total += amount
	return {"elapsed_days": elapsed, "free_days": int(doc.free_days or 0) + int(extra_free_days or 0), "chargeable_days": chargeable, "currency": doc.currency, "amount": total, "breakdown": breakdown}
