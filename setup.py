#!/usr/bin/env python3
"""Setup configuration for mini-display package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mini-display",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="Mini Display (16x32) with tiny pixel font and colored widgets for LED matrices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mini-display",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=9.0.0",
        "requests>=2.25.0",
        "nyct-gtfs>=1.0.0",
        "protobuf>=3.19.0",
    ],
    extras_require={
        "rpi": [
            "rpi-rgb-led-matrix>=0.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "mini-display=mini_display.display:main",
        ],
    },
)