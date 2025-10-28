from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ResumeATSOptimizer",
    version="0.1",
    author="Shivanand",
    packages=find_packages(),
    install_requires = requirements,
)