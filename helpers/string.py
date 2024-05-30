def remove_extra_whitespace(s: str) -> str:
    if s is None or s == "":
        return s
    return " ".join(s.split())
