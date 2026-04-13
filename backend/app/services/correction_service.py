def apply_ai_corrections(data: dict) -> tuple[dict, str | None]:
    notes: list[str] = []

    for key in ["taxable_amount", "cgst", "sgst", "igst", "grand_total"]:
        val = data.get(key)
        if isinstance(val, str):
            try:
                data[key] = float(val.replace(",", "").strip())
                notes.append(f"Normalized {key}")
            except ValueError:
                data[key] = None

    # Correction heuristic: if IGST missing but CGST and SGST present, keep as intra-state.
    if data.get("igst") is None and data.get("cgst") and data.get("sgst"):
        notes.append("Assumed intra-state tax (CGST+SGST)")

    # If grand total missing but components exist, compute it.
    if data.get("grand_total") is None and data.get("taxable_amount") is not None:
        data["grand_total"] = (
            data.get("taxable_amount", 0)
            + data.get("cgst", 0)
            + data.get("sgst", 0)
            + data.get("igst", 0)
        )
        notes.append("Computed missing grand total")

    return data, "; ".join(notes) if notes else None
