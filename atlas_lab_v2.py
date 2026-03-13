import numpy as np
import pyvista as pv

plotter = pv.Plotter(window_size=(1600,900))
plotter.set_background("black")

# -------------------
# parameters
# -------------------

R = 1.2
phase = 0
twist = 3
particles_n = 600

actors = []

# -------------------
# 3-body toroid field
# -------------------

def field(x,y,z):

    r = np.sqrt(x*x+y*y)+1e-6
    theta = np.arctan2(y,x)

    # toroid 1
    vx1 = -y
    vy1 = x
    vz1 = np.sin(theta*twist + phase)

    # toroid 2 (counter)
    vx2 = y*0.7
    vy2 = -x*0.7
    vz2 = np.cos(theta*twist + phase)

    # center stabilizer
    vx3 = -0.4*x
    vy3 = -0.4*y
    vz3 = 0.3*np.sin(z*3 + phase)

    return np.array([
        vx1+vx2+vx3,
        vy1+vy2+vy3,
        vz1+vz2+vz3
    ])

# -------------------
# particles
# -------------------

particles = np.random.randn(particles_n,3)*0.7

# -------------------
# streamlines
# -------------------

def make_streamlines():

    seeds = pv.PolyData(
        np.random.randn(80,3)*0.7
    )

    grid = pv.ImageData(
        dimensions=(25,25,25),
        spacing=(0.18,0.18,0.18),
        origin=(-2,-2,-2)
    )

    vec = []

    for p in grid.points:
        vec.append(field(p[0],p[1],p[2]))

    grid["vectors"] = np.array(vec)

    streams = grid.streamlines_from_source(
        seeds,
        vectors="vectors",
        max_time=200,
        integration_direction="both"
    )

    return streams

# -------------------
# mandala slice
# -------------------

def mandala_slice(normal):

    plane = pv.Plane(i_size=4,j_size=4,direction=normal)

    vals=[]

    for p in plane.points:
        vals.append(np.linalg.norm(field(p[0],p[1],p[2])))

    plane["energy"]=vals

    return plane

# -------------------
# rebuild scene
# -------------------

def rebuild():

    global actors

    for a in actors:
        plotter.remove_actor(a)

    actors=[]

    torus1 = pv.ParametricTorus(R,0.25)
    torus2 = pv.ParametricTorus(R*0.8,0.18)

    actors.append(plotter.add_mesh(torus1,color="cyan",opacity=0.07))
    actors.append(plotter.add_mesh(torus2,color="cyan",opacity=0.05))

    streams = make_streamlines()

    actors.append(plotter.add_mesh(streams,line_width=3))

    pdata = pv.PolyData(particles)

    actors.append(
        plotter.add_points(
            pdata,
            color="yellow",
            point_size=6,
            render_points_as_spheres=True
        )
    )

    for n in [(0,0,1),(1,0,0),(0,1,0)]:

        s = mandala_slice(n)

        actors.append(
            plotter.add_mesh(
                s,
                scalars="energy",
                cmap="plasma",
                opacity=0.85
            )
        )

    plotter.render()

# -------------------
# evolution
# -------------------

def evolve():

    global particles,phase

    for i,p in enumerate(particles):

        v = field(p[0],p[1],p[2])

        particles[i]+=v*0.02

    phase += 0.03

    rebuild()

# -------------------
# sliders
# -------------------

def twist_slider(val):
    global twist
    twist = int(val)
    rebuild()   # immediately update the scene

plotter.add_slider_widget(
    twist_slider,
    rng=[1,10],
    value=twist,
    title="Twist",
    pointa=(0.02,0.1),
    pointb=(0.3,0.1),
    style="modern"
))

# -------------------
# gif export
# -------------------

def export():

    plotter.open_gif("atlas_flight.gif")

    for i in range(200):
        evolve()
        plotter.write_frame()

    plotter.close()

plotter.add_key_event("g", export)

plotter.add_key_event("space", evolve)

plotter.add_text(
"SPACE = evolve | G = export GIF",
font_size=12
)

rebuild()

plotter.camera_position="iso"

plotter.show()
