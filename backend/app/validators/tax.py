def is_gst_calculation_correct(
    taxable_amount: float | None,
    cgst: float | None,
    sgst: float | None,
    igst: float | None,
    grand_total: float | None,
    tolerance: float = 2.0,
) -> bool:
    if taxable_amount is None or grand_total is None:
        return False

    cgst_val = cgst or 0.0
    sgst_val = sgst or 0.0
    igst_val = igst or 0.0
    expected = taxable_amount + cgst_val + sgst_val + igst_val
    return abs(expected - grand_total) <= tolerance
