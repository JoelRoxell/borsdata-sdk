import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="borsdata_sdk",
    version="1.1.3",
    author="Joel S. Roxell",
    author_email="joel.roxell@annevo.se",
    description="Borsdata api SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelroxell/borsdata_sdk-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "case-converter"],
)
