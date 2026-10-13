# AI Code Review Assistant

A Python-based web application prototype for reviewing source code and presenting potential code quality findings.

## Features

- Submit source code for review through a Streamlit interface
- Validate code input and enforce a maximum input length
- Parse and validate structured JSON review responses
- Display review summaries and individual findings
- Prepare an injectable AI client interface for testable AI integration
- Unit tests using pytest and mocked AI responses

## Technology Stack

- Python
- Streamlit
- pytest
- OpenAI Python SDK
- python-dotenv

## Current Status

The application currently supports prototype mode without an API key. In this mode, it validates input and demonstrates the review interface but does not perform AI-powered code analysis.

The AI review function is prepared for integration with a compatible API model. Real AI review requires valid API configuration.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/santa1912/AI-Code-Review-Assistant.git
cd AI-Code-Review-Assistant
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the tests

```powershell
python -m pytest -v
```

### 5. Start the application

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Configuration

To enable AI-powered review, configure `OPENAI_API_KEY` and `OPENAI_MODEL` in a local `.env` file after selecting a model supported by the API.

Never commit API keys or other secrets to version control.

## Testing

The test suite covers input validation, JSON response validation, prototype behavior, and mocked AI response handling.

## Limitations

- AI-powered analysis requires API credentials and a supported model.
- Prototype mode does not identify actual bugs or security vulnerabilities.
- Review findings should be verified by a developer before acting on them.

## Future Improvements

- Improve AI error handling and response validation
- Add support for more programming languages
- Integrate code review into a Git workflow
- Add Docker support and automated CI testing
