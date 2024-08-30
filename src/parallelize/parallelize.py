import multiprocess
from functools import wraps
from tqdm import tqdm
from types import FunctionType as function
import copy

def parallelize(func: function = None, **kwargs):
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

    n_threads = kwargs.get('n_threads', None)
    use_tqdm = kwargs.get('use_tqdm', False)
    enum = kwargs.get('enum', False)
    use_chunks = kwargs.get('use_chunks', False)
    setup_func = kwargs.get('setup_func', None)

    if func is None:
        return lambda f: parallelize(f, **kwargs)

    if n_threads is None:
        n_threads = multiprocess.cpu_count()

    # the idea behind this is that there might be some kind of object that is repeatedly used in the for loop
    # to prevent race conditions and memory locks, we chunk the data and pass deep copies of the object to each thread
    # this isn't done yet!!! been having issues testing it...
    if use_chunks:

        if use_tqdm:
            global pbars
            pbars = []
            for i in range(n_threads):
                pbars.append(tqdm(position=i, desc=f'Thread {i:<3}', leave=False))

        def operation(operation_data):
            chunk_i, lst = operation_data
            res = []

            if enum:
                lst = [(i,el) for i,el in enumerate(lst)]

            data = setup_func()
            lst = [(el,data) for i,el in enumerate(lst)]

            if use_tqdm:
                pbars[chunk_i].total = len(lst)

            for el in lst:
                res.append(func(el))
                if use_tqdm:
                    pbars[chunk_i].update()

            return res

        @wraps(func)
        def wrapper(data: list):

            with multiprocess.Pool(n_threads) as pool:
                arg_list = list(chunks(data, n_threads))
                arg_list = [(i,el) for i,el in enumerate(arg_list)] # get the chunk numbers (not enumerate)

                res = list(istarmap(pool, operation,  arg_list))
                res = [r for rs in res for r in rs] # flatten the list

            return res

        return wrapper

    @wraps(func)
    def wrapper(data: list):

        with multiprocess.Pool(n_threads) as pool:
            if enum: 
                data = [(i,el) for i,el in enumerate(data)]

            res = list(istarmap(pool, func, data, use_tqdm=use_tqdm))

        return res
    return wrapper


def chunks(l, n):
    for i in range(0, n):
        yield l[i::n]

def istarmap(pool, func: function, data: list, chunksize: int = 1, use_tqdm: bool = False):
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
        res = tqdm(pool.imap(func, data, chunksize), total=len(data))
    else:
        res = pool.imap(func, data, chunksize)
    
    for result in res:
        yield result