import numpy as np
import plotly.graph_objects as go
import webbrowser

N = 180
extent = 2.6

x = np.linspace(-extent,extent,N)
y = np.linspace(-extent,extent,N)
X,Y = np.meshgrid(x,y)

def torus_env(x,y,z,R,a):
    r = np.sqrt(x**2+y**2)
    return np.exp(-((r-R)**2 + z**2)/a)

def braid(x,y,z,phase,modeA,modeB,spiral):

    theta = np.arctan2(y,x)
    r = np.sqrt(x**2+y**2)+1e-6

    mode1 = np.sin(modeA*theta + 2*z + phase)
    mode2 = 0.6*np.sin(modeB*theta - 1.2*z - phase)

    spiral_term = spiral*np.sin(3*np.log(r) + phase)

    return (mode1+mode2+spiral_term)*np.exp(-(r-0.6)**2)


def generate_field(phase,modeA,modeB,spiral,center):

    z=0

    field = (
        torus_env(X,Y,z+0.9,1.25,0.45)
        + center*torus_env(X,Y,z,1.25,0.45)
        + torus_env(X,Y,z-0.9,1.25,0.45)
        + braid(X,Y,z,phase,modeA,modeB,spiral)
    )

    return field


frames=[]

for phase in np.linspace(0,2*np.pi,80):

    field=generate_field(phase,4,6,0.8,0.7)

    frames.append(
        go.Frame(
            data=[go.Contour(
                z=field,
                colorscale="Plasma",
                contours=dict(showlines=True)
            )]
        )
    )


fig=go.Figure(
    data=frames[0].data,
    frames=frames
)

fig.update_layout(
    title="Atlas Toroid Field Lab",
    paper_bgcolor="black",
    plot_bgcolor="black",
    updatemenus=[{
        "type":"buttons",
        "buttons":[
            {
                "label":"Play Field Evolution",
                "method":"animate",
                "args":[None,{"frame":{"duration":50}}]
            }
        ]
    }]
)

file="atlas_field_lab.html"

fig.write_html(file)

webbrowser.open(file)

print("Atlas Field Lab launched.")
