import numpy as np
import plotly.graph_objects as go
import webbrowser

N = 140
extent = 2.4

x = np.linspace(-extent,extent,N)
y = np.linspace(-extent,extent,N)
X,Y = np.meshgrid(x,y)

def torus_env(x,y,z,R=1.25,a=0.45):
    r=np.sqrt(x**2+y**2)
    return np.exp(-((r-R)**2 + z**2)/a)

def braid(x,y,z,phase,modeA,modeB,spiral):

    theta=np.arctan2(y,x)
    r=np.sqrt(x**2+y**2)+1e-6

    m1=np.sin(modeA*theta + 2*z + phase)
    m2=0.6*np.sin(modeB*theta -1.2*z -phase)

    s=spiral*np.sin(3*np.log(r)+phase)

    return (m1+m2+s)*np.exp(-(r-0.6)**2)

def compute(modeA,modeB,spiral,center,phase,z):

    return (
        torus_env(X,Y,z+0.9)
        + center*torus_env(X,Y,z)
        + torus_env(X,Y,z-0.9)
        + braid(X,Y,z,phase,modeA,modeB,spiral)
    )

field=compute(4,6,0.8,0.7,0,0)

fig=go.Figure(
    data=[go.Contour(z=field,colorscale="Plasma")]
)

steps=[]

for modeA in [3,4,5]:

    f=compute(modeA,6,0.8,0.7,0,0)

    steps.append(dict(
        method="update",
        args=[{"z":[f]}],
        label=f"modeA {modeA}"
    ))

fig.update_layout(
    sliders=[dict(
        currentvalue={"prefix":"modeA: "},
        steps=steps
    )],
    paper_bgcolor="black",
    plot_bgcolor="black",
    title="Atlas Field Lab"
)

file="atlas_field_lab_sliders.html"

fig.write_html(file)

webbrowser.open(file)

print("Atlas field lab running")
