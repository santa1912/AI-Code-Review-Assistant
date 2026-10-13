import json

import pytest

from reviewer import (
    MAX_CODE_LENGTH,
    parse_review_response,
    review_code,
    review_code_with_client,
    validate_code,
)


def test_validate_code_accepts_valid_code():
    assert validate_code("print('Hello')") == "print('Hello')"


def test_validate_code_rejects_empty_code():
    with pytest.raises(ValueError, match="enter some code"):
        validate_code("   ")


def test_validate_code_rejects_code_that_is_too_long():
    code = "x" * (MAX_CODE_LENGTH + 1)

    with pytest.raises(ValueError, match="too long"):
        validate_code(code)


def test_parse_review_response_accepts_valid_json():
    response = json.dumps(
        {
            "summary": "One potential issue found.",
            "findings": [
                {
                    "severity": "medium",
                    "line": 3,
                    "title": "Potential issue",
                    "description": "Review this section.",
                }
            ],
        }
    )

    result = parse_review_response(response)

    assert result["summary"] == "One potential issue found."
    assert len(result["findings"]) == 1


def test_parse_review_response_rejects_invalid_json():
    with pytest.raises(ValueError, match="valid JSON"):
        parse_review_response("not json")


def test_parse_review_response_rejects_missing_fields():
    response = json.dumps({"summary": "No findings provided."})

    with pytest.raises(ValueError, match="summary and findings"):
        parse_review_response(response)



def test_review_code_returns_placeholder():
    result = review_code("print('Hello')", "Python")

    assert "no API key is configured" in result["summary"]
    assert result["findings"] == []
    assert result["code_length"] == len("print('Hello')")

def test_review_code_rejects_missing_language():
    with pytest.raises(ValueError, match="select a programming language"):
        review_code("print('Hello')", "")


from unittest.mock import Mock


def test_review_code_with_client_returns_ai_findings():
    mock_client = Mock()
    mock_client.responses.create.return_value.output_text = """
    {
        "summary": "One potential issue found.",
        "findings": [
            {
                "severity": "medium",
                "line": 1,
                "title": "Potential issue",
                "description": "Review this code."
            }
        ]
    }
    """

    result = review_code_with_client(
        code="print('Hello')",
        language="Python",
        client=mock_client,
        model="test-model",
    )

    assert result["summary"] == "One potential issue found."
    assert len(result["findings"]) == 1
    assert result["findings"][0]["severity"] == "medium"
    mock_client.responses.create.assert_called_once()


def test_review_code_with_client_rejects_invalid_ai_response():
    mock_client = Mock()
    mock_client.responses.create.return_value.output_text = "not valid JSON"

    with pytest.raises(ValueError, match="valid JSON"):
        review_code_with_client(
            code="print('Hello')",
            language="Python",
            client=mock_client,
            model="test-model",
        )