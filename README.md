# PII Detection CLI

[![CI](https://github.com/yourusername/pii-detect/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/pii-detect/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/yourusername/pii-detect/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/pii-detect)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python command-line tool for detecting personally identifiable information (PII) in text files using Microsoft Presidio.

## Features

- Detect PII in single files or entire directories
- Support for multiple file formats (.txt, .md, .py, .js, .json, .csv, .log)
- JSON and text output formats
- Configurable file extensions
- Detailed PII entity reporting with confidence scores

## Installation

### Install as a System Command

Install the package globally to use `pii-detect` command from anywhere:

```bash
pip install -e .
```

After installation, you can use the `pii-detect` command directly:

```bash
pii-detect --help
```

### Install Dependencies Only

If you prefer to run the script directly without installing:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

After installation, use the `pii-detect` command:

```bash
# Analyze a single file
pii-detect sample_text.txt

# Analyze all files in a directory
pii-detect /path/to/directory

# Output results as JSON
pii-detect -f json sample_text.txt

# Analyze only specific file types
pii-detect -e .py -e .js /path/to/directory
```

Or run the Python module directly:

```bash
# Analyze a single file
python src/pii_detect.py sample_text.txt

# Analyze all files in a directory
python src/pii_detect.py /path/to/directory

# Output results as JSON
python src/pii_detect.py -f json sample_text.txt

# Analyze only specific file types
python src/pii_detect.py -e .py -e .js /path/to/directory
```

### Command Line Options

- `path`: Path to file or directory to analyze
- `-f, --format`: Output format (text or json)
- `-e, --extensions`: File extensions to analyze (can be used multiple times)

## Detected PII Types

The tool can detect various types of PII including:

- Names (PERSON)
- Email addresses (EMAIL_ADDRESS)
- Phone numbers (PHONE_NUMBER)
- Social Security Numbers (US_SSN)
- Credit card numbers (CREDIT_CARD)
- IP addresses (IP_ADDRESS)
- URLs (URL)
- Locations (LOCATION)
- And more...

## Example Output

```
=== PII Detection Results ===
Files analyzed: 1
Files with PII: 1
Total PII entities found: 8
==============================

🔍 sample_text.txt - 8 PII entities found:
  • PERSON: 'John Doe' (confidence: 0.85)
  • EMAIL_ADDRESS: 'john.doe@email.com' (confidence: 1.00)
  • PHONE_NUMBER: '(555) 123-4567' (confidence: 0.75)
  • US_SSN: '123-45-6789' (confidence: 0.80)
  • CREDIT_CARD: '4532-1234-5678-9012' (confidence: 1.00)
  • LOCATION: 'New York City' (confidence: 0.85)
  • LOCATION: 'Redmond, WA' (confidence: 0.85)
  • US_BANK_NUMBER: '9876543210' (confidence: 0.70)
```

## Requirements

- Python 3.9+
- presidio-analyzer
- presidio-anonymizer
- spacy (with en_core_web_lg model)

## Development

### Setup for Development

1. Clone the repository and set up the environment:

```bash
pip install -r requirements.txt
```

2. Install development dependencies:

```bash
pip install pytest pytest-cov black flake8 isort bandit safety pre-commit
```

3. Set up pre-commit hooks:

```bash
pre-commit install
```

### Code Quality

This project uses:

- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting
- **Bandit** for security vulnerability scanning
- **Safety** for dependency vulnerability checking
- **Pre-commit hooks** for automated code quality checks

Run code formatting:

```bash
black src/
```

Run import sorting:

```bash
isort src/
```

Run linting:

```bash
flake8 src/
```

Run security scanning:

```bash
bandit -r src/
```

Check for vulnerable dependencies:

```bash
safety check
```

### Testing

#### Running Tests

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_detector.py
pytest tests/test_cli.py
```

Run with verbose output:

```bash
pytest -v
```

#### Manual Testing

Test the CLI with the sample file:

```bash
pii-detect sample_text.txt
# or
python src/pii_detect.py sample_text.txt
```

Test directory scanning:

```bash
pii-detect .
# or
python src/pii_detect.py .
```

Test JSON output:

```bash
pii-detect -f json sample_text.txt
# or
python src/pii_detect.py -f json sample_text.txt
```

Test with specific extensions:

```bash
pii-detect -e .py -e .md .
# or
python src/pii_detect.py -e .py -e .md .
```

### Contributing

1. Make your changes
2. Run tests to ensure functionality works: `pytest`
3. Ensure code passes pre-commit checks
4. Test with sample files manually
5. Submit a pull request

#### Test Coverage

The project aims for 80% test coverage. Current test files:

- `tests/test_detector.py` - Unit tests for PIIDetector class
- `tests/test_cli.py` - Integration tests for CLI functionality

To check coverage:

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment:

### Automated Checks

- **Testing**: Runs on Python 3.9, 3.10, 3.11, and 3.12
- **Linting**: Code style checks with flake8 and black
- **Security**: Vulnerability scanning with bandit and safety
- **Coverage**: Code coverage reporting with pytest-cov and Codecov
- **Pre-commit**: Automated code formatting and quality checks

### Workflow Triggers

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### Local Pre-commit Setup

Enable pre-commit hooks locally:

```bash
pre-commit install
```

Run pre-commit on all files:

```bash
pre-commit run --all-files
```

## Security Note

⚠️ **Important**: Presidio can help identify sensitive/PII data in your text, but there is no guarantee that it will find all sensitive information. Always review results and consider additional security measures for sensitive data handling.
