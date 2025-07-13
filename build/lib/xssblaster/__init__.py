"""
XSS Blaster - Advanced XSS Payload Generator

A comprehensive Python-based tool that generates advanced XSS payloads with 40+ encoding
techniques to bypass modern WAFs, input filters, and security mechanisms.
"""

__version__ = "1.0.0"

from .core import generate_payloads
from .cli import cli

__all__ = ['generate_payloads', 'cli']
