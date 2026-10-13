import json
from typing import Any


MAX_CODE_LENGTH = 20_000


def validate_code(code: str) -> str:
    """Validate submitted source code."""
    if not isinstance(code, str):
        raise TypeError("Code must be a string.")

    code = code.strip()

    if not code:
        raise ValueError("Please enter some code to review.")

    if len(code) > MAX_CODE_LENGTH:
        raise ValueError(
            f"Code is too long. Maximum length is {MAX_CODE_LENGTH:,} characters."
        )

    return code


def parse_review_response(response: str) -> dict[str, Any]:
    """Parse and validate a JSON review response."""
    try:
        result = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError("The review response is not valid JSON.") from exc

    if not isinstance(result, dict):
        raise ValueError("The review response must be a JSON object.")

    if "summary" not in result or "findings" not in result:
        raise ValueError("The response must contain summary and findings.")

    if not isinstance(result["summary"], str):
        raise ValueError("The summary must be a string.")

    if not isinstance(result["findings"], list):
        raise ValueError("Findings must be a list.")

    for finding in result["findings"]:
        if not isinstance(finding, dict):
            raise ValueError("Each finding must be a JSON object.")

        required_fields = {"severity", "line", "title", "description"}
        if not required_fields.issubset(finding):
            raise ValueError(
                "Each finding must contain severity, line, title, and description."
            )

    return result


def review_code(code: str, language: str) -> dict[str, Any]:
    """Validate code and return a placeholder review for initial testing."""
    validated_code = validate_code(code)

    if not isinstance(language, str) or not language.strip():
        raise ValueError("Please select a programming language.")

    # Placeholder only: AI integration will be added in a later step.
    return {
        "summary": (
            f"Code submitted successfully for {language.strip()} review. "
            "AI-powered analysis has not been connected yet."
        ),
        "findings": [],
        "code_length": len(validated_code),
    }