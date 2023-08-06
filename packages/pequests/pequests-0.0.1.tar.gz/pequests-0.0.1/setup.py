from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A simple proxy HTTP request library.'

# Setting up
setup(
    name="pequests",
    version=VERSION,
    author="Fritz Forster",
    author_email="fritzforster@protonmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'file', 'write file', 'fast witing', 'simple'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
    ]
)