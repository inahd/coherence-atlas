from atlas_lab.engine.toroid import generate_toroid
import plotly.graph_objects as go
import webbrowser
import numpy as np

from atlas_lab.engine.braid import generate_braid


def build_scene(strands=6, twist=2, radius=1.0):

    curves = generate_braid(strands, twist, radius)

    traces = []

    for x, y, z in curves:

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


def launch():

    strands_list = [6, 9, 12]

    data = []
    visibility = []

    for strands in strands_list:

        curves = build_scene(strands)

        data.extend(curves)

        visibility.extend([False]*len(curves))

    # make first scene visible
    for i in range(len(build_scene(6))):
        visibility[i] = True

    fig = go.Figure(data=data)

    for i,v in enumerate(visibility):
        fig.data[i].visible = v

    # button masks
    masks = []
    start = 0

    for strands in strands_list:

        count = len(build_scene(strands))

        mask = [False]*len(data)

        for i in range(start,start+count):
            mask[i] = True

        masks.append(mask)

        start += count

    fig.update_layout(

        title="Atlas Toroid Braid Lab",

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
                        label="6 Strands",
                        method="update",
                        args=[{"visible": masks[0]}]
                    ),

                    dict(
                        label="9 Strands",
                        method="update",
                        args=[{"visible": masks[1]}]
                    ),

                    dict(
                        label="12 Strands",
                        method="update",
                        args=[{"visible": masks[2]}]
                    ),

                ]

            )

        ]

    )

    file="atlas_lab_viewer.html"

    fig.write_html(file)

    webbrowser.open(file)
