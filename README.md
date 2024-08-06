# parallelize

This is a super simple package for adding decorators to parallelize your code easily. It is specifically designed for the case that you are running independent operations on a list of data. E.g. I have a list of data that need to be processed in some kind of way. The processing of these frames are independent of each other, and can be done in parallel. This package is not for any complicated kind of parallel processing, just the simple case of easily parallelizable for loops that occur frequently in data analysis.

Uses the `multiprocess` package (instead of `multiprocessing`), which overcomes the serialization limitations of `pickle` by using `dill` instead.

## Installation

```
git clone https://github.com/jsnguyen/parallelize.git
pip install ./parallelize
```

## Example

See [examples.py](./tests/examples.py) for more verbose versions of these examples.

Lets say you have the following for loop you want to parallelize:

``` python
data = [10**6] * 256
for el in data:
    res = sum(i * i for i in range(el))
```

On my computer, using a single thread, this takes ~8.5 seconds to run.

To parallelize this, we wrap the contents of the for loop in a function and use the `parallelize` decorator:

``` python
data = [10**6] * 256
@parallelize
def compute_heavy_task(val):
    res = sum(i * i for i in range(val))
    return res
```

By default, it will use parallelize across all available cores on your system.

`compute_heavy_task` now takes a list of values, rather than a single value. This list will be split amongst all the available threads. To run the parallelized version of the function:

``` python
res = compute_heavy_task(data)
```

This parallelized function takes only 0.5 seconds to run. `res` will be an ordered list of the function applied to the data.

## Function Arguments

Your function should only take one argument, an instance of the data being operated on. To avoid adding arguments to your function, define your function in line with the code so that it has access to all the local variables defined in your program.

## Other Features

It also supports `tqdm`:

``` python
@parallelize(use_tqdm=True)
def compute_heavy_task(val):
    res = sum(i * i for i in range(val))
    return res
res = compute_heavy_task(data)
```

This will print a progressbar of the parallelized function using `tqdm`.

If you need an index in your function, ie: your loop used `enumerate` you have to make sure your function now takes a tuple instead, with the second value in the tuple being the index.

This for loop:

``` python
for i,el in enumerate(data:)
    res = sum(i * i for i in range(el))
```
Turns into:

``` python
@parallelize(enum=True)
def compute_heavy_task(val_tuple):
    val, ii = val_tuple
    res = sum(i * i for i in range(val))
    return res
res = compute_heavy_task(data)
```