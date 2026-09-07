from decimal import Decimal

from src.invoice_service import MediaOrder, invoice_html


def test_invoice_html_shows_creator_delivery_total() -> None:
    order = MediaOrder("ord-1", "Ava Chen", "Cardiology lecture", 30, Decimal("2.00"))
    html = invoice_html(order)
    assert "Creator: Ava Chen" in html
    assert "Streaming minutes: 30" in html
    assert "Total: $60.00" in html
