<h1 align="center">
  <img src="https://raw.githubusercontent.com/manrajgrover/halo/master/art/halo.png" height="50px"/>
  <br>
  halo
</h1>

[![Build Status](https://travis-ci.com/manrajgrover/halo.svg?branch=master)](https://travis-ci.com/manrajgrover/halo) [![Build status](https://ci.appveyor.com/api/projects/status/wa6t414gltr403ff?svg=true)](https://ci.appveyor.com/project/manrajgrover/halo) [![Coverage Status](https://coveralls.io/repos/github/manrajgrover/halo/badge.svg?branch=master)](https://coveralls.io/github/manrajgrover/halo?branch=master)
 [![PyPI](https://img.shields.io/pypi/v/halo.svg)](https://github.com/manrajgrover/halo) ![awesome](https://img.shields.io/badge/awesome-yes-green.svg) [![Downloads](https://pepy.tech/badge/halo)](https://pepy.tech/project/halo) [![Downloads](https://pepy.tech/badge/halo/month)](https://pepy.tech/project/halo/month)
> Beautiful spinners for terminal, IPython and Jupyter

![halo](https://raw.github.com/manrajgrover/halo/master/art/doge_spin.svg?sanitize=true)

## Install

```shell
$ pip install halo
```

## Usage

```py
from halo import Halo

spinner = Halo(text='Loading', spinner='dots')
spinner.start()

# Run time consuming work here
# You can also change properties for spinner as and when you want

spinner.stop()
```

Alternatively, you can use halo with Python's `with` statement:

```py
from halo import Halo

with Halo(text='Loading', spinner='dots'):
    # Run time consuming work here
```

Finally, you can use halo as a decorator:

```py
from halo import Halo

@Halo(text='Loading', spinner='dots')
def long_running_function():
    # Run time consuming work here
    pass

long_running_function()
```

## API

#### `Halo([text|text_color|spinner|animation|placement|color|interval|stream|enabled])`

##### `text`
*Type*: `str`

Text shown along with spinner.

##### `text_color`
*Type*: `str`
*Values*: `grey`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`

Color of the spinner text. Defaults to `None`.

##### `spinner`
*Type*: `str|dict`

If string, it should be one of the spinners listed in the given [json](https://github.com/sindresorhus/cli-spinners/blob/dac4fc6571059bb9e9bc204711e9dfe8f72e5c6f/spinners.json) file. If a dict is passed, it should define `interval` and `frames`. Something like:

```py
{
    'interval': 100,
    'frames': ['-', '+', '*', '+', '-']
}
```

Defaults to `dots` spinner. For Windows users, it defaults to `line` spinner.

##### `animation`
*Type*: `str`
*Values*: `bounce`, `marquee`

Animation to apply to the text if it's too large and doesn't fit in the terminal. If no animation is defined, the text will be ellipsed.

##### `placement`
*Type*: `str`
*Values*: `left`, `right`

Which side of the text the spinner should be displayed. Defaults to `left`

##### `color`
*Type*: `str`
*Values*: `grey`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`

Color of the spinner. Defaults to `cyan`.

##### `interval`
*Type*: `float`

Interval between each frame. Defaults to spinner interval (recommended).

##### `stream`
*Type*: `file`

Stream to write the output. Defaults to `sys.stdout`.

##### `enabled`
*Type*: `bool`

Enable or disable the spinner. Defaults to `True`.

### Methods

Following are the methods available:

#### `spinner.start([text])`

Starts the spinner. If `text` is passed, it is set as spinner text. Returns the instance.

#### `spinner.stop()`

Stops and clears the spinner. Returns the instance.

#### `spinner.clear()`

Clears the spinner. Returns the instance.

#### `spinner.render()`

Manually renders a new frame. Returns the instance.

#### `spinner.frame()`

Returns next frame to be rendered.

#### `spinner.succeed([text])`
##### `text`: *Type*: `str`

Stops the spinner and changes symbol to `✔`. If text is provided, it is persisted else current text is persisted. Returns the instance.

#### `spinner.fail([text])`
##### `text`: *Type*: `str`

Stops the spinner and changes symbol to `✖`. If text is provided, it is persisted else current text is persisted. Returns the instance.

#### `spinner.warn([text])`
##### `text`: *Type*: `str`

Stops the spinner and changes symbol to `⚠`. If text is provided, it is persisted else current text is persisted. Returns the instance.

#### `spinner.info([text])`
##### `text`: *Type*: `str`

Stops the spinner and changes symbol to `ℹ`. If text is provided, it is persisted else current text is persisted. Returns the instance.

#### `spinner.stop_and_persist([symbol|text])`
Stops the spinner and changes symbol and text. Returns the instance.

##### `symbol`
*Type*: `str`

Symbol to replace the spinner with. Defaults to `' '`.

##### `text`
*Type*: `str`

Text to be persisted. Defaults to instance text.

![Persist spin](https://raw.github.com/manrajgrover/halo/master/art/persist_spin.svg?sanitize=true)

#### `spinner.text`
Change the text of spinner.

#### `spinner.color`
Change the color of spinner

#### `spinner.spinner`
Change the spinner itself.

#### `spinner.enabled`
Enable or disable the spinner.

## How to contribute?

Please see [Contributing guidelines](https://github.com/manrajgrover/halo/blob/master/.github/CONTRIBUTING.md) for more information.

## Like it?

🌟 this repo to show support. Let me know you liked it on [Twitter](https://twitter.com/manrajsgrover).
Also, share the [project](https://twitter.com/intent/tweet?url=https%3A%2F%2Fgithub.com%2Fmanrajgrover%2Fhalo&via=manrajsgrover&text=Checkout%20%23halo%20-%20a%20beautiful%20%23terminal%20%23spinners%20library%20for%20%23python&hashtags=github%2C%20pypi).

## Related

* [py-spinners](https://github.com/manrajgrover/py-spinners) - Spinners in Python
* [py-log-symbols](https://github.com/manrajgrover/py-log-symbols) - Log Symbols in Python
* [ora](https://github.com/sindresorhus/ora) - Elegant terminal spinners in JavaScript (inspiration behind this project) 

## License
[MIT](https://github.com/manrajgrover/halo/blob/master/LICENSE) © Manraj Singh
