def normalize_input(text: str) -> str:
    text = text.lower().strip()
    text = " ".join(text.split())
    return text


def detect_structure(text: str) -> str:
    if " but for " in text:
        return "analogy"

    if " for " in text:
        return "solution_for_audience"

    if text.startswith("why ") or " why " in text:
        return "problem_exploration"

    return "general"


def generate_queries(user_input: str) -> list[str]:
    text = normalize_input(user_input)
    structure = detect_structure(text)

    queries = []

    if structure == "solution_for_audience":
        queries.extend([
            f"best {text}",
            f"{text} problems",
            f"{text} examples",
        ])

    elif structure == "problem_exploration":
        queries.extend([
            text,
            f"{text} solutions",
            f"{text} examples",
        ])

    elif structure == "analogy":
        queries.extend([
            text.replace(" but for ", " for "),
            f"{text} examples",
            f"{text} alternatives",
        ])

    else:
        queries.extend([
            text,
            f"{text} problems",
            f"{text} examples",
        ])

    # Deduplicate + limit
    return list(dict.fromkeys(queries))[:3]
