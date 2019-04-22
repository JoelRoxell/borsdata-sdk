import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="borsdata-sdk",
    version="0.0.1",
    author="Joel S. Roxell",
    author_email="joel.roxell@annevo.se",
    description="Borsdata api SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelroxell/borsdata-sdk",
    packages=['borsdata_sdk', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
