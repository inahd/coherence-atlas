import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio

# resolution
N = 220
frames = 160

x = np.linspace(-2.2, 2.2, N)
y = np.linspace(-2.2, 2.2, N)
X, Y = np.meshgrid(x, y)


def torus_env(x, y, z, R=1.25, a=0.45):
    r = np.sqrt(x**2 + y**2)
    return np.exp(-((r - R)**2 + z**2) / a)


def braid(x, y, z, phase):
    theta = np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2) + 1e-6

    mode1 = np.sin(4 * theta + 2 * z + phase)
    mode2 = 0.6 * np.sin(6 * theta - 1.2 * z - phase)
    spiral = 0.8 * np.sin(3 * np.log(r) + phase)

    return (mode1 + mode2 + spiral) * np.exp(-(r - 0.6) ** 2)


images = []

for i in range(frames):
    t = i * 0.12

    # spiral path through field
    z = np.sin(t) * 1.2
    x_shift = 0.5 * np.cos(t)
    y_shift = 0.5 * np.sin(t)

    # rotate toroids slowly
    angle = 0.25 * t
    Xr = (X + x_shift) * np.cos(angle) - (Y + y_shift) * np.sin(angle)
    Yr = (X + x_shift) * np.sin(angle) + (Y + y_shift) * np.cos(angle)

    # 3-body convolution version: upper + middle + lower toroids + braid
    field = (
        torus_env(Xr, Yr, z + 0.9)
        + 0.7 * torus_env(Xr, Yr, z)
        + torus_env(Xr, Yr, z - 0.9)
        + braid(Xr, Yr, z, t)
    )

    fig, ax = plt.subplots(figsize=(6, 6), facecolor="black")

    m = np.max(np.abs(field))
    levels = np.linspace(-0.65 * m, 0.65 * m, 22)

    ax.contour(field, levels=levels, cmap="plasma", linewidths=1.2)
    ax.axis("off")
    ax.set_title("Toroid Field Spacetime Travel (3-body)", color="white")

    fname = f"_travel_{i:03d}.png"
    fig.savefig(fname, bbox_inches="tight", pad_inches=0.03, facecolor="black")
    plt.close(fig)

    images.append(imageio.imread(fname))

imageio.mimsave("spacetime_travel.gif", images, duration=0.07)
print("Created spacetime_travel.gif")
