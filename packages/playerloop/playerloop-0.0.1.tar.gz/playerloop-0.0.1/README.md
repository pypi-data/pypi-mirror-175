# playerloop-python

[![license](https://img.shields.io/pypi/l/playerloop.svg)](./LICENSE)
[![pypi version](https://img.shields.io/pypi/v/playerloop.svg)](https://pypi.org/project/playerloop/)
[![PyPI status](https://img.shields.io/pypi/status/playerloop.svg)](https://github.com/daelonsuzuka/playerloop-python)

Get bug reports from your users, fast. Improve your Python application, reward the community. 

# Installation

```sh 
pip install playerloop
```

# Usage

```py
from playerloop import PlayerLoop

key = '<your api key>'

pl = PlayerLoop(key, 'test_app')
pl.send_report('test report please ignore')
```