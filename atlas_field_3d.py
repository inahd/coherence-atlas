import numpy as np
import plotly.graph_objects as go
import webbrowser

N = 60
extent = 2.4

x = np.linspace(-extent,extent,N)
y = np.linspace(-extent,extent,N)
z = np.linspace(-extent,extent,N)

X,Y,Z = np.meshgrid(x,y,z)

def torus_env(x,y,z,R=1.25,a=0.45):
    r = np.sqrt(x**2+y**2)
    return np.exp(-((r-R)**2 + z**2)/a)

def braid(x,y,z,phase):

    theta = np.arctan2(y,x)
    r = np.sqrt(x**2+y**2)+1e-6

    m1 = np.sin(4*theta + 2*z + phase)
    m2 = 0.6*np.sin(6*theta - 1.2*z - phase)

    spiral = 0.8*np.sin(3*np.log(r) + phase)

    return (m1+m2+spiral)*np.exp(-(r-0.6)**2)

phase = 0

field = (
    torus_env(X,Y,Z+0.9)
    + 0.7*torus_env(X,Y,Z)
    + torus_env(X,Y,Z-0.9)
    + braid(X,Y,Z,phase)
)

fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=field.flatten(),
    isomin=0.2,
    isomax=0.9,
    surface_count=4,
    colorscale="Plasma",
    caps=dict(x_show=False,y_show=False,z_show=False)
))

fig.update_layout(
    title="Atlas Toroid Field (3D)",
    scene=dict(
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False,
        bgcolor="black"
    ),
    paper_bgcolor="black"
)

file="atlas_field_3d.html"

fig.write_html(file)

webbrowser.open(file)

print("3D field viewer launched")
