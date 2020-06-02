

def mapm(f, xs):
    """ mapm(print, [1,2,3])  """
    for x in xs:
        f(x)
    return True


def maplist(f, xs):
    """ newlist =  maplist(abs, [-1,-2])  """
    return [f(x) for x in xs]
