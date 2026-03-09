import json
import pathlib

OUT="atlas/cards/cards.json"

def build():

    cards=[
        {"name":"Sun","type":"graha"},
        {"name":"Moon","type":"graha"},
        {"name":"Mars","type":"graha"},
        {"name":"Venus","type":"graha"}
    ]

    pathlib.Path(OUT).write_text(json.dumps(cards,indent=2))

    print("Cards generated:",len(cards))
