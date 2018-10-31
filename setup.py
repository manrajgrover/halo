from setuptools import setup, find_packages  # pylint: disable=no-name-in-module,import-error


setup(
    name='halo',
    packages=find_packages(exclude=('tests', 'examples')),
    include_package_data=True,
    version='0.0.18',
    license='MIT',
    description='Beautiful terminal spinners in Python',
    long_description='Beautiful terminal spinners in Python. Find the documentation here: https://github.com/ManrajGrover/halo',
    author='Manraj Singh',
    author_email='manrajsinghgrover@gmail.com',
    url='https://github.com/manrajgrover/halo',
    keywords=[
        'console',
        'loading',
        'indicator',
        'progress',
        'cli',
        'spinner',
        'spinners',
        'terminal',
        'term',
        'busy',
        'wait',
        'idle',
    ],
    install_requires=[
        'backports.shutil_get_terminal_size==1.0.0;python_version < "3.3"',
        'log_symbols==0.0.11',
        'spinners==0.0.23',
        'cursor==1.2.0',
        'termcolor==1.1.0',
        'colorama==0.3.9',
        'six==1.11.0',
    ],
    extras_require={
        'ipython': [
            'IPython==5.7.0',
            'ipywidgets==7.1.0',
        ],
        'test': [
            'coverage==4.4.1',
            'nose==1.3.7',
            'pylint==1.7.2',
            'tox==2.8.2',
        ],
        'dev': [
            'halo[test,ipython]',
        ],
    },
    tests_require=[
        'halo[test]',
    ],
)
