from atlas.core.seeds import ingest
from atlas.core.cards import build

def run():

    print("Running Atlas cycle...")

    ingest()

    build()

    print("Cycle complete")
