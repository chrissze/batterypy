"""
https://www.w3schools.com/python/python_try_except.asp

https://stackoverflow.com/questions/2083987/how-to-retry-after-exception

"""

# STANDARD LIBS
from typing import Any, List, Optional

def try_none(func, *args, **kwargs) -> None:
    '''
    This function is a wrapper, it is suitbale for functions that returns None.
    If the function returns a Value, better to manually construct a try function.

    when I print arguments and keyword arguments in except block, 
    args without preceding star is a tuple, 
    kwargs without preceding single star is a dictionary.
    
    Successful example:
        trys(print, 'cat', 'dog', end='\n\n\n')

    Error example:
        trys(print, 'cats', en='\n\n\n')
        trys(print( cats en )) ERROR: 'en' is an invalid keyword argument for print()
    '''
    try:
        func(*args, **kwargs)
    except Exception as error:
        print(f'try_none({func.__name__}) ERROR: {error}')
        return None

def try_str(func, *args, **kwargs) -> str:
    '''
    This function is a wrapper, it is suitbale for functions that returns a string.

    Please note that the return value of the except block is also a string.
    '''
    try:
        func(*args, **kwargs)
    except Exception as error:
        return f'try_str({func.__name__}) ERROR: {error}'






def try_float(func, *args, **kwargs) -> float:
    '''
    This function is a wrapper, it is suitbale for functions that returns a float.

    '''
    try:
        func(*args, **kwargs)
    except Exception as error:
        print(f'try_float({func.__name__}) ERROR: {error}')
        return -1.0



def try_optional_float(func, *args, **kwargs) -> Optional[float]:
    '''
    This function is a wrapper, it is suitbale for functions that returns an optional float.

    '''
    try:
        func(*args, **kwargs)
    except Exception as error:
        print(f'try_optional_float({func.__name__}) ERROR: {error}')
        return None


def try_int(func, *args, **kwargs) -> int:
    '''
    This function is a wrapper, it is suitbale for functions that returns an int.

    '''
    try:
        func(*args, **kwargs)
    except Exception as error:
        print(f'try_int({func.__name__}) ERROR: {error}')
        return -1



def try_optional_int(func, *args, **kwargs) -> Optional[int]:
    '''
    This function is a wrapper, it is suitbale for functions that returns an optional int.

    '''
    try:
        func(*args, **kwargs)
    except Exception as error:
        print(f'try_optional_int({func.__name__}) ERROR: {error}')
        return None



    


def try_list(func, *args, **kwargs) -> List[Any]:
    '''
    This function is a wrapper, it is suitbale for functions that returns a list.

    '''
    try:
        func(*args, **kwargs)
    except Exception as error:
        print(f'try_int({func.__name__}) ERROR: {error}')
        return []


def try_for(times, func, *args, **kwargs) -> None:
    '''
    This try_for function is a wrapper, it is suitbale for functions that returns None.
    If the function returns a Value, it is best to manually construct the try function.

    Run a function multiple times in a try block, 
    Python does not allow putting times argument after **kwargs
    Successful example:
        try_for(4, print, 'cats', 'dogs', end='\n\n')  
    '''
    try:
        for i in range(times):
            func(*args, **kwargs)
    except Exception as error:
        print(f'{try_for.__name__}({times}, {func.__name__}(', *args, kwargs, f')) ERROR: {error}')


if __name__ == '__main__':
    try_none(print, 'cat', 'dog', end='\n\n')
    try_for(3, print, 'cats', 'dogs', end='\n\n\n')
    
