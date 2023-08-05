"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="iconarray",  # Required
    version="v0.1.23",  # Required
    description="A package of modules for processing and plotting ICON data.",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional
    url="https://github.com/C2SM/iconarray",  # Optional
    author="MeteoSwiss, C2SM",  # Optional
    author_email="victoria.cherkas@meteoswiss.ch, annika.lauber@c2sm.ethz.ch",  # Optional
    # package_dir={"": "iconarray"},  # Optional
    packages=find_packages(
        exclude=["tests"],
    ),  # Required
    python_requires=">=3.7, <4",
    install_requires=[
        "cfgrib>=0.9.9.1",
        "xarray>=0.15",
        "psyplot",
        "psy-reg",
        "psy-simple",
        "psy-maps",
        "numpy",
        "six",
        "cartopy",
    ],  # Optional
    extras_require={
        "tests": ["flake8", "pytest"],
    },
)
