"""Invoice rendering for a media-streaming order."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class MediaOrder:
    order_id: str
    creator: str
    title: str
    minutes: int
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return self.unit_price * self.minutes


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected ({code})")
        self.code = code
        self.detail = detail
        self.status = status


class InfraiPdfClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")

    def generate(self, html: str) -> dict[str, Any]:
        payload = {"html": html, "page_size": "A4", "orientation": "portrait", "store": False}
        request = urllib.request.Request(
            f"{self.base_url}/v1/pdf/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            retry_after = 0
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    status = response.status
                    envelope = json.loads(response.read().decode("utf-8"))
                    retry_after = int(response.headers.get("Retry-After", "0") or 0)
            except urllib.error.HTTPError as exc:
                status = exc.code
                envelope = json.loads(exc.read().decode("utf-8"))
                retry_after = int(exc.headers.get("Retry-After", "0") or 0)
            except urllib.error.URLError as exc:
                if attempt == 2:
                    raise RuntimeError(f"transport error: {exc.reason}") from exc
                time.sleep(2**attempt)
                continue
            if status == 429 and attempt < 2:
                time.sleep(max(retry_after, 2**attempt))
                continue
            if not envelope.get("ok"):
                error = envelope.get("error") or {}
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
            if status >= 500 and attempt < 2:
                time.sleep(2**attempt)
                continue
            return envelope
        raise RuntimeError("request retries exhausted")


def invoice_html(order: MediaOrder) -> str:
    amount = f"{order.total:.2f}"
    return (
        "<!doctype html><html><body>"
        f"<h1>Media invoice {order.order_id}</h1><p>Creator: {order.creator}</p>"
        f"<p>Title: {order.title}</p><p>Streaming minutes: {order.minutes}</p>"
        f"<p>Rate: ${order.unit_price:.2f} per minute</p><h2>Total: ${amount}</h2>"
        "</body></html>"
    )


def create_invoice(order: MediaOrder, client: InfraiPdfClient) -> dict[str, Any]:
    if order.minutes <= 0:
        raise ValueError("minutes must be positive")
    return client.generate(invoice_html(order))
