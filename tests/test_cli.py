"""Tests for CLI functionality."""

import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from xssblaster.cli import cli, parse_args


class TestParseArgs:
    """Test the argument parsing functionality."""

    def test_default_args(self):
        """Test default argument values."""
        with patch("sys.argv", ["xssblaster"]):
            args = parse_args()

            assert args.output is None
            assert args.input is None
            assert args.no_output is False
            assert args.init_config is False
            assert args.prefix == ""
            assert args.suffix == ""
            assert args.base64 is False
            assert args.unicode is False

    def test_output_arg(self):
        """Test output argument parsing."""
        with patch("sys.argv", ["xssblaster", "-o", "output.txt"]):
            args = parse_args()
            assert args.output == "output.txt"

    def test_input_arg(self):
        """Test input argument parsing."""
        with patch("sys.argv", ["xssblaster", "-i", "input.txt"]):
            args = parse_args()
            assert args.input == "input.txt"

    def test_encoding_flags(self):
        """Test encoding flag parsing."""
        with patch("sys.argv", ["xssblaster", "--base64", "--unicode", "--hex"]):
            args = parse_args()
            assert args.base64 is True
            assert args.unicode is True
            assert args.hex is True

    def test_prefix_suffix(self):
        """Test prefix and suffix arguments."""
        with patch("sys.argv", ["xssblaster", "-p", "PREFIX", "-s", "SUFFIX"]):
            args = parse_args()
            assert args.prefix == "PREFIX"
            assert args.suffix == "SUFFIX"

    def test_init_config_flag(self):
        """Test init-config flag."""
        with patch("sys.argv", ["xssblaster", "--init-config"]):
            args = parse_args()
            assert args.init_config is True


class TestCLI:
    """Test the CLI functionality."""

    @patch("pathlib.Path.home")
    def test_init_config_new(self, mock_home):
        """Test --init-config with new configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_home.return_value = Path(temp_dir)

            with patch("sys.argv", ["xssblaster", "--init-config"]):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    result = cli()
                    output = fake_out.getvalue()

                    # Should succeed (return 0) or fail gracefully
                    assert result in [0, 1]
                    # Should have some output about configuration
                    assert (
                        "configuration" in output.lower() or "config" in output.lower()
                    )

    @patch("pathlib.Path.home")
    def test_init_config_existing(self, mock_home):
        """Test --init-config with existing configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_home.return_value = Path(temp_dir)
            config_dir = Path(temp_dir) / ".config" / "xssblaster"
            config_dir.mkdir(parents=True)
            user_file = config_dir / "my-xss.txt"
            user_file.write_text("existing payload")

            with patch("sys.argv", ["xssblaster", "--init-config"]):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    result = cli()
                    output = fake_out.getvalue()

                    assert result == 0
                    assert "already exists" in output

    def test_basic_payload_generation(self):
        """Test basic payload generation."""
        with patch("sys.argv", ["xssblaster", "--no-output"]):
            result = cli()
            # Should succeed
            assert result == 0

    def test_output_to_file(self):
        """Test outputting payloads to file."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            with patch("sys.argv", ["xssblaster", "-o", temp_path]):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    result = cli()
                    output = fake_out.getvalue()

                    assert result == 0
                    assert "written to" in output

                    # Check that file was created and has content
                    assert Path(temp_path).exists()
                    content = Path(temp_path).read_text()
                    assert len(content) > 0
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_custom_input_file(self):
        """Test using custom input file."""
        custom_payloads = ["custom1", "custom2", "custom3"]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as input_file:
            for payload in custom_payloads:
                input_file.write(payload + "\n")
            input_path = input_file.name

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as output_file:
            output_path = output_file.name

        try:
            with patch("sys.argv", ["xssblaster", "-i", input_path, "-o", output_path]):
                result = cli()
                assert result == 0

                # Check output contains custom payloads
                content = Path(output_path).read_text()
                for payload in custom_payloads:
                    assert payload in content
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(output_path).unlink(missing_ok=True)

    def test_encoding_options(self):
        """Test various encoding options."""
        encoding_flags = ["--base64", "--unicode", "--hex", "--html"]

        for flag in encoding_flags:
            with patch("sys.argv", ["xssblaster", flag, "--no-output"]):
                result = cli()
                assert result == 0

    def test_prefix_suffix_functionality(self):
        """Test prefix and suffix functionality."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            with patch(
                "sys.argv", ["xssblaster", "-p", "PRE_", "-s", "_SUF", "-o", temp_path]
            ):
                result = cli()
                assert result == 0

                content = Path(temp_path).read_text()
                lines = content.strip().split("\n")

                # Check that payloads have prefix and suffix
                for line in lines:
                    if line.strip():  # Skip empty lines
                        assert line.startswith("PRE_")
                        assert line.endswith("_SUF")
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_error_handling(self):
        """Test error handling with invalid input."""
        with patch(
            "sys.argv", ["xssblaster", "-i", "/nonexistent/file.txt", "--no-output"]
        ):
            result = cli()
            # Should handle error gracefully
            assert result in [0, 1]
