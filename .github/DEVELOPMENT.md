## Development

We need to clone the project and prepare the dev environment:

```bash
$ git clone https://github.com/manrajgrover/halo.git // or using ssh: git@github.com:manrajgrover/halo.git
$ cd halo
$ pip install -e .
```

This will install all requirements to use `halo`. You may want to create a virtual environment specifically for this.

To install development dependencies, run:

```bash
$ pip install -r requirements-dev.txt
```

#### Testing
Before submitting a pull request, make sure the code passes all the tests and is clean of lint errors:

```bash
$ tox
```

To run tests for specific environment, run:

1. For Python 2.7:

```bash
$ tox -e py27
```

2. For Python 3.6:

```bash
$ tox -e py36
```

For checking lint issues:

```bash
$ tox -e lint
```

### Building Documentation

To install documentation dependencies, run:

```bash
$ pip install -r requirements-docs.txt
```

To build the docs, change directories and then run the `html` make target:

```bash
$ cd docs
$ make html
```

Documentation will be located in `docs/build/html`.

#### Adding Documentation

After editing or adding to the module's docstrings, update the Sphinx documentation with `sphinx-apidoc`, 
clear the output directory, then rebuild the html pages:

```bash
$ sphinx-apidoc -f -o ./docs/source halo
$ cd docs
$ make clean
$ make html
``` 

#### Testing Documentation

Documentation testing is integrated with `tox`.

Simply run:

```bash
$ tox -e sphinx
```

If `linkcheck` fails, a list of broken external links will be located in `docs/build/linkcheck/output.txt`.
