"""
Integration tests for PII Detection CLI
"""

import json
import os
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import Mock, patch

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), "..", "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Mock presidio imports before importing our modules
with patch.dict(
    "sys.modules", {"presidio_analyzer": Mock(), "presidio_analyzer.nlp_engine": Mock()}
):
    import pii_detect.cli as pii_detect


class TestCLI(unittest.TestCase):
    """Test cases for CLI functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_file = os.path.join(self.temp_dir, "test.txt")

        # Create sample file with PII
        with open(self.sample_file, "w") as f:
            f.write("Hello, my name is John Doe and my email is john@example.com")

    def tearDown(self):
        """Clean up after tests"""
        import shutil

        shutil.rmtree(self.temp_dir)

    @patch("pii_detect.PIIDetector")
    def test_print_results_text_format(self, _):
        """Test text format output"""
        # Mock results
        results = [
            {
                "file": "test.txt",
                "pii_found": True,
                "pii_count": 2,
                "entities": [
                    {"entity_type": "PERSON", "text": "John Doe", "score": 0.85},
                    {
                        "entity_type": "EMAIL_ADDRESS",
                        "text": "john@example.com",
                        "score": 1.0,
                    },
                ],
            }
        ]

        # Capture output
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            pii_detect.print_results(results, "text")

        output = captured_output.getvalue()

        # Verify output contains expected elements
        self.assertIn("PII Detection Results", output)
        self.assertIn("Files analyzed: 1", output)
        self.assertIn("Files with PII: 1", output)
        self.assertIn("Total PII entities found: 2", output)
        self.assertIn("PERSON", output)
        self.assertIn("John Doe", output)
        self.assertIn("EMAIL_ADDRESS", output)
        self.assertIn("john@example.com", output)

    @patch("pii_detect.PIIDetector")
    def test_print_results_json_format(self, _):
        """Test JSON format output"""
        # Mock results
        results = [
            {
                "file": "test.txt",
                "pii_found": True,
                "pii_count": 1,
                "entities": [
                    {"entity_type": "PERSON", "text": "John Doe", "score": 0.85}
                ],
            }
        ]

        # Capture output
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            pii_detect.print_results(results, "json")

        output = captured_output.getvalue()

        # Verify JSON output
        try:
            parsed_json = json.loads(output)
            self.assertEqual(len(parsed_json), 1)
            self.assertEqual(parsed_json[0]["file"], "test.txt")
            self.assertTrue(parsed_json[0]["pii_found"])
            self.assertEqual(parsed_json[0]["pii_count"], 1)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    @patch("pii_detect.PIIDetector")
    def test_print_results_no_pii(self, _):
        """Test output when no PII is found"""
        # Mock results with no PII
        results = [
            {"file": "test.txt", "pii_found": False, "pii_count": 0, "entities": []}
        ]

        # Capture output
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            pii_detect.print_results(results, "text")

        output = captured_output.getvalue()

        # Verify output
        self.assertIn("Files analyzed: 1", output)
        self.assertIn("Files with PII: 0", output)
        self.assertIn("Total PII entities found: 0", output)
        self.assertIn("No PII detected", output)

    @patch("pii_detect.PIIDetector")
    def test_print_results_with_errors(self, _):
        """Test output when file analysis has errors"""
        # Mock results with error
        results = [
            {
                "file": "error_file.txt",
                "error": "Permission denied",
                "pii_found": False,
                "pii_count": 0,
                "entities": [],
            }
        ]

        # Capture output
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            pii_detect.print_results(results, "text")

        output = captured_output.getvalue()

        # Verify error output
        self.assertIn("ERROR", output)
        self.assertIn("error_file.txt", output)
        self.assertIn("Permission denied", output)

    @patch("sys.argv", ["pii_detect.py", "nonexistent_file.txt"])
    def test_main_nonexistent_file(self):
        """Test main function with nonexistent file"""
        # Mock Path.exists to return False
        with patch("pathlib.Path.exists", return_value=False):
            with patch("sys.exit") as mock_exit:
                captured_output = StringIO()
                with patch("sys.stdout", captured_output):
                    pii_detect.main()

                # Verify exit was called
                mock_exit.assert_called_with(1)

                output = captured_output.getvalue()
                self.assertIn("does not exist", output)

    @patch("sys.argv", ["pii_detect.py", "/fake/path"])
    def test_main_invalid_path_type(self):
        """Test main function with invalid path type"""
        # Mock Path methods
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_file", return_value=False):
                with patch("pathlib.Path.is_dir", return_value=False):
                    with patch("sys.exit") as mock_exit:
                        captured_output = StringIO()
                        with patch("sys.stdout", captured_output):
                            pii_detect.main()

                        # Verify exit was called
                        mock_exit.assert_called_with(1)

                        output = captured_output.getvalue()
                        self.assertIn("not a file or directory", output)

    @patch("sys.argv", ["pii_detect.py", "test.txt"])
    def test_main_single_file(self):
        """Test main function with single file"""
        # Mock detector instance
        mock_detector = Mock()
        mock_detector.analyze_file.return_value = {
            "file": "test.txt",
            "pii_found": False,
            "pii_count": 0,
            "entities": [],
        }

        # Mock Path methods
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_file", return_value=True):
                # Patch both the detector module and the pii_detect module reference
                with patch(
                    "pii_detect.detector.PIIDetector", return_value=mock_detector
                ) as mock_detector_class:
                    with patch.object(pii_detect, "PIIDetector", mock_detector_class):
                        with patch.object(pii_detect, "print_results") as mock_print:
                            pii_detect.main()

                            # Verify detector was called
                            mock_detector_class.assert_called_once()
                            mock_detector.analyze_file.assert_called_once()
                            mock_print.assert_called_once()

    @patch("sys.argv", ["pii_detect.py", "/fake/dir"])
    def test_main_directory(self):
        """Test main function with directory"""
        # Mock detector instance
        mock_detector = Mock()
        mock_detector.analyze_directory.return_value = []

        # Mock Path methods
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_file", return_value=False):
                with patch("pathlib.Path.is_dir", return_value=True):
                    # Directly patch the PIIDetector on the module to avoid import
                    # issues
                    with patch.object(
                        pii_detect, "PIIDetector", return_value=mock_detector
                    ) as mock_detector_class:
                        with patch.object(pii_detect, "print_results") as mock_print:
                            pii_detect.main()

                            # Verify detector was called
                            mock_detector_class.assert_called_once()
                            mock_detector.analyze_directory.assert_called_once()
                            mock_print.assert_called_once()

    @patch("sys.argv", ["pii_detect.py", "-f", "json", "test.txt"])
    def test_main_json_format(self):
        """Test main function with JSON format"""
        # Mock detector instance
        mock_detector = Mock()
        mock_detector.analyze_file.return_value = {
            "file": "test.txt",
            "pii_found": False,
            "pii_count": 0,
            "entities": [],
        }

        # Mock Path methods
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_file", return_value=True):
                with patch(
                    "pii_detect.detector.PIIDetector", return_value=mock_detector
                ) as mock_detector_class:
                    with patch.object(pii_detect, "PIIDetector", mock_detector_class):
                        with patch.object(pii_detect, "print_results") as mock_print:
                            pii_detect.main()

                            # Verify print_results was called with json format
                            mock_detector_class.assert_called_once()
                            mock_detector.analyze_file.assert_called_once()
                            mock_print.assert_called_once()
                            args, _ = mock_print.call_args
                            self.assertEqual(args[1], "json")

    @patch("sys.argv", ["pii_detect.py", "-e", ".py", "-e", ".js", "/fake/dir"])
    def test_main_with_extensions(self):
        """Test main function with custom extensions"""
        # Mock detector instance
        mock_detector = Mock()
        mock_detector.analyze_directory.return_value = []

        # Mock Path methods
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_file", return_value=False):
                with patch("pathlib.Path.is_dir", return_value=True):
                    with patch(
                        "pii_detect.detector.PIIDetector", return_value=mock_detector
                    ) as mock_detector_class:
                        with patch.object(
                            pii_detect, "PIIDetector", mock_detector_class
                        ):
                            with patch.object(pii_detect, "print_results"):
                                pii_detect.main()

                                # Verify analyze_directory was called with extensions
                                mock_detector_class.assert_called_once()
                                mock_detector.analyze_directory.assert_called_once()
                                _, kwargs = mock_detector.analyze_directory.call_args
                                self.assertEqual(kwargs["extensions"], [".py", ".js"])


if __name__ == "__main__":
    unittest.main()
