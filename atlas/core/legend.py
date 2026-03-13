def build_legend(context="mandala"):

    legends={

        "mandala":[
            "Circle layout = relational field",
            "Distance = connection gravity",
            "Node cluster = conceptual resonance"
        ],

        "graph":[
            "Node = concept",
            "Edge = relation",
            "Cluster = conceptual family"
        ],

        "card":[
            "Card = structured knowledge object",
            "Symbol = archetypal reference",
            "Fields = research anchors"
        ]

    }

    return legends.get(context,[])
