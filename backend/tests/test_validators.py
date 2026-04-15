from app.validators.gst import is_valid_gstin
from app.validators.tax import is_gst_calculation_correct


def test_valid_gstin() -> None:
    assert is_valid_gstin("27AABCA1234B1Z5")
    assert not is_valid_gstin("INVALIDGSTIN")


def test_tax_calculation() -> None:
    assert is_gst_calculation_correct(1000, 90, 90, 0, 1180)
    assert not is_gst_calculation_correct(1000, 90, 90, 0, 1200)
