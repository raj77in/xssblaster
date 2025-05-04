# XSSBlaster

A Python-based XSS payload generator tool designed for ethical security testing of web applications. This tool automates the generation of obfuscated and encoded XSS payloads to bypass common input filters and WAFs.

## ✨ Features

* Generates a variety of XSS payloads using different obfuscation techniques.
* Supports encoding (HTML entity, URL, Base64, `String.fromCharCode`, etc.).
* Includes options to customize payload prefix/suffix and whether to encode them.
* Automatically increments payload ID to help trace successful injections.
* Takes input from custom payload files or uses built-in payload list.
* Supports output to file or console only.
* Designed to be used as both CLI and Python module.

## 🚀 Quick Start

```bash
python3 xssblaster.py -o out.txt -p '<script>' -s '</script>' -e
```

This command:

* Saves payloads to `out.txt`
* Wraps each payload inside `<script>` and `</script>`
* Encodes prefix and suffix using HTML entities

## 🔧 CLI Usage

```bash
python3 xssblaster.py [options]
```

### Options

* `-o`, `--output`: Output file name.
* `-p`, `--prefix`: Payload prefix.
* `-s`, `--suffix`: Payload suffix.
* `-e`, `--encode-wrap`: Encode prefix and suffix.
* `-i`, `--input`: Custom payload file path.
* `-n`, `--no-output`: Don’t write to file.
* `-f`, `--filter`: Filter type (e.g., html-encoded) \[currently not enforced but future-ready]

### Example

```bash
python3 xssblaster.py -o xss.txt -p '<svg>' -s '</svg>' -e -i my_payloads.txt
```

## 🖉 Use as a Python Module

```python
from xss_payload_generator import generate_payloads

payloads = generate_payloads(prefix='<script>', suffix='</script>', encode_prefix_suffix=True)
for num, payload in payloads:
    print(f"[{num}] {payload}")
```

You can also pass `payload_file="my_payloads.txt"` to load your own base payloads.

## 🚫 Ethical Use Only

> This tool is intended for use in penetration testing and security research **with explicit authorization only**. Do not use it against systems without consent. Stay legal, stay ethical.

## 📁 Project Structure

* `xssblaster.py` - Main script.
* `README.md` - This file.
* `my_payloads.txt` - Optional custom payloads input.

## ✨ Contribution & Improvements

Pull requests, payload contributions, and ideas to evade more modern filters are welcome. Let's make this smarter and sneakier (for the good guys)!

## 🌟 Author

Amit Agarwal | Security Researcher & Pentester

## 🚨 Disclaimer

This tool is provided as-is. The author is not responsible for any misuse. Always test with proper permission.
