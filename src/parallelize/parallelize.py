import time
import multiprocess
from functools import wraps
from tqdm import tqdm
from types import FunctionType as function

def parallelize(func: function = None, n_threads: int = None, use_tqdm: bool = False, enum: bool = False):
    '''
    function or decorator that automatically parallelizes a function

    args:
        func: function to be parallelized
        n_threads: number of processes to be spawned by the pool, typically equal to the number of cores on your machine
                   if left none, then it will use the maximum amount allowed on your machine
        use_tqdm: make a progressbar using tqdm
        enum: if the function needs an index, add an integer counter to be passed to the function
              useful in the case that the order of your data matters, or for saving data later

    returns:
        the return value of your function, in the form of a list

    '''

    if func is None:
        return lambda f: parallelize(f, n_threads=n_threads, use_tqdm=use_tqdm, enum=enum)

    @wraps(func)
    def wrapper(data: list):
        '''
        args:
            data: a list of the data
        '''

        with multiprocess.Pool(n_threads) as pool:
            if enum:
                arg_list = [(el,i) for i,el in enumerate(data)]
            else:
                arg_list = data

            res = list(istarmap(pool, func, arg_list, iterable_len=len(arg_list), use_tqdm=use_tqdm))

        return res
    return wrapper

def istarmap(pool, func, iterable, chunksize=1, use_tqdm=False, iterable_len=None):
    """
    function that combines of imap and starmap

    args:
        pool (multiprocessing.Pool): the pool of worker processes
        func (callable): the function to apply to the items
        iterable (iterable): an iterable of argument tuples
        chunksize (int, optional): the size of the chunks to split the iterable into
    
    yields:
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
