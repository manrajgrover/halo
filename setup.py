from setuptools import setup, find_packages # pylint: disable=no-name-in-module,import-error
import os

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = """
    Beautiful terminal spinners in Python. Find the documentation here: https://github.com/ManrajGrover/halo
    """

def dependencies(file):
    with open(file) as f:
        return f.read().splitlines()

setup(
    name='halo',
    packages=find_packages(exclude=('tests', 'examples')),
    version='0.0.3',
    license='MIT',
    description='Beautiful terminal spinners in Python',
    long_description=long_description,
    author='Manraj Singh',
    author_email='manrajsinghgrover@gmail.com',
    url='https://github.com/ManrajGrover/halo',
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
        "idle"
    ],
    install_requires=dependencies('requirements.txt'),
    tests_require=dependencies('requirements-dev.txt'),
    include_package_data=True
)
