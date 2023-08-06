# Savescreen

[![PyPI](https://img.shields.io/pypi/v/savescreen)](https://pypi.python.org/pypi/savescreen)
[![Pypi - License](https://img.shields.io/github/license/codesrg/savescreen)](https://github.com/codesrg/savescreen/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/savescreen?color=red)](https://pypi.python.org/pypi/savescreen)

To take and save screenshot.

## Installation

`pip install -U savescreen`

## Usage

```
usage: savescreen [options]

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show version number and exit

to take screenshot:
  -n , --name      name to screenshot
  -p , --path      path to save screenshot (default : path)
  -f , --format    image format to save screenshot (default : png)
  -t , --timeout   timeout period before taking screenshot in secs (default : 5s)
  -d , --display   to display the screenshot (default : False)
```

### Python Script
To encrypt/decrypt message using rsa.

```python
from savescreen import Screenshot

screenshot = Screenshot(name='shot', img_format='png')
screenshot.take() # to take screenshot
screenshot.save() # to save the screenshot
screenshot.display() # to display screenshot
```

### Command Line
To take and save screenshot in png format.
```commandline
$ savescreen --name shot --format png
Screenshot saved in '.../shot.png'.
```
###

To take and save screenshot after 30 secs.

```commandline
$ savescreen --name shot --format png --timeout 30
Screenshot saved in '.../shot.png'.
```

## Issues:

If you encounter any problems, please file an [issue](https://github.com/codesrg/savescreen/issues) along with a detailed description.