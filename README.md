# parallelize

This is a super simple package for adding decorators to parallelize your code easily. It is specifically designed for the case that you are running independent operations on an array of data.

Example:

Lets say you have the following for loop you want to parallelize:

```
data = [10**6] * 256
for el in data:
    res = sum(i * i for i in range(el))
```

On my computer, using a single thread, this takes ~8.5 seconds to run.

To parallelize this, we wrap the contents of the `for` loop in a function and use the `parallelize` decorator:

```
data = [10**6] * 256
@parallelize
def compute_heavy_task(val):
    res = sum(i * i for i in range(val))
    return res
```

`compute_heavy_task` now takes a list of values, rather than a single value. This list will be split amongst all the available threads. To run the parallelized version of the function:

```
res = compute_heavy_task(data)
```

`res` will be an ordered list of the function applied to the data.

See [examples.py](./tests/examples.py) for more examples.