# halo
[![Build Status](https://travis-ci.org/ManrajGrover/halo.svg?branch=master)](https://travis-ci.org/ManrajGrover/halo) [![Build status](https://ci.appveyor.com/api/projects/status/wa6t414gltr403ff?svg=true)](https://ci.appveyor.com/project/ManrajGrover/halo)
 [![PyPI](https://img.shields.io/pypi/v/halo.svg)](https://github.com/ManrajGrover/halo) ![awesome](https://img.shields.io/badge/awesome-yes-green.svg)
> Beautiful terminal spinners in Python

## Install

```shell
$ pip install halo
```

## Usage

```py
from halo.halo import Halo

spinner = Halo({'text': 'Loading', 'spinner': 'dots'})
spinner.start()

# Run time consuming work here
# You can also change properties for spinner as and when you want

spinner.stop()
```

## To Do

- [ ] [Support Windows](https://github.com/ManrajGrover/halo/issues/5)

## Like it?

:star2: this repo to show support. 

## Related

* [py-spinners](https://github.com/ManrajGrover/py-spinners)
* [py-log-symbols](https://github.com/ManrajGrover/py-log-symbols)
* [ora](https://github.com/sindresorhus/ora)


## License
[MIT](https://github.com/ManrajGrover/halo/blob/master/LICENSE) © Manraj Singh
