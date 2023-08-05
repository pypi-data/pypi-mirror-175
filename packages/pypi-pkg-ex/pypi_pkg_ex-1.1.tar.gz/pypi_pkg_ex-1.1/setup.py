import setuptools
from pathlib import Path

setuptools.setup(
    name="pypi_pkg_ex",
    version=1.1,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)

#  Generate a distribution package (IN BASH)
# python3 setup.py sdist bdist_wheel

# to upload
# twine upload dist/*