"""
https://www.w3schools.com/python/python_try_except.asp

https://stackoverflow.com/questions/2083987/how-to-retry-after-exception

"""


def trys(func, *args, **kwargs):
    '''
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
        print(f'{trys.__name__}({func.__name__}(', args, kwargs, f')) ERROR: {error}')
    


def try_for(times, func, *args, **kwargs):
    '''
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
    trys(print, 'cat', 'dog', end='\n\n')
    try_for(3, print, 'cats', 'dogs', end='\n\n\n')
    
