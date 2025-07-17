"""
Unit tests for PIIDetector class
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), "..", "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from detector import PIIDetector
except ImportError:
    # Additional fallback for editors
    import importlib.util

    detector_path = Path(__file__).parent.parent / "src" / "detector.py"
    spec = importlib.util.spec_from_file_location("detector", detector_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load detector module from {detector_path}")
    detector_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(detector_module)
    PIIDetector = detector_module.PIIDetector


class TestPIIDetector(unittest.TestCase):
    """Test cases for PIIDetector class"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock the presidio imports to avoid dependency issues in tests
        self.presidio_patcher = patch.dict(
            "sys.modules",
            {"presidio_analyzer": Mock(), "presidio_analyzer.nlp_engine": Mock()},
        )
        self.presidio_patcher.start()

    def tearDown(self):
        """Clean up after tests"""
        self.presidio_patcher.stop()

    @patch("detector.AnalyzerEngine")
    @patch("detector.NlpEngineProvider")
    def test_init_success(self, mock_provider, mock_analyzer):
        """Test successful initialization of PIIDetector"""
        # Mock the provider and analyzer
        mock_nlp_engine = Mock()
        mock_provider_instance = Mock()
        mock_provider_instance.create_engine.return_value = mock_nlp_engine
        mock_provider.return_value = mock_provider_instance

        mock_analyzer_instance = Mock()
        mock_analyzer.return_value = mock_analyzer_instance

        # Create detector
        detector = PIIDetector()

        # Verify initialization
        self.assertIsNotNone(detector.analyzer)
        mock_provider.assert_called_once()
        mock_analyzer.assert_called_once_with(nlp_engine=mock_nlp_engine)

    @patch("detector.AnalyzerEngine")
    @patch("detector.NlpEngineProvider")
    def test_analyze_text_success(self, mock_provider, mock_analyzer):
        """Test successful text analysis"""
        # Mock setup
        mock_nlp_engine = Mock()
        mock_provider_instance = Mock()
        mock_provider_instance.create_engine.return_value = mock_nlp_engine
        mock_provider.return_value = mock_provider_instance

        # Mock analyzer result
        mock_result = Mock()
        mock_result.entity_type = "PERSON"
        mock_result.start = 0
        mock_result.end = 8
        mock_result.score = 0.85

        mock_analyzer_instance = Mock()
        mock_analyzer_instance.analyze.return_value = [mock_result]
        mock_analyzer.return_value = mock_analyzer_instance

        # Create detector and analyze text
        detector = PIIDetector()
        text = "John Doe"
        results = detector.analyze_text(text)

        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["entity_type"], "PERSON")
        self.assertEqual(results[0]["text"], "John Doe")
        self.assertEqual(results[0]["score"], 0.85)

    @patch("detector.AnalyzerEngine")
    @patch("detector.NlpEngineProvider")
    def test_analyze_text_empty_result(self, mock_provider, mock_analyzer):
        """Test text analysis with no PII found"""
        # Mock setup
        mock_nlp_engine = Mock()
        mock_provider_instance = Mock()
        mock_provider_instance.create_engine.return_value = mock_nlp_engine
        mock_provider.return_value = mock_provider_instance

        mock_analyzer_instance = Mock()
        mock_analyzer_instance.analyze.return_value = []
        mock_analyzer.return_value = mock_analyzer_instance

        # Create detector and analyze text
        detector = PIIDetector()
        results = detector.analyze_text("No PII here")

        # Verify empty results
        self.assertEqual(len(results), 0)

    @patch("detector.AnalyzerEngine")
    @patch("detector.NlpEngineProvider")
    @patch("builtins.open", new_callable=mock_open, read_data="John Doe")
    def test_analyze_file_success(self, _, mock_provider, mock_analyzer):
        """Test successful file analysis"""
        # Mock setup
        mock_nlp_engine = Mock()
        mock_provider_instance = Mock()
        mock_provider_instance.create_engine.return_value = mock_nlp_engine
        mock_provider.return_value = mock_provider_instance

        # Mock analyzer result
        mock_result = Mock()
        mock_result.entity_type = "PERSON"
        mock_result.start = 0
        mock_result.end = 8
        mock_result.score = 0.85

        mock_analyzer_instance = Mock()
        mock_analyzer_instance.analyze.return_value = [mock_result]
        mock_analyzer.return_value = mock_analyzer_instance

        # Create detector and analyze file
        detector = PIIDetector()
        file_path = Path("/fake/path/test.txt")
        result = detector.analyze_file(file_path)

        # Verify results
        self.assertTrue(result["pii_found"])
        self.assertEqual(result["pii_count"], 1)
        self.assertEqual(result["file"], str(file_path))
        self.assertEqual(len(result["entities"]), 1)

    @patch("detector.AnalyzerEngine")
    @patch("detector.NlpEngineProvider")
    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_analyze_file_error(self, _, mock_provider, mock_analyzer):
        """Test file analysis with file error"""
        # Mock setup
        mock_nlp_engine = Mock()
        mock_provider_instance = Mock()
        mock_provider_instance.create_engine.return_value = mock_nlp_engine
        mock_provider.return_value = mock_provider_instance

        mock_analyzer_instance = Mock()
        mock_analyzer.return_value = mock_analyzer_instance

        # Create detector and analyze file
        detector = PIIDetector()
        file_path = Path("/fake/path/nonexistent.txt")
        result = detector.analyze_file(file_path)

        # Verify error handling
        self.assertFalse(result["pii_found"])
        self.assertEqual(result["pii_count"], 0)
        self.assertIn("error", result)
        self.assertEqual(result["file"], str(file_path))

    @patch("detector.AnalyzerEngine")
    @patch("detector.NlpEngineProvider")
    def test_analyze_directory(self, mock_provider, mock_analyzer):
        """Test directory analysis"""
        # Mock setup
        mock_nlp_engine = Mock()
        mock_provider_instance = Mock()
        mock_provider_instance.create_engine.return_value = mock_nlp_engine
        mock_provider.return_value = mock_provider_instance

        mock_analyzer_instance = Mock()
        mock_analyzer_instance.analyze.return_value = []
        mock_analyzer.return_value = mock_analyzer_instance

        # Create detector
        detector = PIIDetector()

        # Mock directory with files
        mock_directory = Mock()
        mock_file1 = Mock()
        mock_file1.is_file.return_value = True
        mock_file1.suffix = ".txt"
        mock_file1.__str__ = lambda: "/fake/file1.txt"

        mock_file2 = Mock()
        mock_file2.is_file.return_value = True
        mock_file2.suffix = ".py"
        mock_file2.__str__ = lambda: "/fake/file2.py"

        mock_directory.rglob.return_value = [mock_file1, mock_file2]

        # Mock the analyze_file method to avoid file I/O
        with patch.object(detector, "analyze_file") as mock_analyze_file:
            mock_analyze_file.return_value = {
                "file": "test.txt",
                "pii_found": False,
                "pii_count": 0,
                "entities": [],
            }

            results = detector.analyze_directory(mock_directory)

            # Verify results
            self.assertEqual(len(results), 2)
            self.assertEqual(mock_analyze_file.call_count, 2)


if __name__ == "__main__":
    unittest.main()
