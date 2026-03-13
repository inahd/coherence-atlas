from atlas.core.legend import build_legend
from atlas.core.prompts import research_prompts, expansion_prompts

def render_output(context="mandala"):

    legend=build_legend(context)

    print("")
    print("ATLAS LEGEND")
    print("------------")

    for l in legend:
        print("•",l)

    print("")
    print("RESEARCH PROMPTS")
    print("----------------")

    for p in research_prompts():
        print("•",p)

    print("")
    print("EXPANSION PROMPTS")
    print("-----------------")

    for p in expansion_prompts():
        print("•",p)

    print("")
