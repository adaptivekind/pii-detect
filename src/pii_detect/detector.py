"""
PII Detection module using Microsoft Presidio
Contains the PIIDetector class for analyzing text files for PII
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_analyzer.nlp_engine import NlpEngineProvider
except ImportError:
    print(
        "Error: Presidio packages not installed. Please run: pip "
        "install -r requirements.txt"
    )
    print("Then run: python -m spacy download en_core_web_lg")
    sys.exit(1)


class PIIDetector:
    def __init__(self):
        """Initialize the PII detector with Presidio analyzer"""
        try:
            # Create NLP engine configuration
            configuration = {
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
            }

            # Create NLP engine based on configuration
            provider = NlpEngineProvider(nlp_configuration=configuration)
            nlp_engine = provider.create_engine()

            # Initialize analyzer
            self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
        except Exception as e:
            print(f"Error initializing Presidio: {e}")
            print("Make sure you have installed the required packages and spaCy model:")
            print("pip install -r requirements.txt")
            print("python -m spacy download en_core_web_lg")
            sys.exit(1)

    def analyze_text(self, text: str) -> List[Dict[str, Any]]:
        """Analyze text for PII entities"""
        try:
            results = self.analyzer.analyze(text=text, language="en")
            return [
                {
                    "entity_type": result.entity_type,
                    "start": result.start,
                    "end": result.end,
                    "score": result.score,
                    "text": text[result.start : result.end],
                }
                for result in results
            ]
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return []

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for PII"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            results = self.analyze_text(content)

            return {
                "file": str(file_path),
                "pii_found": len(results) > 0,
                "pii_count": len(results),
                "entities": results,
            }
        except Exception as e:
            return {
                "file": str(file_path),
                "error": str(e),
                "pii_found": False,
                "pii_count": 0,
                "entities": [],
            }

    def analyze_directory(
        self,
        directory_path: Path,
        extensions: List[str] = [".txt", ".md", ".py", ".js", ".json", ".csv", ".log"],
    ) -> List[Dict[str, Any]]:
        """Analyze all text files in a directory for PII"""
        results = []

        for file_path in directory_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                result = self.analyze_file(file_path)
                results.append(result)

        return results
