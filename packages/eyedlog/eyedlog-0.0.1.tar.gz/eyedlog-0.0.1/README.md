# coloredlog

A tool to make the log display more elegant.

## Installation

```shell
pip install eyedlog
```

## Usage

Recommended usage

```python
from readablelog import get_logger
logger = get_logger('pretty.log')
logger.info('some text')
```

Advanced usage

```python
from readablelog import ColoredLogger
logger = ColoredLogger('pretty.log')
logger.info('some text')
```
