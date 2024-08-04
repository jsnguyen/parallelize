import time
import multiprocess
from functools import wraps
from tqdm import tqdm

def parallelize(func=None, pool_size=None, use_tqdm=False, enum=False):
    if func is None:
        return lambda f: parallelize(f, pool_size=pool_size, use_tqdm=use_tqdm, enum=enum)

    @wraps(func)
    def wrapper(iterator):
        with multiprocess.Pool(pool_size) as pool:
            if enum:
                arg_list = [(item,i) for i,item in enumerate(iterator)]
            else:
                arg_list = [item for item in iterator]

            res = list(istarmap(pool, func, arg_list, iterable_len=len(arg_list), use_tqdm=use_tqdm))

        return res
    return wrapper

def istarmap(pool, func, iterable, chunksize=1, use_tqdm=False, iterable_len=None):
    """
    function that combines the functionality of `imap` and `starmap`

    params:
        pool (multiprocessing.Pool): the pool of worker processes
        func (callable): the function to apply to the items
        iterable (iterable): an iterable of argument tuples
        chunksize (int, optional): the size of the chunks to split the iterable into
    
    yield:
        The results of the function applied to each item.
    """
    # Ensure the iterable is an iterator
    iterable = iter(iterable)
    
    # Apply the function to the chunks
    if use_tqdm:
        res = tqdm(pool.imap(func, iterable, chunksize), total=iterable_len)
    else:
        res = pool.imap(func, iterable, chunksize)
    
    # Yield the res as they become available
    for result in res:
        yield result
