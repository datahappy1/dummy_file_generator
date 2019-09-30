import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dummy_file_generator",
    version="1.0.3",
    author="datahappy1",
    author_email="",
    description="dummy flat text/csv file generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datahappy1/dummy_file_generator",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)