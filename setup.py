from typing import Optional

from setuptools import find_packages, setup  # type: ignore

package_name = "flake8_reassignment_checker"


def get_version() -> Optional[str]:
    with open(f"{package_name}/__init__.py", "r") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split("=")[-1].strip().strip('"')
    return None


def get_long_description() -> str:
    with open("README.md") as f:
        return f.read()


setup(
    name=package_name,
    description="[WIP] Flake8 plugin that checks reassignment values.",
    classifiers=[
        "Environment :: Console",
        "Framework :: Flake8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    keywords="flake8",
    version=get_version(),
    author="RentalCat",
    author_email="RentalCat@users.noreply.github.com",
    install_requires=["setuptools"],
    entry_points={
        "flake8.extension": [f"RAC = {package_name}.checker:ReassignmentChecker"],
    },
    url="https://github.com/RentalCat/flake8-reassignment-checker",
    license="MIT",
    py_modules=[package_name],
    zip_safe=False,
)
