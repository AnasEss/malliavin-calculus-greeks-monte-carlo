import numpy as np

def brownian_motion(T,m):
    
    dt = 1/m
    G = np.random.normal(size=m) * np.sqrt(dt)
    return np.cumsum(G)