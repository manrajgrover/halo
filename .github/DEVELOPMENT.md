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
