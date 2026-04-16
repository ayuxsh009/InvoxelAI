from app.utils.parser import parse_invoice_fields


def test_parse_invoice_fields() -> None:
    text = """
    ABC Traders
    GSTIN: 27AABCA1234B1Z5
    Invoice No: INV-12
    Date: 12/04/2026
    Taxable Amount 1000.00
    CGST 90
    SGST 90
    Total 1180
    """
    parsed = parse_invoice_fields(text)
    assert parsed["vendor_name"] == "ABC Traders"
    assert parsed["gstin"] == "27AABCA1234B1Z5"
    assert parsed["invoice_number"] == "INV-12"
