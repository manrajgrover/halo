import io
from setuptools import (
    setup,
    find_packages,
)  # pylint: disable=no-name-in-module,import-error


def dependencies(file):
    with open(file) as f:
        return f.read().splitlines()


with io.open("README.md", encoding="utf-8") as infile:
    long_description = infile.read()

setup(
    name="halo",
    packages=find_packages(exclude=("tests", "examples")),
    version="0.0.31",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.4",
    description="Beautiful terminal spinners in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Manraj Singh",
    author_email="manrajsinghgrover@gmail.com",
    url="https://github.com/manrajgrover/halo",
    keywords=[
        "console",
        "loading",
        "indicator",
        "progress",
        "cli",
        "spinner",
        "spinners",
        "terminal",
        "term",
        "busy",
        "wait",
        "idle",
    ],
    install_requires=dependencies("requirements.txt"),
    tests_require=dependencies("requirements-dev.txt"),
    include_package_data=True,
    extras_require={"ipython": ["IPython==5.7.0", "ipywidgets==7.1.0",]},
)
