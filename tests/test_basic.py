# tests/test_basic.py
from xssblaster import generate_payloads


def test_generate_payloads():
    payloads, base_count, total = generate_payloads(variant_filters={"base": True})
    payloads = list(payloads)
    assert len(payloads) > 0
    assert base_count > 0
    assert total > 0
