from app.services.correction_service import apply_ai_corrections


def test_ai_corrections_compute_total() -> None:
    data = {
        "taxable_amount": "1000",
        "cgst": "90",
        "sgst": "90",
        "igst": None,
        "grand_total": None,
    }
    corrected, notes = apply_ai_corrections(data)
    assert corrected["grand_total"] == 1180
    assert notes is not None
