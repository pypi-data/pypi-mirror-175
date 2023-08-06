# nr.stream

Provides a useful `Stream` and `Optional` class.

```py
from nr.stream import Stream

values = [3, 6, 4, 7, 1, 2, 5]
assert list(Stream(values).chunks(values, 3, fill=0).map(sum)) == [13, 10, 5]
```
