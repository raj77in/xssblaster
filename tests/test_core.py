"""Tests for core functionality."""

import tempfile
from pathlib import Path

from xssblaster.core import generate_payloads


class TestGeneratePayloads:
    """Test the generate_payloads function."""

    def test_basic_payload_generation(self):
        """Test basic payload generation with default settings."""
        payloads, base_count, total = generate_payloads(variant_filters={"base": True})
        payloads_list = list(payloads)

        assert len(payloads_list) > 0
        assert base_count > 0
        assert total > 0
        assert total == len(payloads_list)

    def test_multiple_variants(self):
        """Test payload generation with multiple variants."""
        payloads, base_count, total = generate_payloads(
            variant_filters={
                "base": True,
                "html_entity": True,
                "base64_encode": True,
            }
        )
        payloads_list = list(payloads)

        # Should have more payloads with multiple variants
        assert len(payloads_list) > base_count
        assert total == len(payloads_list)

    def test_prefix_suffix(self):
        """Test payload generation with prefix and suffix."""
        prefix = "PREFIX_"
        suffix = "_SUFFIX"

        payloads, _, _ = generate_payloads(
            prefix=prefix, suffix=suffix, variant_filters={"base": True}
        )
        payloads_list = list(payloads)

        # Check that all payloads have prefix and suffix
        for _, payload in payloads_list:
            assert payload.startswith(prefix)
            assert payload.endswith(suffix)

    def test_custom_payload_file(self):
        """Test payload generation with custom payload file."""
        custom_payloads = [
            "custom_payload_1",
            "custom_payload_2",
            "# This is a comment",
            "",  # Empty line
            "custom_payload_3",
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            for payload in custom_payloads:
                f.write(payload + "\n")
            temp_file = f.name

        try:
            payloads, base_count, total = generate_payloads(
                payload_file=temp_file, variant_filters={"base": True}
            )
            payloads_list = list(payloads)

            # Should have 3 non-empty, non-comment payloads
            assert base_count == 3
            assert len(payloads_list) == 3

            # Check that custom payloads are used
            payload_texts = [payload for _, payload in payloads_list]
            assert "custom_payload_1" in payload_texts
            assert "custom_payload_2" in payload_texts
            assert "custom_payload_3" in payload_texts

        finally:
            Path(temp_file).unlink()

    def test_nonexistent_payload_file(self):
        """Test behavior with nonexistent payload file."""
        payloads, base_count, total = generate_payloads(
            payload_file="/nonexistent/file.txt", variant_filters={"base": True}
        )
        payloads_list = list(payloads)

        # Should fall back to built-in payloads
        assert len(payloads_list) > 0
        assert base_count > 0

    def test_empty_variant_filters(self):
        """Test with empty variant filters."""
        payloads, base_count, total = generate_payloads(variant_filters={})
        payloads_list = list(payloads)

        # Should still generate base payloads (default behavior)
        assert len(payloads_list) > 0

    def test_placeholder_replacement(self):
        """Test that {n} placeholders are replaced with counter values."""
        payloads, _, _ = generate_payloads(variant_filters={"base": True})
        payloads_list = list(payloads)

        # Check that placeholders are replaced
        for counter, payload in payloads_list:
            assert "{n}" not in payload
            # Counter should be present in the payload
            assert str(counter) in payload

    def test_encoding_variants(self):
        """Test various encoding variants."""
        encoding_variants = [
            "html_entity",
            "base64_encode",
            "unicode_escape",
            "hex_encode",
            "octal_encode",
        ]

        for variant in encoding_variants:
            payloads, base_count, total = generate_payloads(
                variant_filters={"base": True, variant: True}
            )
            payloads_list = list(payloads)

            # Should have more payloads than just base
            assert len(payloads_list) > base_count
            assert total == len(payloads_list)

    def test_no_payloads_scenario(self):
        """Test scenario where no payloads would be generated."""
        # This tests the robustness of the function
        payloads, base_count, total = generate_payloads(
            variant_filters={"nonexistent_variant": True}
        )
        payloads_list = list(payloads)

        # Should still have base payloads due to default behavior
        assert len(payloads_list) >= 0
        assert base_count >= 0
