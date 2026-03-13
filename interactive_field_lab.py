import numpy as np
import plotly.graph_objects as go
import webbrowser

N = 160
extent = 2.4

x = np.linspace(-extent,extent,N)
y = np.linspace(-extent,extent,N)
X,Y = np.meshgrid(x,y)

def torus_env(x,y,z,R=1.25,a=0.45):
    r = np.sqrt(x**2+y**2)
    return np.exp(-((r-R)**2 + z**2)/a)

def braid(x,y,z,phase,modeA,modeB):

    theta = np.arctan2(y,x)
    r = np.sqrt(x**2+y**2)+1e-6

    mode1 = np.sin(modeA*theta + 2*z + phase)
    mode2 = 0.6*np.sin(modeB*theta - 1.2*z - phase)

    spiral = 0.8*np.sin(3*np.log(r) + phase)

    return (mode1+mode2+spiral)*np.exp(-(r-0.6)**2)

frames=[]

z=0

for phase in np.linspace(0,2*np.pi,60):

    field = (
        torus_env(X,Y,z+0.9)
        + 0.7*torus_env(X,Y,z)
        + torus_env(X,Y,z-0.9)
        + braid(X,Y,z,phase,4,6)
    )

    frames.append(
        go.Frame(
            data=[go.Contour(
                z=field,
                colorscale="Plasma"
            )]
        )
    )

fig = go.Figure(
    data=frames[0].data,
    frames=frames
)

fig.update_layout(
    title="Toroid Field Lab",
    paper_bgcolor="black",
    plot_bgcolor="black",
    updatemenus=[{
        "type":"buttons",
        "buttons":[
            {"label":"Animate",
             "method":"animate",
             "args":[None]}
        ]
    }]
)

file="field_lab.html"

fig.write_html(file)

webbrowser.open(file)

print("Interactive viewer launched.")
