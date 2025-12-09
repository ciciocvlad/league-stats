def mymap(func, iterable):
    return list(filter(lambda x: x is not None, map(func, iterable)))

