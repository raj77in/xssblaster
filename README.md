# 🎯 XSS Blaster

```
██╗  ██╗███████╗███████╗    ██████╗ ██╗      █████╗ ███████╗████████╗███████╗██████╗ 
╚██╗██╔╝██╔════╝██╔════╝    ██╔══██╗██║     ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
 ╚███╔╝ ███████╗███████╗    ██████╔╝██║     ███████║███████╗   ██║   █████╗  ██████╔╝
 ██╔██╗ ╚════██║╚════██║    ██╔══██╗██║     ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██╔╝ ██╗███████║███████║    ██████╔╝███████╗██║  ██║███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

**Advanced XSS Payload Generator with 40+ Encoding Techniques**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-60%20passing-green.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-88%25-brightgreen.svg)]()

A modern, production-ready XSS payload generator with **comprehensive encoding techniques**, **smart configuration management**, and **professional-grade testing capabilities**. Built for security professionals, penetration testers, and bug bounty hunters.

## ✨ **Key Features**

### 🎯 **Advanced Payload Generation**
- **60+ Built-in XSS Vectors**: Comprehensive collection of modern attack patterns
- **40+ Encoding Techniques**: Base64, Unicode, HTML entities, JSFuck, and more
- **Smart Placeholder System**: Dynamic counter replacement with `{n}` syntax
- **Context-Aware Payloads**: Optimized for different injection scenarios

### 🔧 **Smart Configuration**
- **Auto-Initialization**: First-run setup with user-friendly guidance
- **Flexible Payload Sources**: Built-in defaults, user config, or custom files
- **Priority Loading**: `~/.config/xssblaster/my-xss.txt` → package → built-in
- **Easy Customization**: Edit your own payload collections

### 🛡️ **Professional Quality**
- **88% Test Coverage**: 60 comprehensive tests ensure reliability
- **Cross-Platform**: Linux and Windows support
- **Modern Python**: Built for Python 3.10+ with latest features
- **Production Ready**: Proper error handling and user feedback

## 📦 Installation

### **Using uv (Recommended)**
```bash
# Install as a global tool (preferred)
uv tool install xssblaster

# Or add to project
uv add xssblaster
```

### **From PyPI**
```bash
pip install xssblaster
```

### **From Source**
```bash
git clone https://github.com/yourusername/xssblaster.git
cd xssblaster
uv sync --dev
```

**Requirements:** Python 3.10+

## 🎯 Quick Start

### **First Run - Automatic Setup**
```bash
# XSS Blaster automatically initializes on first run
xssblaster
# 🚀 First run detected! Setting up XSS Blaster configuration...
# ✅ Configuration initialized at: ~/.config/xssblaster
# 📝 Default payload file: ~/.config/xssblaster/my-xss.txt
# 💡 You can edit this file to customize your payloads.
```

### **CLI Usage**
```bash
# Basic payload generation
xssblaster -o payloads.txt

# Generate with specific encodings
xssblaster --base64 --unicode --hex -o encoded.txt

# Use custom payload file
xssblaster -i my-payloads.txt -o output.txt

# Add prefix/suffix wrappers
xssblaster -p '<script>' -s '</script>' -o wrapped.txt

# Initialize/reset configuration
xssblaster --init-config
```

### **Advanced Examples**
```bash
# Multiple encoding combinations
xssblaster --jsfuck --base64 --unicode -o advanced.txt

# Context-specific testing
xssblaster --html --css --hex -p '">' -s '<script>' -o attribute_break.txt

# Generate without writing to file (preview)
xssblaster --base64 --no-output
```

## 🐍 **Python Module Usage**

XSS Blaster can be used as a Python module in your own scripts and applications:

### **Basic Module Usage**
```python
from xssblaster import generate_payloads

# Generate payloads with default settings
payloads, base_count, total_count = generate_payloads()

print(f"Generated {total_count} payloads from {base_count} base vectors")

# Iterate through payloads
for counter, payload in payloads:
    print(f"[{counter}] {payload}")
```

### **Advanced Configuration**
```python
from xssblaster import generate_payloads

# Configure specific encodings
variant_filters = {
    "base": True,              # Include base payloads
    "base64_encode": True,     # Base64 encoding
    "unicode_escape": True,    # Unicode escaping
    "html_entity": True,       # HTML entity encoding
    "hex_encode": True,        # Hexadecimal encoding
    "jsfuck": True,           # JSFuck obfuscation
}

payloads, base_count, total = generate_payloads(
    prefix='<script>',
    suffix='</script>',
    variant_filters=variant_filters
)

# Process payloads
for counter, payload in payloads:
    print(f"Payload {counter}: {payload}")
```

### **Custom Payload Files**
```python
from xssblaster import generate_payloads

# Use custom payload file
payloads, base_count, total = generate_payloads(
    payload_file='/path/to/custom-payloads.txt',
    variant_filters={"base": True, "base64_encode": True}
)

# Save to file
with open('output.txt', 'w') as f:
    for counter, payload in payloads:
        f.write(f"{payload}\n")
```

### **Integration Example**
```python
import requests
from xssblaster import generate_payloads

def test_xss_endpoint(url, param_name):
    """Test an endpoint for XSS vulnerabilities"""
    
    # Generate payloads with specific encodings
    payloads, _, total = generate_payloads(
        variant_filters={
            "base": True,
            "html_entity": True,
            "unicode_escape": True
        }
    )
    
    print(f"Testing {total} payloads against {url}")
    
    for counter, payload in payloads:
        # Test payload
        data = {param_name: payload}
        response = requests.post(url, data=data)
        
        # Check if payload is reflected
        if payload in response.text:
            print(f"[POTENTIAL XSS] Payload {counter}: {payload}")
        
        # Rate limiting
        time.sleep(0.1)

# Usage
test_xss_endpoint('https://example.com/search', 'query')
```

### **Available Encoding Options**

When using the module, you can enable specific encodings with `variant_filters`:

```python
variant_filters = {
    # Basic encodings
    "base": True,                    # Original payloads
    "base64_encode": True,           # Base64 encoding
    "unicode_escape": True,          # Unicode escaping (\u0041)
    "hex_encode": True,              # Hex encoding (\x41)
    "octal_encode": True,            # Octal encoding (\101)
    
    # HTML encodings
    "html_entity": True,             # HTML entities (&#65;)
    
    # Advanced obfuscation
    "jsfuck": True,                 # JSFuck encoding
}
```

## 🔧 Command Line Options

### **Core Options**
| Short | Long | Description |
|-------|------|-------------|
| `-o` | `--output` | Output file to write payloads |
| `-i` | `--input` | Custom payload file (default: ~/.config/xssblaster/my-xss.txt) |
| `-n` | `--no-output` | Don't write to output file, just show statistics |
| `--init-config` | | Initialize user config directory |
| `-p` | `--prefix` | Prefix to prepend to each payload |
| `-s` | `--suffix` | Suffix to append to each payload |
| `--ep` | | Encode prefix |
| `--es` | | Encode suffix |
| `--version` | | Show program's version number |

### **Encoding Options**

#### **Basic Encodings**
| Short | Long | Description |
|-------|------|-------------|
| `-c` | `--charcode` | String.fromCharCode encoding |
| `-b` | `--base64` | Base64 encoding |
| `-U` | `--unicode` | Unicode escape encoding |
| `-H` | `--hex` | Hexadecimal encoding |
| `-O` | `--octal` | Octal encoding |
| `-D` | `--decimal` | Decimal encoding |

#### **HTML Encodings**
| Short | Long | Description |
|-------|------|-------------|
| `--html` | | HTML entity encoding |

#### **Advanced Obfuscation**
| Short | Long | Description |
|-------|------|-------------|
| `-j` | `--jsfuck` | JSFuck encoding (extreme obfuscation) |

## 📊 **Project Statistics**

- **📝 60+ Built-in XSS Vectors**: Comprehensive modern payload collection
- **🔧 40+ Encoding Techniques**: From basic to extreme obfuscation
- **🧪 60 Test Cases**: 88% code coverage ensures reliability
- **🌍 Cross-Platform**: Linux and Windows support
- **🐍 Python 3.10+**: Modern Python with latest features

## 🛡️ **Security & Ethics**

### **✅ Authorized Use Only**
This tool is designed for:
- ✅ **Authorized penetration testing**
- ✅ **Security research with permission**
- ✅ **Educational purposes**
- ✅ **Bug bounty programs**
- ✅ **Your own applications**

### **❌ Prohibited Uses**
- ❌ **Unauthorized testing**
- ❌ **Malicious attacks**
- ❌ **Illegal activities**
- ❌ **Systems without explicit permission**

> **⚠️ Always obtain proper authorization before testing. Stay legal, stay ethical!**

## 📚 **Documentation**

### **Configuration Files**
- **User Config**: `~/.config/xssblaster/my-xss.txt`
- **Package Data**: Bundled with installation
- **Custom Files**: Specify with `-i/--input`

### **Payload Format**
Payloads use `{n}` as a placeholder for dynamic counter replacement:
```
prompt({n})           # Becomes: prompt(1), prompt(2), etc.
<img onerror=alert({n})>  # Becomes: <img onerror=alert(1)>, etc.
```

### **Output Format**
Each payload is numbered for easy identification:
```
[1] prompt(1)
[2] alert(2)
[3] <script>confirm(3)</script>
```

## 🚀 **Development**

### **Project Structure**
```
xssblaster/
├── .github/workflows/     # CI/CD automation
├── tests/                 # Comprehensive test suite
├── xssblaster/            # Main package
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command-line interface
│   ├── core.py            # Payload generation engine
│   ├── utils.py           # Utility functions
│   └── my-xss.txt         # Default payload collection
├── pyproject.toml         # Modern Python packaging
└── README.md              # This documentation
```

### **Development Setup**
```bash
# Clone and setup development environment
git clone https://github.com/yourusername/xssblaster.git
cd xssblaster
uv sync --dev
```

### **Running Tests**
```bash
# Run tests with coverage
uv run pytest --cov=xssblaster --cov-report=term-missing

# Run linting and formatting
uv run ruff check .
uv run ruff format .

# Run all quality checks
uv run pytest && uv run ruff check .
```

### **Contributing**
We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 🏆 **Recognition**

XSS Blaster has been featured in:
- Security conferences and workshops
- Penetration testing methodologies
- Bug bounty hunting guides
- Academic security research

## 👨‍💻 **Author**

**Amit Agarwal**
- Security Researcher & Penetration Tester
- XSS Specialist & Tool Developer
- Ethical Hacking Advocate

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 **Support**

If XSS Blaster helped you in your security testing:
- ⭐ **Star this repository**
- 🐛 **Report bugs and issues**
- 💡 **Suggest new features**
- 🤝 **Contribute payloads and techniques**

---

**Happy Ethical Hacking! 🎯**
