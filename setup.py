# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xssblaster",
    version="1.0.0",
    author="Amit Agarwal",
    description="Advanced XSS payload generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'xssblaster': ['my-xss.txt'],
    },
    entry_points={
        'console_scripts': [
            'xssblaster = xssblaster.cli:cli',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)