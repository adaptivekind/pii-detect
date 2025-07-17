# PII Detection CLI Project

## Overview

This project provides a Python CLI tool for detecting personally identifiable information (PII) in text files using Microsoft Presidio.

## Universal Directives

1. you MUST write code that is clear and explains meaning - prefer readability
   over condensed code.
2. you MUST test and lint before declaring done.
3. you MUST handle errors explicitly.
4. you MUST code in a way that matches the style of the existing code.
5. you MUST code in a way that makes it easier for future coders.
6. you MUST focus on the task at hand, do not make changes that do not help
   towards this goal.
7. you SHOULD ensure a test exists that describes the intended behaviour, before
   writing the code that delivers that behaviour. Once the test is passes you
   should refactor the implementation to ensure the universal directives are met.

## Testing & Validation

### Automated Tests

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test files
pytest tests/test_detector.py
pytest tests/test_cli.py
```

### Manual Testing

To test the CLI after making changes:

```bash
# Test with sample file
python src/pii_detect.py sample_text.txt

# Test directory scanning
python src/pii_detect.py .

# Test JSON output
python src/pii_detect.py -f json sample_text.txt
```

## Code Structure

- `src/pii_detect.py` - Main CLI application with argument parsing and output formatting
- `src/detector.py` - PIIDetector class that wraps Presidio functionality
- `tests/test_detector.py` - Unit tests for PIIDetector class
- `tests/test_cli.py` - Integration tests for CLI functionality
- `.github/workflows/ci.yml` - GitHub Actions CI/CD pipeline
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `requirements.txt` - Python dependencies (presidio-analyzer, presidio-anonymizer, spacy)
- `pytest.ini` - Pytest configuration with coverage settings
- `setup.sh` - Installation script that installs deps and downloads spaCy model
- `sample_text.txt` - Test file containing various PII types

## Key Components

- **PIIDetector class**: Wraps Presidio analyzer with spaCy NLP engine
- **File analysis**: Single file and directory scanning capabilities
- **Output formats**: Text (default) and JSON
- **File filtering**: Configurable extensions (.txt, .md, .py, .js, .json, .csv, .log)

## CI/CD Pipeline

The project uses GitHub Actions for automated testing and quality checks:

- **Version testing**: Python 3.13
- **Code quality**: Black formatting, flake8 linting, isort import sorting
- **Security scanning**: Bandit for vulnerabilities, safety for dependencies
- **Test coverage**: pytest with coverage reporting to Codecov
- **Pre-commit hooks**: Automated code quality enforcement

## Dependencies

- Requires Python 3.13+
- Uses spaCy en_core_web_lg model for NLP
- Built on Microsoft Presidio for PII detection
