import re

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")


def is_valid_gstin(gstin: str | None) -> bool:
    if not gstin:
        return False
    return bool(GSTIN_REGEX.match(gstin.strip().upper()))
