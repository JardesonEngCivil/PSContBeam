from numpy import abs

def erro_percentual(exato, aproximado):
    
    return abs(exato - aproximado) / exato * 100
