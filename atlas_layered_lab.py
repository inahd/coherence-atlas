import numpy as np
import pyvista as pv

plotter = pv.Plotter(window_size=(1600,900))
plotter.set_background("black")

# -------------------------
# parameters
# -------------------------

R = 1.2
phase = 0.0
nakshatra_phase = 0.0
particles_n = 500

actors = []

# -------------------------
# vector field
# -------------------------

def field(x,y,z):

    r = np.sqrt(x*x+y*y)+1e-6
    theta = np.arctan2(y,x)

    # base toroidal circulation
    vx = -y
    vy = x

    # poloidal component
    vz = 0.6*np.sin(theta*6 + phase)

    # second toroid interaction
    vx += 0.4*np.sin(z*3 + phase)
    vy += 0.4*np.cos(z*3 + phase)

    # nakshatra modulation
    mod = np.sin(theta*27 + nakshatra_phase)

    vx += 0.3*mod*np.cos(theta)
    vy += 0.3*mod*np.sin(theta)

    return np.array([vx,vy,vz])

# -------------------------
# streamlines
# -------------------------

def make_streamlines():

    pts=[]

    for i in range(60):

        t=np.random.rand()*2*np.pi
        r=R+np.random.randn()*0.15

        pts.append([
            r*np.cos(t),
            r*np.sin(t),
            np.random.randn()*0.3
        ])

    seeds=pv.PolyData(np.array(pts))

    grid=pv.ImageData(
        dimensions=(25,25,25),
        spacing=(0.18,0.18,0.18),
        origin=(-2.2,-2.2,-2.2)
    )

    vec=[]

    for p in grid.points:
        vec.append(field(p[0],p[1],p[2]))

    grid["vectors"]=np.array(vec)

    streams=grid.streamlines_from_source(
        seeds,
        vectors="vectors",
        max_time=300,
        integration_direction="both"
    )

    return streams

# -------------------------
# mandala slice
# -------------------------

def mandala_slice(normal):

    plane=pv.Plane(i_size=4,j_size=4,direction=normal)

    vals=[]

    for p in plane.points:
        v=field(p[0],p[1],p[2])
        vals.append(np.linalg.norm(v))

    plane["energy"]=vals

    return plane

# -------------------------
# particles
# -------------------------

particles=np.random.randn(particles_n,3)*0.6

# -------------------------
# rebuild scene
# -------------------------

def rebuild():

    global actors

    for a in actors:
        plotter.remove_actor(a)

    actors=[]

    # toroid shells

    torus1=pv.ParametricTorus(R,0.25)
    torus2=pv.ParametricTorus(R*0.8,0.18)

    actors.append(
        plotter.add_mesh(torus1,color="cyan",opacity=0.07)
    )

    actors.append(
        plotter.add_mesh(torus2,color="cyan",opacity=0.05)
    )

    # streamlines

    streams=make_streamlines()

    actors.append(
        plotter.add_mesh(
            streams,
            line_width=3
        )
    )

    # particles

    pdata=pv.PolyData(particles)

    actors.append(
        plotter.add_points(
            pdata,
            color="yellow",
            point_size=7,
            render_points_as_spheres=True
        )
    )

    # slices

    for n in [(0,0,1),(1,0,0),(0,1,0)]:

        s=mandala_slice(n)

        actors.append(
            plotter.add_mesh(
                s,
                scalars="energy",
                cmap="plasma",
                opacity=0.85
            )
        )

    plotter.render()

# -------------------------
# evolution loop
# -------------------------

def evolve():

    global particles,phase,nakshatra_phase

    for i,p in enumerate(particles):

        v=field(p[0],p[1],p[2])

        particles[i]+=v*0.02

    phase+=0.03
    nakshatra_phase+=0.01

    rebuild()

# -------------------------
# animation timer
# -------------------------

def tick():

    evolve()

plotter.add_text(
"Atlas Field Lab — rotating toroidal field",
font_size=12
)

rebuild()

plotter.camera_position = "iso"

plotter.show(auto_close=False)

# continuous animation loop
while True:
    evolve()
    plotter.update()
