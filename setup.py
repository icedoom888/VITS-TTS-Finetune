from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    dependencies = f.read().splitlines()

setup(
    name="natural_voices",
    version="0.0.1",
    author="Media Technology Center (ETH Zürich)",
    author_email="mtc@ethz.ch",
    description="A python implementation of Vits TTS model",
    packages=find_packages(),
    install_requires=dependencies,
)
