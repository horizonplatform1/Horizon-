from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="datacoin",
    version="1.0.0",
    author="DataCoin Team",
    author_email="team@datacoin.dev",
    description="A digital currency powered by internet data conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datacoin/datacoin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "datacoin=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.css", "*.js", "*.md"],
    },
    keywords="cryptocurrency blockchain data-mining digital-currency web3 fintech",
    project_urls={
        "Bug Reports": "https://github.com/datacoin/datacoin/issues",
        "Source": "https://github.com/datacoin/datacoin",
        "Documentation": "https://datacoin.readthedocs.io/",
    },
)