import string
from setuptools import find_packages, setup


def load_README() -> str:
    """Load the README.md file in current directory"""
    with open("README.md") as f:
        return f.read()

setup(
    name="assemblyai",
    version="1.0.0",
    url="https://github.com/Jeadie/assemblyai-python-sdk",
    author="Jack Eadie",
    author_email="jackeadie@duck.com",
    description="AssemblyAI Python SDK",
    long_description=load_README(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
    ]
)