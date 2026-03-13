import numpy as np
import plotly.graph_objects as go
import webbrowser

N = 45
extent = 2.4

x = np.linspace(-extent,extent,N)
y = np.linspace(-extent,extent,N)
z = np.linspace(-extent,extent,N)

X,Y,Z = np.meshgrid(x,y,z)

def torus_env(x,y,z,R=1.25,a=0.45):
    r = np.sqrt(x**2+y**2)
    return np.exp(-((r-R)**2 + z**2)/a)

def braid_field(x,y,z,phase):

    theta = np.arctan2(y,x)
    r = np.sqrt(x**2+y**2)+1e-6

    m1 = np.sin(4*theta + 2*z + phase)
    m2 = 0.6*np.sin(6*theta - 1.2*z - phase)

    spiral = 0.8*np.sin(3*np.log(r) + phase)

    return (m1+m2+spiral)*np.exp(-(r-0.6)**2)

frames=[]

phases=np.linspace(0,2*np.pi,27)

for p in phases:

    toroid = (
        torus_env(X,Y,Z+0.9)
        + 0.7*torus_env(X,Y,Z)
        + torus_env(X,Y,Z-0.9)
    )

    braid = braid_field(X,Y,Z,p)

    frames.append(
        go.Frame(
            data=[
                # transparent toroid shells
                go.Isosurface(
                    x=X.flatten(),
                    y=Y.flatten(),
                    z=Z.flatten(),
                    value=toroid.flatten(),
                    isomin=0.2,
                    isomax=0.9,
                    surface_count=2,
                    opacity=0.18,
                    colorscale="Blues",
                    caps=dict(x_show=False,y_show=False,z_show=False)
                ),

                # glowing braid tubes
                go.Isosurface(
                    x=X.flatten(),
                    y=Y.flatten(),
                    z=Z.flatten(),
                    value=braid.flatten(),
                    isomin=0.35,
                    isomax=0.9,
                    surface_count=2,
                    opacity=0.55,
                    colorscale="Plasma",
                    caps=dict(x_show=False,y_show=False,z_show=False)
                )
            ]
        )
    )

fig=go.Figure(data=frames[0].data,frames=frames)

fig.update_layout(
    title="Toroid Braid Field – Nakshatra Cycle",
    paper_bgcolor="black",
    scene=dict(
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False,
        bgcolor="black"
    ),
    updatemenus=[{
        "type":"buttons",
        "buttons":[
            {"label":"Play Cycle",
             "method":"animate",
             "args":[None,{"frame":{"duration":220}}]}
        ]
    }]
)

file="atlas_braid_nakshatra.html"

fig.write_html(file)

webbrowser.open(file)

print("3D braid viewer launched")

