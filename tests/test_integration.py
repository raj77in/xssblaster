"""Integration tests for XSS Blaster."""

import subprocess
import sys
import tempfile
from pathlib import Path


class TestIntegration:
    """Integration tests that test the full application flow."""

    def test_cli_help(self):
        """Test that CLI help works."""
        result = subprocess.run(
            [sys.executable, "-m", "xssblaster.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0
        assert "XSS Blaster" in result.stdout
        assert "usage:" in result.stdout

    def test_basic_payload_generation_cli(self):
        """Test basic payload generation through CLI."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            result = subprocess.run(
                [sys.executable, "-m", "xssblaster.cli", "-o", temp_path, "--base64"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent,
            )

            assert result.returncode == 0
            assert Path(temp_path).exists()

            content = Path(temp_path).read_text()
            assert len(content) > 0
            # Should have multiple lines of payloads
            lines = content.strip().split("\n")
            assert len(lines) > 1
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_custom_payload_file_integration(self):
        """Test end-to-end with custom payload file."""
        custom_payloads = ["alert('test1')", "prompt('test2')", "console.log('test3')"]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as input_file:
            for payload in custom_payloads:
                input_file.write(payload + "\n")
            input_path = input_file.name

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as output_file:
            output_path = output_file.name

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "xssblaster.cli",
                    "-i",
                    input_path,
                    "-o",
                    output_path,
                    "-p",
                    "PREFIX_",
                    "-s",
                    "_SUFFIX",
                ],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent,
            )

            assert result.returncode == 0

            content = Path(output_path).read_text()
            lines = content.strip().split("\n")

            # Should have at least as many lines as input payloads
            assert len(lines) >= len(custom_payloads)

            # Check that custom payloads are present with prefix/suffix
            for line in lines:
                if line.strip():
                    assert line.startswith("PREFIX_")
                    assert line.endswith("_SUFFIX")

        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(output_path).unlink(missing_ok=True)

    def test_multiple_encoding_options(self):
        """Test multiple encoding options together."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "xssblaster.cli",
                    "--base64",
                    "--unicode",
                    "--hex",
                    "-o",
                    temp_path,
                ],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent,
            )

            assert result.returncode == 0

            content = Path(temp_path).read_text()
            lines = content.strip().split("\n")

            # Should have many more payloads with multiple encodings
            assert len(lines) > 10

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_no_output_option(self):
        """Test --no-output option."""
        result = subprocess.run(
            [sys.executable, "-m", "xssblaster.cli", "--no-output"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0
        # Should not output payloads to stdout
        assert len(result.stdout.strip()) == 0 or "first run" in result.stdout.lower()

    def test_version_option(self):
        """Test --version option."""
        result = subprocess.run(
            [sys.executable, "-m", "xssblaster.cli", "--version"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0
        # Should output version information
        assert len(result.stdout.strip()) > 0


class TestPayloadQuality:
    """Tests to ensure payload quality and correctness."""

    def test_payload_syntax_validity(self):
        """Test that generated payloads have valid syntax."""
        from xssblaster import generate_payloads

        payloads, _, _ = generate_payloads(variant_filters={"base": True})
        payloads_list = list(payloads)

        for counter, payload in payloads_list:
            # Basic syntax checks
            assert isinstance(payload, str)
            assert len(payload) > 0

            # Should not contain unresolved placeholders
            assert "{n}" not in payload

            # Should contain the counter value
            assert str(counter) in payload

    def test_encoding_correctness(self):
        """Test that encodings are applied correctly."""
        from xssblaster import generate_payloads

        # Test HTML entity encoding
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "html_entity": True}
        )
        payloads_list = list(payloads)

        # Should have both base and encoded variants
        base_payloads = []
        encoded_payloads = []

        for _, payload in payloads_list:
            if "&#" in payload:
                encoded_payloads.append(payload)
            else:
                base_payloads.append(payload)

        assert len(base_payloads) > 0
        assert len(encoded_payloads) > 0

    def test_payload_diversity(self):
        """Test that payloads are diverse and cover different attack vectors."""
        from xssblaster import generate_payloads

        payloads, _, _ = generate_payloads(variant_filters={"base": True})
        payloads_list = list(payloads)

        payload_texts = [payload for _, payload in payloads_list]

        # Should have different types of payloads
        has_script_tag = any("<script" in p.lower() for p in payload_texts)
        has_img_tag = any("<img" in p.lower() for p in payload_texts)
        has_svg_tag = any("<svg" in p.lower() for p in payload_texts)
        has_javascript_protocol = any("javascript:" in p.lower() for p in payload_texts)

        # Should have at least some variety
        attack_types = sum(
            [has_script_tag, has_img_tag, has_svg_tag, has_javascript_protocol]
        )
        assert attack_types >= 2, "Payloads should include multiple attack vectors"

    def test_counter_uniqueness(self):
        """Test that payload counters are unique and sequential."""
        from xssblaster import generate_payloads

        payloads, _, _ = generate_payloads(variant_filters={"base": True})
        payloads_list = list(payloads)

        counters = [counter for counter, _ in payloads_list]

        # Counters should be unique
        assert len(counters) == len(set(counters))

        # Counters should start from 1 and be sequential
        assert min(counters) == 1
        assert max(counters) == len(counters)
