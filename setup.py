from setuptools import setup, find_packages

with open("requirements.txt", "r") as rf:
    requirements = rf.readlines()

setup(
    name="ictbuilder", 
    version="0.1", 
    package=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "icdbuilder=icdbuilder.__main__:main"
        ]
    })