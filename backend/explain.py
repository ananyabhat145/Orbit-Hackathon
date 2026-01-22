def explain_risk(total_risk, threats):
    if total_risk == 0:
        return "No significant conjunctions detected in the forecast window."

    lines = [
        f"Aggregate collision risk is elevated due to {len(threats)} close approaches."
    ]

    for t in threats:
        lines.append(
            f"• High relative orbital overlap with {t['name']} "
            f"(p ≈ {t['probability']:.3f})"
        )

    return " ".join(lines)

