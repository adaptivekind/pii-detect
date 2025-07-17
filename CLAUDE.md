# PII Detection CLI Project

## Overview
This project provides a Python CLI tool for detecting personally identifiable information (PII) in text files using Microsoft Presidio.

## Setup
To set up the project dependencies:
```bash
./setup.sh
```

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
- **Multi-version testing**: Python 3.9, 3.10, 3.11, 3.12
- **Code quality**: Black formatting, flake8 linting, isort import sorting
- **Security scanning**: Bandit for vulnerabilities, safety for dependencies
- **Test coverage**: pytest with coverage reporting to Codecov
- **Pre-commit hooks**: Automated code quality enforcement

## Dependencies
- Requires Python 3.9+
- Uses spaCy en_core_web_lg model for NLP
- Built on Microsoft Presidio for PII detection
