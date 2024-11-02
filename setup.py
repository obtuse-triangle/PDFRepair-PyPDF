from setuptools import setup

with open("README.md", "r") as file:
  long_description = file.read()

setup(
    name="PDF-Repair",
    version="1.1",
    install_requires=[
        "pypdf",
        "tqdm",
        "argparse",
    ],
    scripts=["repair.py"],
    author="obtuse-triangle",
    author_email="me@obtuse.kr",
    description="PDFRepair Tool using PyPDF",
    entry_points={
        "console_scripts": [
            "pdf-repair=repair:main"
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obtuse-triangle/PDFRepair-PyPDF"
)
