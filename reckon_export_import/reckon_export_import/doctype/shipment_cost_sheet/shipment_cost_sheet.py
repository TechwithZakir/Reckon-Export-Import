import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ShipmentCostSheet(Document):
	def validate(self):
		self.estimated_total = sum(flt(row.estimated_amount) for row in self.costs)
		self.actual_total = sum(flt(row.actual_amount) for row in self.costs)
		self.variance = self.actual_total - self.estimated_total


@frappe.whitelist()
def create_landed_cost_voucher(source_name: str):
	source = frappe.get_doc("Shipment Cost Sheet", source_name)
	source.check_permission("write")
	if source.shipment_type != "Import Shipment":
		frappe.throw(_("Landed Cost Vouchers are only available for import shipments."))
	if source.landed_cost_voucher:
		return source.landed_cost_voucher

	receipts = frappe.get_all(
		"Trade Shipment Reference",
		filters={
			"parent": source.shipment,
			"parenttype": "Import Shipment",
			"reference_doctype": "Purchase Receipt",
		},
		pluck="reference_name",
	)
	if not receipts:
		frappe.throw(_("Link at least one Purchase Receipt to the Import Shipment first."))

	lcv = frappe.new_doc("Landed Cost Voucher")
	lcv.company = source.company
	lcv.posting_date = source.posting_date
	for receipt in receipts:
		lcv.append("purchase_receipts", {
			"receipt_document_type": "Purchase Receipt",
			"receipt_document": receipt,
		})
	for row in source.costs:
		if flt(row.actual_amount) and not row.is_recoverable:
			if not row.expense_account:
				frappe.throw(_("Row {0}: Expense Account is required for landed cost.").format(row.idx))
			lcv.append("taxes", {
				"expense_account": row.expense_account,
				"description": row.cost_type,
				"amount": row.actual_amount,
			})
	lcv.insert()
	source.db_set("landed_cost_voucher", lcv.name)
	return lcv.name

