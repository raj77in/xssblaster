#!/usr/bin/env python3
"""
XSS Blaster Command Line Interface
"""

import argparse
import sys
from pathlib import Path

from .core import generate_payloads
from .utils import copy_default_payload_file, get_payload_file_path


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="XSS Blaster - Advanced XSS Payload Generator",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Input/Output
    io_group = parser.add_argument_group("Input/Output")
    io_group.add_argument(
        "-o", "--output", help="Output file to write payloads (default: stdout)"
    )
    io_group.add_argument(
        "-i",
        "--input",
        help="Input file containing base payloads (default: ~/.config/xssblaster/my-xss.txt or built-in)",
    )
    io_group.add_argument(
        "-n",
        "--no-output",
        action="store_true",
        help="Don't write to output file, just show statistics",
    )

    # Configuration
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "--init-config",
        action="store_true",
        help="Initialize user config directory with default payload file",
    )

    # Payload wrapping
    wrap_group = parser.add_argument_group("Payload Wrapping")
    wrap_group.add_argument(
        "-p", "--prefix", default="", help="Prefix to prepend to each payload"
    )
    wrap_group.add_argument(
        "-s", "--suffix", default="", help="Suffix to append to each payload"
    )
    wrap_group.add_argument(
        "--ep",
        "--encode-prefix",
        dest="encode_prefix",
        action="store_true",
        help="Encode the prefix",
    )
    wrap_group.add_argument(
        "--es",
        "--encode-suffix",
        dest="encode_suffix",
        action="store_true",
        help="Encode the suffix",
    )

    # Encoding options
    enc_group = parser.add_argument_group("Encoding Options")

    # Basic encodings
    enc_group.add_argument(
        "-c",
        "--charcode",
        action="store_true",
        help="Generate String.fromCharCode encoded payloads",
    )
    enc_group.add_argument(
        "-b", "--base64", action="store_true", help="Generate Base64 encoded payloads"
    )
    enc_group.add_argument(
        "-U", "--unicode", action="store_true", help="Generate Unicode escaped payloads"
    )
    enc_group.add_argument(
        "-H", "--hex", action="store_true", help="Generate hex encoded payloads"
    )
    enc_group.add_argument(
        "-O", "--octal", action="store_true", help="Generate octal encoded payloads"
    )
    enc_group.add_argument(
        "-D", "--decimal", action="store_true", help="Generate decimal encoded payloads"
    )

    # HTML encodings
    enc_group.add_argument(
        "-hn",
        "--htmlnamed",
        action="store_true",
        help="Generate HTML named entity payloads",
    )
    enc_group.add_argument(
        "-C", "--css", action="store_true", help="Generate CSS unicode encoded payloads"
    )

    # Advanced obfuscation
    enc_group.add_argument(
        "-j",
        "--jsfuck",
        action="store_true",
        help="Generate JSFuck encoded payloads (extreme obfuscation)",
    )
    enc_group.add_argument(
        "-hg",
        "--homoglyph",
        action="store_true",
        help="Generate homoglyph obfuscated payloads",
    )
    enc_group.add_argument(
        "-zw",
        "--zerowidth",
        action="store_true",
        help="Generate zero-width character obfuscated payloads",
    )
    enc_group.add_argument(
        "-l",
        "--leet",
        action="store_true",
        help="Generate leet speak obfuscated payloads",
    )
    enc_group.add_argument(
        "-cv",
        "--casevar",
        action="store_true",
        help="Generate case variation obfuscated payloads",
    )
    enc_group.add_argument(
        "-R", "--reverse", action="store_true", help="Generate reversed payloads"
    )

    # Language-specific
    enc_group.add_argument(
        "-pc",
        "--phpchr",
        action="store_true",
        help="Generate PHP chr() encoded payloads",
    )
    enc_group.add_argument(
        "-py",
        "--pythonchr",
        action="store_true",
        help="Generate Python chr() encoded payloads",
    )
    enc_group.add_argument(
        "-ps",
        "--powershell",
        action="store_true",
        help="Generate PowerShell [char] encoded payloads",
    )
    enc_group.add_argument(
        "-sq",
        "--sqlchar",
        action="store_true",
        help="Generate SQL CHAR() encoded payloads",
    )
    enc_group.add_argument(
        "-v",
        "--vbscript",
        action="store_true",
        help="Generate VBScript encoded payloads",
    )

    # Data encodings
    enc_group.add_argument(
        "-d",
        "--datauri",
        action="store_true",
        help="Generate data URI encoded payloads",
    )
    enc_group.add_argument(
        "-a", "--atob", action="store_true", help="Generate atob() encoded payloads"
    )
    enc_group.add_argument(
        "-r", "--rot13", action="store_true", help="Generate ROT13 encoded payloads"
    )
    enc_group.add_argument(
        "-q",
        "--quotedprint",
        action="store_true",
        help="Generate quoted-printable encoded payloads",
    )
    enc_group.add_argument(
        "-uu", "--uuencode", action="store_true", help="Generate UUencoded payloads"
    )
    enc_group.add_argument(
        "-P",
        "--punycode",
        action="store_true",
        help="Generate punycode encoded payloads",
    )
    enc_group.add_argument(
        "-m",
        "--morse",
        action="store_true",
        help="Generate Morse code encoded payloads",
    )
    enc_group.add_argument(
        "-B", "--binary", action="store_true", help="Generate binary encoded payloads"
    )

    # Additional options
    parser.add_argument(
        "--version",
        action="version",
        version=f"XSS Blaster v{__import__('xssblaster').__version__}",
    )

    return parser.parse_args()


def cli() -> int:
    """Command line interface entry point."""
    args = parse_args()

    # Handle init-config option
    if args.init_config:
        config_dir = Path.home() / ".config" / "xssblaster"
        user_payload_file = config_dir / "my-xss.txt"

        if user_payload_file.exists():
            print(f"📝 Configuration already exists at: {config_dir}")
            print(f"📝 Payload file: {user_payload_file}")
            print("💡 You can edit this file to customize your payloads.")
            return 0

        if copy_default_payload_file():
            print(f"✅ Configuration initialized at: {config_dir}")
            print(f"📝 Default payload file: {user_payload_file}")
            print("💡 You can now edit this file to customize your payloads.")
            return 0
        else:
            print("❌ Failed to initialize configuration.")
            return 1

    # Set up variant filters based on command line args
    variant_filters = {
        # Basic encodings
        "base": True,  # Always include base variant
        "from_char_code": args.charcode,
        "base64_encode": args.base64,
        "unicode_escape": args.unicode,
        "hex_encode": args.hex,
        "octal_encode": args.octal,
        "decimal_encode": args.decimal,
        # HTML encodings
        "html_named_entities": args.htmlnamed,
        "css_unicode_encode": args.css,
        # Advanced obfuscation
        "jsfuck_encode": args.jsfuck,
        "homoglyph_encode": args.homoglyph,
        "zero_width_encode": args.zerowidth,
        "leet_speak_encode": args.leet,
        "case_variation_encode": args.casevar,
        "reverse_encode": args.reverse,
        # Language-specific
        "php_chr_encode": args.phpchr,
        "python_chr_encode": args.pythonchr,
        "powershell_char_encode": args.powershell,
        "sql_char_encode": args.sqlchar,
        "vbscript_encode": args.vbscript,
        # Data encodings
        "data_uri_encode": args.datauri,
        "atob_encode": args.atob,
        "rot13": args.rot13,
        "quoted_printable_encode": args.quotedprint,
        "uuencode": args.uuencode,
        "punycode_encode": args.punycode,
        "morse_encode": args.morse,
        "binary_encode": args.binary,
    }

    try:
        # Check if this is the first run and auto-initialize if needed
        config_dir = Path.home() / ".config" / "xssblaster"
        user_payload_file = config_dir / "my-xss.txt"

        # Auto-initialize on first run if no custom input specified
        if not args.input and not user_payload_file.exists():
            if copy_default_payload_file():
                pass
            else:
                pass

        # Determine payload file to use
        payload_file = get_payload_file_path(args.input)

        # Generate payloads
        payloads, base_count, total_count = generate_payloads(
            prefix=args.prefix,
            suffix=args.suffix,
            encode_prefix=args.encode_prefix,
            encode_suffix=args.encode_suffix,
            payload_file=payload_file,
            variant_filters=variant_filters,
        )

        # Output results
        output_file = None
        try:
            if args.output and not args.no_output:
                output_file = open(args.output, "w")

            for _, payload in payloads:
                if args.no_output:
                    continue
                if output_file:
                    output_file.write(payload + "\n")
                else:
                    pass

            if not args.no_output and args.output:
                print(f"[+] Payloads written to {args.output}")

        finally:
            if output_file:
                output_file.close()

        return 0

    except Exception as e:
        if hasattr(e, "errno") and e.errno == 2:  # File not found
            pass
        return 1


if __name__ == "__main__":
    sys.exit(cli())
