from setuptools import setup, find_packages
from pathlib import Path

with open("requirements.txt", "r") as rf:
    requirements = rf.readlines()

    setup(
        name="icdbuilder", 
        version="0.1", 
        package=find_packages(),
        install_requires=requirements,
        author="Davide Savarro",
        author_email="davide.savarro@unito.it",
        description="A tool to build ICD files from pandapower networks"
        )