#!/usr/bin/env python3
"""
Setup configuration for PII Detection CLI
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="pii-detect",
    version="1.0.0",
    author="Ian",
    description="A CLI tool for detecting personally identifiable "
    "information (PII) in text files using Microsoft Presidio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adaptivekind/pii-detect",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pii-detect=pii_detect.cli:main",
        ],
    },
    keywords="pii detection security privacy presidio cli",
    project_urls={
        "Bug Reports": "https://github.com/adaptivekind/pii-detect/issues",
        "Source": "https://github.com/adaptivekind/pii-detect",
        "Documentation": "https://github.com/adaptivekind/pii-detect",
    },
)
