import json
import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()

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

    required_fields = {"severity", "line", "title", "description"}

    for finding in result["findings"]:
        if not isinstance(finding, dict):
            raise ValueError("Each finding must be a JSON object.")

    for finding in result["findings"]:
        if not required_fields.issubset(finding):
            raise ValueError(
                "Each finding must contain severity, line, title, and description."
            )

    return result


def review_code_with_client(
    code: str,
    language: str,
    client: Any,
    model: str,
) -> dict[str, Any]:
    """Review code using an injected AI client."""
    validated_code = validate_code(code)

    if not isinstance(language, str) or not language.strip():
        raise ValueError("Please select a programming language.")

    if not isinstance(model, str) or not model.strip():
        raise ValueError("Please configure an AI model.")

    prompt = f"""
You are a careful software code reviewer.

Review the following {language.strip()} code for potential bugs,
security risks, readability problems, and maintainability issues.

Only report issues supported by the code. Do not invent problems.
If no issues are found, return an empty findings list.
Line numbers should refer to the submitted code.

Return only a valid JSON object in this format:
{{
  "summary": "Short review summary",
  "findings": [
    {{
      "severity": "low, medium, or high",
      "line": 1,
      "title": "Short issue title",
      "description": "Explain the issue and how to improve it."
    }}
  ]
}}

Code to review:
```{language.strip()}
{validated_code}
```
"""

    response = client.responses.create(
        model=model.strip(),
        input=prompt,
    )

    return parse_review_response(response.output_text)


def review_code(code: str, language: str) -> dict[str, Any]:
    """Review code when configured, or use prototype mode without an API key."""
    validated_code = validate_code(code)

    if not isinstance(language, str) or not language.strip():
        raise ValueError("Please select a programming language.")

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key:
        return {
            "summary": (
                f"Code submitted successfully for {language.strip()} review. "
                "AI-powered analysis is not connected because no API key is configured."
            ),
            "findings": [],
            "code_length": len(validated_code),
        }

    if not model:
        raise ValueError(
            "Please configure OPENAI_MODEL in your .env file."
        )

    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    result = review_code_with_client(
        code=validated_code,
        language=language,
        client=client,
        model=model,
    )

    result["code_length"] = len(validated_code)
    return result