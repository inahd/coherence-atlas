import numpy as np
import pyvista as pv


def generate_braid(strands=6, twist=2, radius=1.0):

    t = np.linspace(0, 20, 800)

    curves = []

    for i in range(strands):

        phase = i * (2*np.pi/strands)

        r = radius + 0.2*np.sin(twist*t + phase)

        x = r*np.cos(t)
        y = r*np.sin(t)
        z = 0.5*np.sin(twist*t + phase)

        curves.append(np.column_stack((x, y, z)))

    return curves


def build_torus(radius=1.0):

    return pv.ParametricTorus(
        ringradius=radius,
        crosssectionradius=0.25
    )


plotter = pv.Plotter()

actors = []
torus_actor = None


def rebuild(strands=6, twist=2, radius=1.0):

    global actors, torus_actor

    for a in actors:
        plotter.remove_actor(a)

    actors.clear()

    if torus_actor:
        plotter.remove_actor(torus_actor)

    curves = generate_braid(strands, twist, radius)

    for c in curves:

        spline = pv.Spline(c, 800)

        actor = plotter.add_mesh(
            spline,
            line_width=4,
            color="orange"
        )

        actors.append(actor)

    torus = build_torus(radius)

    torus_actor = plotter.add_mesh(
        torus,
        opacity=0.25,
        color="cyan"
    )


rebuild()

plotter.add_slider_widget(
    lambda v: rebuild(int(v), 2, 1.0),
    [3, 18],
    value=6,
    title="Strands"
)

plotter.add_slider_widget(
    lambda v: rebuild(6, int(v), 1.0),
    [1, 6],
    value=2,
    title="Twist"
)

plotter.add_slider_widget(
    lambda v: rebuild(6, 2, v),
    [0.5, 2.0],
    value=1.0,
    title="Radius"
)

plotter.show()
