from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Romania Search",
    version="0.0.3",
    author="Raphael Garcia",
    author_email="raphaelgarcia0607@gmail.com",
    description="Multiple search algorithms in Romania map",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raposones/Inteligencia-Artificial-2022.2",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8'
)
