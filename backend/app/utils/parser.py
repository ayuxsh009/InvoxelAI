import re
from datetime import date

from dateutil import parser as date_parser

GSTIN_PATTERN = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b")
INVOICE_NO_PATTERN = re.compile(
    r"(?:invoice\s*(?:no|number|#)\s*[:\-]?\s*)([A-Z0-9][A-Z0-9\-/]*)", re.I
)
HSN_PATTERN = re.compile(r"\b\d{4,8}\b")
AMOUNT_PATTERN = re.compile(r"\b([0-9][0-9,]*(?:\.[0-9]{1,3})?)\b")
GEM_INVOICE_NO_PATTERN = re.compile(r"\bGeM\s+Invoice\s+No\s*:\s*([A-Z0-9\-/]+)", re.I)
GEM_INVOICE_DATE_PATTERN = re.compile(r"\bGeM\s+Invoice\s+Date\s*:\s*([A-Za-z0-9\-\/]+)", re.I)


def parse_date(text: str) -> date | None:
    try:
        dt = date_parser.parse(text, dayfirst=True, fuzzy=True)
        return dt.date()
    except (ValueError, TypeError, OverflowError):
        return None


def _extract_amount_after_keyword(lines: list[str], keyword: str) -> float | None:
    keyword_lc = keyword.lower()
    for line in lines:
        if keyword_lc in line.lower():
            amounts = AMOUNT_PATTERN.findall(line)
            if amounts:
                return float(amounts[-1].replace(",", ""))
    return None


def _extract_vendor_name(lines: list[str], raw_text: str) -> str | None:
    match = re.search(r"Address:\s*(.*?)\s+GeM\s+Invoice\s+No", raw_text, re.I)
    if match:
        vendor = match.group(1).strip(" -:")
        if vendor:
            return vendor

    for idx, line in enumerate(lines):
        if "service provider details" in line.lower():
            for sub in lines[idx + 1 : idx + 6]:
                if sub.lower().startswith("address:"):
                    candidate = sub.split(":", 1)[1].strip()
                    candidate = re.sub(r"\s+GeM\s+Invoice\s+No.*$", "", candidate, flags=re.I).strip()
                    if candidate:
                        return candidate

    blacklist = {
        "invoice",
        "bill to:",
        "service delivered to:",
        "service provider details:",
    }
    for line in lines:
        if line.lower() not in blacklist and len(line) > 3:
            return line
    return None


def _extract_invoice_number(lines: list[str], raw_text: str) -> str | None:
    gem_match = GEM_INVOICE_NO_PATTERN.search(raw_text)
    if gem_match:
        return gem_match.group(1).strip()

    for idx, line in enumerate(lines):
        if "service provider gst tax invoice number" in line.lower() and idx + 1 < len(lines):
            next_line = lines[idx + 1]
            tokens = next_line.split()
            if tokens:
                return tokens[0].strip()

    for line in lines:
        match = INVOICE_NO_PATTERN.search(line)
        if match:
            return match.group(1).strip()
    return None


def _extract_invoice_date(lines: list[str], raw_text: str) -> date | None:
    gem_date_match = GEM_INVOICE_DATE_PATTERN.search(raw_text)
    if gem_date_match:
        parsed = parse_date(gem_date_match.group(1))
        if parsed:
            return parsed

    for idx, line in enumerate(lines):
        if "service provider gst tax invoice number" in line.lower() and idx + 1 < len(lines):
            next_line = lines[idx + 1]
            tokens = next_line.split()
            if len(tokens) >= 2:
                parsed = parse_date(tokens[1])
                if parsed:
                    return parsed

    for line in lines:
        if "invoice date" in line.lower() or line.lower().startswith("date"):
            parsed = parse_date(line)
            if parsed:
                return parsed
    return None


def _extract_hsn_sac_codes(lines: list[str], raw_text: str) -> str | None:
    code_candidates: list[str] = []

    for idx, line in enumerate(lines):
        lower = line.lower()
        if "sac code" in lower or "hsn code" in lower:
            nums = HSN_PATTERN.findall(line)
            if nums:
                code_candidates.extend(nums)
            elif idx + 1 < len(lines):
                next_nums = HSN_PATTERN.findall(lines[idx + 1])
                if next_nums:
                    # Service description rows often contain quantities and codes together;
                    # prefer longer code-like tokens first (e.g. SAC 996601 over 3000 km).
                    next_nums = sorted(next_nums, key=len, reverse=True)
                    code_candidates.append(next_nums[0])

    if not code_candidates:
        direct = re.findall(r"\b(?:SAC|HSN)\s*Code\b.*?(\d{4,8})", raw_text, flags=re.I)
        code_candidates.extend(direct)

    code_candidates = sorted(set(code_candidates))
    return ", ".join(code_candidates[:10]) if code_candidates else None


def parse_invoice_fields(raw_text: str) -> dict:
    lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
    upper_text = raw_text.upper()

    gstin_match = GSTIN_PATTERN.search(upper_text)
    vendor_name = _extract_vendor_name(lines, raw_text)
    invoice_number = _extract_invoice_number(lines, raw_text)
    invoice_date = _extract_invoice_date(lines, raw_text)
    hsn_sac_codes = _extract_hsn_sac_codes(lines, raw_text)

    taxable_amount = _extract_amount_after_keyword(lines, "taxable amount")
    cgst = _extract_amount_after_keyword(lines, "cgst")
    sgst = _extract_amount_after_keyword(lines, "sgst")
    if sgst is None:
        sgst = _extract_amount_after_keyword(lines, "sgst/utgst")
    igst = _extract_amount_after_keyword(lines, "igst")

    grand_total = _extract_amount_after_keyword(lines, "grand total")
    if grand_total is None:
        grand_total = _extract_amount_after_keyword(lines, "total price inclusive all taxes")
    if grand_total is None:
        grand_total = _extract_amount_after_keyword(lines, "total")

    return {
        "vendor_name": vendor_name,
        "gstin": gstin_match.group(0) if gstin_match else None,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "hsn_sac_codes": hsn_sac_codes,
        "taxable_amount": taxable_amount,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "grand_total": grand_total,
    }
