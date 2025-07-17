#!/bin/bash
# Setup script for PII Detection CLI

echo "Setting up PII Detection CLI..."

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_lg

echo "Setup complete!"
echo ""
echo "To use the CLI:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the CLI: python src/pii_detect.py <file_or_directory>"
echo ""
echo "Examples:"
echo "  python src/pii_detect.py sample_text.txt"
echo "  python src/pii_detect.py /path/to/directory"
echo "  python src/pii_detect.py -f json sample_text.txt"
