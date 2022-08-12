from __future__ import annotations
import typing as t
from setuptools import find_packages, setup  # type: ignore
from packaging import version

import flake8_reassignment_checker

PACKAGE_NAME = "flake8_reassignment_checker"
SHORT_DESCRIPTION = "[WIP] Flake8 plugin that checks reassignment values."
AUTHOR_NAME = "RentalCat"
AUTHOR_EMAIL = "RentalCat"
URL = "https://github.com/RentalCat/flake8-reassignment-checker"
PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10"]

py_versions: list[version.Version] = [
    t.cast(version.Version, version.parse(v)) for v in PYTHON_VERSIONS
]


def get_long_description() -> str:
    with open("README.md") as f:
        return f.read()


def make_classifiers() -> t.Iterator[str]:
    yield "Development Status :: 1 - Planning"  # TODO fix to stable
    yield "Environment :: Console"
    yield "Framework :: Flake8"
    yield "Intended Audience :: Developers"
    yield "License :: OSI Approved :: MIT License"
    yield "Operating System :: OS Independent"
    # Programming Language: (python versions)
    yield "Programming Language :: Python"
    for py_major in {v.major for v in py_versions}:
        yield f"Programming Language :: Python :: {py_major}"
    for py_version in py_versions:
        yield f"Programming Language :: Python :: {py_version}"
    # Topic:
    yield "Topic :: Software Development :: Documentation"
    yield "Topic :: Software Development :: Libraries :: Python Modules"
    yield "Topic :: Software Development :: Quality Assurance"


setup(
    name=PACKAGE_NAME,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR_NAME,
    maintainer_email=AUTHOR_EMAIL,
    description=SHORT_DESCRIPTION,
    classifiers=list(make_classifiers()),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=f">={min(py_versions)}",
    include_package_data=True,
    keywords="flake8",
    version=flake8_reassignment_checker.__version__,
    install_requires=["setuptools", "flake8"],
    entry_points={"flake8.extension": [f"RAC = {PACKAGE_NAME}:ReassignmentChecker"]},
    url=URL,
    license="MIT",
    py_modules=[PACKAGE_NAME],
    zip_safe=False,
)
