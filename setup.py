#!/usr/bin/env python
"""Setup script for Banking ETL Assessment."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="banking_etl_assessment",
    version="1.0.0",
    author="Banking ETL Team",
    description="A comprehensive Banking ETL (Extract, Transform, Load) assessment project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
        ],
    },
    entry_points={
        "console_scripts": [
            "banking-etl=example:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="etl extract transform load banking finance csv validation",
    url="https://github.com/your-username/banking_etl_assessment",
    project_urls={
        "Documentation": "https://github.com/your-username/banking_etl_assessment/blob/main/README.md",
        "Source": "https://github.com/your-username/banking_etl_assessment",
        "Bug Tracker": "https://github.com/your-username/banking_etl_assessment/issues",
    },
)
