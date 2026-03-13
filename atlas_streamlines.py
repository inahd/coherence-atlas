import numpy as np
import plotly.graph_objects as go
import webbrowser


def generate_lines(strands=6, twist=2, radius=1.0):

    t = np.linspace(0,20,800)
    traces=[]

    for i in range(strands):

        phase = i * (2*np.pi/strands)

        r = radius + 0.2*np.sin(twist*t + phase)

        x = r*np.cos(t)
        y = r*np.sin(t)
        z = 0.5*np.sin(twist*t + phase)

        traces.append(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=dict(width=4)
            )
        )

    return traces


six  = generate_lines(6)
nine = generate_lines(9)
twelve = generate_lines(12)

data = six + nine + twelve

# visibility masks
vis6  = [True]*len(six) + [False]*len(nine) + [False]*len(twelve)
vis9  = [False]*len(six) + [True]*len(nine) + [False]*len(twelve)
vis12 = [False]*len(six) + [False]*len(nine) + [True]*len(twelve)


fig = go.Figure(data=data)

# initial visibility
for i,v in enumerate(vis6):
    fig.data[i].visible = v


fig.update_layout(

    title="Toroid Braid Explorer",

    paper_bgcolor="black",

    scene=dict(
        bgcolor="black",
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False
    ),

    updatemenus=[

        dict(
            type="buttons",

            buttons=[

                dict(
                    label="6 strands",
                    method="update",
                    args=[{"visible":vis6}]
                ),

                dict(
                    label="9 strands",
                    method="update",
                    args=[{"visible":vis9}]
                ),

                dict(
                    label="12 strands",
                    method="update",
                    args=[{"visible":vis12}]
                )

            ]

        )

    ]

)

file="atlas_braid_explorer.html"

fig.write_html(file)

webbrowser.open(file)
