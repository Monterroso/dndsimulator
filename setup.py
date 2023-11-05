from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dndSimulator",
    version="0.0.6",
    author="Marcus Monterroso",
    description="A pet project for simulated d&d battles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Monterroso/dndsimulator",
    license="MIT",
    python_requires=">=3.7",
    install_requires=[],
)