#!/usr/bin/env python
# coding: utf-8
from setuptools import find_packages, setup

with open("fastFET/README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()    
with open("requirements.txt", "r", encoding='UTF-8' ) as f:     
    lines= f.readlines()
    requires= [ line.strip() for line in lines]

setup( 
    name="fastFET",
    version="0.0.2", 
    author="James Ray",
    author_email="hl1670704310@icloud.com",
    description="A fast feature extrating tool for BGP Dataset Collection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/author/value***c/tree/master",
    python_requires='>=3.8.0',
    packages=find_packages(),
    
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license= "MIT",
    install_requires=requires
)
