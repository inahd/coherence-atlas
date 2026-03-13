import numpy as np
import plotly.graph_objects as go
import webbrowser

N = 160
extent = 2.4

x = np.linspace(-extent, extent, N)
y = np.linspace(-extent, extent, N)
X, Y = np.meshgrid(x, y)

def torus_env(x, y, z, R=1.25, a=0.45):
    r = np.sqrt(x**2 + y**2)
    return np.exp(-((r - R)**2 + z**2) / a)

def braid(x, y, z, phase):
    theta = np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2)
    return np.sin(4*theta + 2*z + phase) * np.exp(-(r - 0.6)**2)

def compute_field(z, phase):
    return (
        torus_env(X, Y, z + 0.9)
        + torus_env(X, Y, z - 0.9)
        + braid(X, Y, z, phase)
    )

frames = []
total_frames = 120

for i in range(total_frames):

    z = -1.2 + 2.4 * (i / (total_frames - 1))
    phase = 2 * np.pi * (i / total_frames)

    field = compute_field(z, phase)

    frames.append(go.Frame(
        data=[go.Contour(z=field)],
        name=str(i)
    ))

fig = go.Figure(data=[go.Contour(z=compute_field(0,0))], frames=frames)

fig.update_layout(
    title="Toroid Field Explorer",
    paper_bgcolor="black",
    plot_bgcolor="black",
    updatemenus=[{
        "type": "buttons",
        "buttons": [{"label": "Travel Field", "method": "animate", "args": [None]}]
    }]
)

file = "/opt/atlas/field_explorer.html"
fig.write_html(file)

webbrowser.open(file)

print("Explorer launched.")
