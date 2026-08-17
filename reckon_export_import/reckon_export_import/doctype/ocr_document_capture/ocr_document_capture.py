import hashlib

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class OCRDocumentCapture(Document):
	def validate(self):
		if self.source_file and not self.file_hash:
			content = _get_private_file_content(self.source_file)
			self.file_hash = hashlib.sha256(content).hexdigest()
		if self.status == "Approved" and not self.reviewed_by:
			self.reviewed_by, self.reviewed_on = frappe.session.user, now_datetime()
		if self.status == "Approved" and not self.extracted_data:
			frappe.throw(_("Extracted Data is required before approval."))


def _get_private_file_content(file_url):
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	content = file_doc.get_content()
	return content.encode() if isinstance(content, str) else content


@frappe.whitelist()
def queue_extraction(capture):
	doc = frappe.get_doc("OCR Document Capture", capture)
	doc.check_permission("write")
	providers = frappe.get_hooks("reckon_export_import_ocr_provider")
	if not providers:
		frappe.throw(_("No OCR provider is configured. Add reckon_export_import_ocr_provider to site hooks."))
	doc.db_set("status", "Queued")
	frappe.enqueue(
		"reckon_export_import.reckon_export_import.doctype.ocr_document_capture.ocr_document_capture.run_extraction",
		capture=doc.name,
		provider_path=providers[0],
		enqueue_after_commit=True,
	)


def run_extraction(capture, provider_path):
	from reckon_export_import.integrations import get_provider

	doc = frappe.get_doc("OCR Document Capture", capture)
	doc.db_set("status", "Processing")
	try:
		result = get_provider(provider_path).extract(_get_private_file_content(doc.source_file), doc.document_type)
		doc.db_set({
			"provider": result.get("provider"), "provider_version": result.get("version"),
			"confidence": result.get("confidence"), "extracted_data": frappe.as_json(result.get("extracted_data") or {}),
			"validation_messages": result.get("findings"), "status": "Needs Review",
		})
	except Exception:
		doc.db_set("status", "Failed")
		frappe.log_error(title=f"OCR capture failed: {doc.name}")
		raise
