import numpy as np


def generate_braid(strands=6, twist=2, radius=1.0):

    t = np.linspace(0,20,800)

    curves = []

    for i in range(strands):

        phase = i * (2*np.pi/strands)

        r = radius + 0.2*np.sin(twist*t + phase)

        x = r*np.cos(t)
        y = r*np.sin(t)
        z = 0.5*np.sin(twist*t + phase)

        curves.append((x,y,z))

    return curves
