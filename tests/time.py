import time 

def timeit(method):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time() - start_time
        print(end_time) 
        return result
    return timed


