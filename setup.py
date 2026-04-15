from setuptools import setup, find_packages

setup(
    name="entoolkit",
    version="2.2.0",
    author="Andrés García Martínez",
    description="Python extension for the EPANET 2.2 Programmer Toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
