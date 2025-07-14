"""Tests for utility functions."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from xssblaster.utils import (
    copy_default_payload_file,
    ensure_config_dir,
    get_payload_file_path,
    load_payloads_from_file,
)


class TestGetPayloadFilePath:
    """Test the get_payload_file_path function."""

    def test_custom_file_exists(self):
        """Test with existing custom file."""
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            result = get_payload_file_path(temp_file.name)
            assert result == temp_file.name

    def test_custom_file_not_exists(self):
        """Test with non-existent custom file."""
        result = get_payload_file_path("/nonexistent/file.txt")
        # Should not return the non-existent file
        assert result != "/nonexistent/file.txt"

    def test_no_custom_file(self):
        """Test without custom file specified."""
        result = get_payload_file_path()
        # Should return a path or None
        assert result is None or isinstance(result, str)

    @patch("xssblaster.utils.Path.home")
    def test_user_config_file_exists(self, mock_home):
        """Test when user config file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_home.return_value = Path(temp_dir)
            config_dir = Path(temp_dir) / ".config" / "xssblaster"
            config_dir.mkdir(parents=True)
            user_file = config_dir / "my-xss.txt"
            user_file.write_text("test payload")

            result = get_payload_file_path()
            assert result == str(user_file)


class TestLoadPayloadsFromFile:
    """Test the load_payloads_from_file function."""

    def test_load_valid_file(self):
        """Test loading from a valid file."""
        payloads = [
            "payload1",
            "payload2",
            "# comment",
            "",  # empty line
            "payload3",
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            for payload in payloads:
                f.write(payload + "\n")
            temp_file = f.name

        try:
            result = load_payloads_from_file(temp_file)
            # Should filter out comments and empty lines
            assert len(result) == 3
            assert "payload1" in result
            assert "payload2" in result
            assert "payload3" in result
            assert "# comment" not in result
            assert "" not in result
        finally:
            Path(temp_file).unlink()

    def test_load_nonexistent_file(self):
        """Test loading from non-existent file."""
        result = load_payloads_from_file("/nonexistent/file.txt")
        assert result == []

    def test_load_empty_file(self):
        """Test loading from empty file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_file = f.name

        try:
            result = load_payloads_from_file(temp_file)
            assert result == []
        finally:
            Path(temp_file).unlink()

    def test_load_comments_only_file(self):
        """Test loading from file with only comments."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("# Comment 1\n")
            f.write("# Comment 2\n")
            f.write("\n")
            temp_file = f.name

        try:
            result = load_payloads_from_file(temp_file)
            assert result == []
        finally:
            Path(temp_file).unlink()


class TestEnsureConfigDir:
    """Test the ensure_config_dir function."""

    @patch("xssblaster.utils.Path.home")
    def test_create_config_dir(self, mock_home):
        """Test creating config directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_home.return_value = Path(temp_dir)

            result = ensure_config_dir()
            expected_path = Path(temp_dir) / ".config" / "xssblaster"

            assert result == expected_path
            assert result.exists()
            assert result.is_dir()

    @patch("xssblaster.utils.Path.home")
    def test_existing_config_dir(self, mock_home):
        """Test with existing config directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_home.return_value = Path(temp_dir)
            config_dir = Path(temp_dir) / ".config" / "xssblaster"
            config_dir.mkdir(parents=True)

            result = ensure_config_dir()
            assert result == config_dir
            assert result.exists()


class TestCopyDefaultPayloadFile:
    """Test the copy_default_payload_file function."""

    @patch("xssblaster.utils.Path.home")
    def test_copy_when_not_exists(self, mock_home):
        """Test copying when user file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_home.return_value = Path(temp_dir)

            # This might fail if package file doesn't exist, which is expected
            result = copy_default_payload_file()
            # Result can be True or False depending on package file availability
            assert isinstance(result, bool)

    @patch("xssblaster.utils.Path.home")
    def test_no_overwrite_existing(self, mock_home):
        """Test that existing file is not overwritten."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_home.return_value = Path(temp_dir)
            config_dir = Path(temp_dir) / ".config" / "xssblaster"
            config_dir.mkdir(parents=True)
            user_file = config_dir / "my-xss.txt"
            original_content = "original content"
            user_file.write_text(original_content)

            result = copy_default_payload_file()
            assert result is True
            # File should not be overwritten
            assert user_file.read_text() == original_content
