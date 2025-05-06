def validate_xp_input(xp_raw: str):
    if not isinstance(xp_raw, str):
        return "Please enter your XP as a number (e.g., 4,000,000 or 4.000.000)."

    cleaned = xp_raw.replace(",", "").replace(".", "")
    if not cleaned.isdigit():
        return "Invalid XP format. Use digits with optional commas or dots."

    if int(cleaned) <= 0:
        return "XP must be greater than zero."

    return True


def parse_xp_input(xp_raw: str) -> int:
    return int(xp_raw.replace(",", "").replace(".", ""))


def format_number(n: float | int) -> str:
    return f"{int(n):,}"
