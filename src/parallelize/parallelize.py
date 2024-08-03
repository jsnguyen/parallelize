import multiprocess
from functools import wraps
from tqdm import tqdm

def parallelize(iterator, pool_size=None, use_tqdm=False, enum=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use multiprocessing.Pool to parallelize the tasks
            with multiprocess.Pool(pool_size) as pool:
                # Use starmap to pass multiple arguments to the function
                if enum:
                    arg_list = [(item,i) for i,item in enumerate(iterator)]
                else:
                    arg_list = [item for item in iterator]

                results = list(istarmap(pool, func, arg_list, iterable_len=len(arg_list), use_tqdm=use_tqdm))

            return results
        return wrapper
    return decorator

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
        results = tqdm(pool.imap(func, iterable, chunksize), total=iterable_len)
    else:
        results = pool.imap(func, iterable, chunksize)
    
    # Yield the results as they become available
    for result in results:
        yield result
