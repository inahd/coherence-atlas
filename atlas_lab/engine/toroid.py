import numpy as np


def generate_toroid(R=1.2, r=0.35):

    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, 2*np.pi, 30)

    u, v = np.meshgrid(u, v)

    x = (R + r*np.cos(v)) * np.cos(u)
    y = (R + r*np.cos(v)) * np.sin(u)
    z = r*np.sin(v)

    return x, y, z
