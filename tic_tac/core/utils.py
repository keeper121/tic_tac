def color_text(text: str, color: str) -> str:
    """
    Colors the given text with the specified color.
    """
    color_codes = {
        "red": "\033[31m",
        "yellow": "\033[33m",
    }

    if color not in color_codes:
        raise ValueError("Invalid color")

    return f"{color_codes[color]}{text}\033[0m"
