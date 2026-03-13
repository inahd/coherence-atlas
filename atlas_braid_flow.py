import numpy as np
import plotly.graph_objects as go
import webbrowser

t = np.linspace(0,20,600)

lines = []

for phase in np.linspace(0,2*np.pi,6):

    r = 1 + 0.25*np.sin(3*t + phase)

    x = r*np.cos(t)
    y = r*np.sin(t)
    z = 0.5*np.sin(2*t + phase)

    lines.append(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="lines",
            line=dict(width=4)
        )
    )

fig = go.Figure(data=lines)

fig.update_layout(
    title="Toroid Braid Streamlines",
    paper_bgcolor="black",
    scene=dict(
        bgcolor="black",
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False
    )
)

file="atlas_streamlines.html"

fig.write_html(file)

webbrowser.open(file)
