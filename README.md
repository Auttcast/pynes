```
pip install pynes (todo)
```

## Hack your console with Pynes
An easy-to-use api for accessing python's sys.stdio and sys.stderr streams. Consistently line-buffered with asynchronous support.

Pynes has built-in support for windows with the msvcrt library.
-acC

### Write to std io

```python
from pynes.core import Writer

def synchronousWriter():
  writeline = Writer().createStdIoWriter()
  writeline("hello io")

async def asynchronousWriter():
  writeline = Writer().createStdIoWriterAsync()
  await writeline("hello io")

```

### Read from std io

```python
from pynes.core import Reader

def synchronousReader():
  readline = Reader().create()
  for line in readline:
    print(line)

async def asynchronousReader():
  readline = await Reader().createAsync()
  async for line in readline():
    print(line)

```

### Combine commands

```python

```


### Built on 
Python 3.12.8
pytest 8.3.4
