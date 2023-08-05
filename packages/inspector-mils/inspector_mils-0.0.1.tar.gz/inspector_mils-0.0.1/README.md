# inspector_mils

[![CodeFactor](https://www.codefactor.io/repository/github/jmilagroso/inspector_mils/badge)](https://www.codefactor.io/repository/github/jmilagroso/inspector_mils)
[![travis](https://travis-ci.com/jmilagroso/pii_crypt.svg?branch=master)](https://travis-ci.com/jmilagroso/pii_crypt.svg?branch=master)
[![codecov](https://codecov.io/gh/jmilagroso/inspector_mils/branch/master/graph/badge.svg?token=HMC508346L)](https://codecov.io/gh/jmilagroso/inspector_mils)
[![python3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![python3.6](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![python3.6](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

Inspect functions' arguments and keywords arguments at runtime using decorator.

## Installation
To download inspector-mils, either fork this github repo or simply use Pypi via pip
```sh
pip install inspector-mils
```

## Usage
Import `inspect` decorator.
```sh
from inspector_mils.inspector import inspect
```

Add `@inspect` to your function.
```sh
@inspect
def my_func_sample1(a, b):
  pass

my_func_sample1("param1", "param2")
```
Output
```sh
[2022-11-04 02:42:45.151303] Starting inspect..
[2022-11-04 02:42:45.151888] my_func_sample1() called..
[2022-11-04 02:42:45.151937] args: ('param1', 'param2')
[2022-11-04 02:42:45.151978] kwargs: {}
[2022-11-04 02:42:45.152060] Ending inspect..
```

## License
MIT License

Copyright (c) 2022

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
