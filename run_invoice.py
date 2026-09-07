import json
from decimal import Decimal

from src.invoice_service import InfraiPdfClient, MediaOrder, create_invoice


def main() -> None:
    order = MediaOrder("ord-1042", "Dr. Lin", "Sleep study stream", 42, Decimal("1.25"))
    result = create_invoice(order, InfraiPdfClient())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
