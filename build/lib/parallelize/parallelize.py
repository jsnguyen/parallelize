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

        with multiprocess.Pool(n_threads) as pool:
            if enum:
                arg_list = [(el,i) for i,el in enumerate(data)]
            else:
                arg_list = data

            res = list(istarmap(pool, func, arg_list, data_len=len(arg_list), use_tqdm=use_tqdm))

        return res
    return wrapper

def istarmap(pool, func: function, data: list, chunksize: int = 1, use_tqdm: bool = False, data_len: int = None):
    """
    function that combines of imap and starmap

    args:
        pool (multiprocessing.Pool): the pool of worker processes
        func (callable): the function to apply to the items
        data (iterable): list of argument tuples
        chunksize (int, optional): the size of the chunks to split the data into
    
    yields:
        the results of the function applied to each item
    """

    if use_tqdm:
        res = tqdm(pool.imap(func, data, chunksize), total=data_len)
    else:
        res = pool.imap(func, data, chunksize)
    
    for result in res:
        yield result