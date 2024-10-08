# parallelize

This is a super simple package for adding decorators to parallelize your code easily. It is specifically designed for the case that you are running independent operations on a list of data. E.g. I have a list of data that need to be processed in some kind of way. The processing of these frames are independent of each other, and can be done in parallel. This package is not for any complicated kind of parallel processing, just the simple case of easily parallelizable for loops that occur frequently in data analysis.

Uses the `multiprocess` package (instead of `multiprocessing`), which overcomes the serialization limitations of `pickle` by using `dill` instead.

## Installation

``` bash
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
from parallelize import parallelize
data = [10**6] * 256
@parallelize
def compute_heavy_task(val):
    res = sum(i * i for i in range(val))
    return res

res = compute_heavy_task(data)
```

`compute_heavy_task` now takes a *list of values*, rather than a single value. This list will be split amongst all the available threads. The list in the original for loop becomes the argument of the new, parallelized function.

This parallelized function takes only 0.5 seconds to run and `res` will be an *ordered list* of the function applied to the data.

By default, it will use all available cores on your system, but you can use the `n_threads` argument to set the number of threads.

### Note On Function Arguments

Your function should only take one argument, an instance of the data being operated on. To avoid adding arguments to your function, define your function in line with the code so that it has access to all the local variables defined in your program.

## Other Features

It also supports `tqdm`:

``` python
from parallelize import parallelize
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
from parallelize import parallelize
@parallelize(enum=True)
def compute_heavy_task(val_tuple):
    val, ii = val_tuple
    res = sum(i * i for i in range(val))
    return res
res = compute_heavy_task(data)
```

## Known Issues

If you get the error:

```
objc[28657]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
objc[28657]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
```

Seems to be an issue with parallelization on ARM-based Macs.

Change the following environment variable to fix this:

For bash:

``` bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

For fish:

``` fish
set -x OBJC_DISABLE_INITIALIZE_FORK_SAFETY YES
```

Add these lines to your `rc` file for persistence.
