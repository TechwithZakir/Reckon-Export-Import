"""Provider-neutral Phase 2 integration contracts.

Real providers belong in separate adapter modules and must use authorized APIs,
webhooks, EDI/SFTP, or institution-approved file exchange.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import frappe


class TradeProvider(ABC):
	@abstractmethod
	def pull_updates(self, reference: str) -> list[dict]: ...

	@abstractmethod
	def health(self) -> dict: ...


class BankProvider(TradeProvider):
	@abstractmethod
	def get_lc_updates(self, lc_number: str) -> list[dict]: ...


class CarrierProvider(TradeProvider):
	@abstractmethod
	def get_tracking_events(self, reference: str) -> list[dict]: ...


class OCRProvider(ABC):
	@abstractmethod
	def extract(self, content: bytes, document_type: str) -> dict:
		"""Return provider, version, confidence, extracted_data, and findings."""
		...


def get_provider(path: str, settings=None):
	provider_class = frappe.get_attr(path)
	return provider_class(settings=settings)
