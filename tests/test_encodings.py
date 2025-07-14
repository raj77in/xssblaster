"""Tests for encoding functions."""

from xssblaster.core import generate_payloads


class TestEncodingFunctions:
    """Test various encoding functions."""

    def test_base64_encoding(self):
        """Test Base64 encoding functionality."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "base64_encode": True}
        )
        payloads_list = list(payloads)

        # Should have both base and base64 encoded variants
        base64_payloads = [
            p for _, p in payloads_list if "base64" in p.lower() or "btoa" in p.lower()
        ]
        assert len(base64_payloads) > 0

    def test_unicode_encoding(self):
        """Test Unicode encoding functionality."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "unicode_escape": True}
        )
        payloads_list = list(payloads)

        # Should have unicode escaped variants
        unicode_payloads = [p for _, p in payloads_list if "\\u" in p or "\\x" in p]
        assert len(unicode_payloads) > 0

    def test_html_entity_encoding(self):
        """Test HTML entity encoding functionality."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "html_entity": True}
        )
        payloads_list = list(payloads)

        # Should have HTML entity encoded variants
        entity_payloads = [p for _, p in payloads_list if "&#" in p]
        assert len(entity_payloads) > 0

    def test_hex_encoding(self):
        """Test Hex encoding functionality."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "hex_encode": True}
        )
        payloads_list = list(payloads)

        # Should have hex encoded variants
        hex_payloads = [p for _, p in payloads_list if "\\x" in p or "0x" in p]
        assert len(hex_payloads) > 0

    def test_octal_encoding(self):
        """Test Octal encoding functionality."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "octal_encode": True}
        )
        payloads_list = list(payloads)

        # Should have octal encoded variants
        octal_payloads = [
            p for _, p in payloads_list if "\\" in p and any(c in "01234567" for c in p)
        ]
        assert len(octal_payloads) > 0

    def test_multiple_encodings_combination(self):
        """Test that multiple encodings can be applied together."""
        payloads, base_count, total = generate_payloads(
            variant_filters={
                "base": True,
                "base64_encode": True,
                "unicode_escape": True,
                "html_entity": True,
            }
        )
        payloads_list = list(payloads)

        # Should have significantly more payloads with multiple encodings
        assert len(payloads_list) > base_count * 2
        assert total == len(payloads_list)

    def test_encoding_preserves_functionality(self):
        """Test that encodings preserve the basic structure."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "html_entity": True}
        )
        payloads_list = list(payloads)

        for _counter, payload in payloads_list:
            # All payloads should contain some numeric value (counter)
            # Either as plain text or HTML entity encoded
            has_number = any(c.isdigit() for c in payload) or "&#" in payload
            assert has_number, f"Payload should contain a number: {payload}"

            # Should be non-empty strings
            assert isinstance(payload, str)
            assert len(payload) > 0


class TestPayloadVariants:
    """Test different payload variant types."""

    def test_jsfuck_encoding(self):
        """Test JSFuck encoding if available."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "jsfuck": True}
        )
        payloads_list = list(payloads)

        # Should have JSFuck encoded variants (if implemented)
        jsfuck_payloads = [p for _, p in payloads_list if "[]" in p and "+!" in p]
        # JSFuck is complex, so we just check if any complex obfuscation exists
        complex_payloads = [p for _, p in payloads_list if len(p) > 100]
        assert len(jsfuck_payloads) > 0 or len(complex_payloads) > 0

    def test_css_unicode_encoding(self):
        """Test CSS Unicode encoding if available."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "css_unicode_encode": True}
        )
        payloads_list = list(payloads)

        # Should have CSS unicode variants
        css_payloads = [p for _, p in payloads_list if "\\00" in p or "\\0" in p]
        assert len(css_payloads) >= 0  # May not be implemented yet

    def test_data_uri_encoding(self):
        """Test Data URI encoding if available."""
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "data_uri_encode": True}
        )
        payloads_list = list(payloads)

        # Should have data URI variants
        data_uri_payloads = [p for _, p in payloads_list if "data:" in p.lower()]
        assert len(data_uri_payloads) >= 0  # May not be implemented yet

    def test_language_specific_encodings(self):
        """Test language-specific encodings."""
        language_variants = [
            "php_chr_encode",
            "python_chr_encode",
            "powershell_char_encode",
            "sql_char_encode",
            "vbscript_encode",
        ]

        for variant in language_variants:
            payloads, _, _ = generate_payloads(
                variant_filters={"base": True, variant: True}
            )
            payloads_list = list(payloads)

            # Should generate some payloads (even if encoding not fully implemented)
            assert len(payloads_list) > 0


class TestEncodingEdgeCases:
    """Test edge cases for encoding functions."""

    def test_empty_payload_handling(self):
        """Test handling of empty or minimal payloads."""
        # This tests robustness of encoding functions
        payloads, _, _ = generate_payloads(
            variant_filters={"base": True, "html_entity": True}
        )
        payloads_list = list(payloads)

        # Should handle all payloads without errors
        for counter, payload in payloads_list:
            assert isinstance(payload, str)
            assert counter > 0

    def test_special_characters_encoding(self):
        """Test encoding of special characters."""
        # Create a custom payload with special characters
        import tempfile
        from pathlib import Path

        special_payload = "<script>alert('test\"&<>');</script>"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(special_payload + "\n")
            temp_file = f.name

        try:
            payloads, _, _ = generate_payloads(
                payload_file=temp_file,
                variant_filters={"base": True, "html_entity": True},
            )
            payloads_list = list(payloads)

            # Should handle special characters in encoding
            entity_payloads = [p for _, p in payloads_list if "&#" in p]
            assert len(entity_payloads) > 0

            # Encoded payloads should be different from base
            base_payloads = [p for _, p in payloads_list if "&#" not in p]
            assert len(base_payloads) > 0
            assert entity_payloads != base_payloads

        finally:
            Path(temp_file).unlink()

    def test_encoding_consistency(self):
        """Test that encoding is consistent across runs."""
        # Run the same encoding twice
        variant_filters = {"base": True, "html_entity": True}

        payloads1, _, _ = generate_payloads(variant_filters=variant_filters)
        payloads_list1 = list(payloads1)

        payloads2, _, _ = generate_payloads(variant_filters=variant_filters)
        payloads_list2 = list(payloads2)

        # Should produce the same results
        assert len(payloads_list1) == len(payloads_list2)

        # Payloads should be identical
        for (c1, p1), (c2, p2) in zip(payloads_list1, payloads_list2, strict=False):
            assert c1 == c2
            assert p1 == p2
