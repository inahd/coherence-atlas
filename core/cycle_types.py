from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class CycleStepResult:
    name: str
    ok: bool
    message: str = ""


@dataclass
class DayOfBrahmaConfig:
    source_dirs: List[str] = field(default_factory=lambda: [
        "docs",
        "architecture",
        "datasets",
        "transcripts",
        "wiki",
        "research",
    ])
    seed_dir: str = "seeds"
    graph_path: str = "memory/graphs/canonical_graph.json"
    visual_graph_path: str = "memory/cosmology_graph.json"
    mandala_path: str = "memory/visualizations/atlas_mandala.html"


@dataclass
class CycleState:
    config: DayOfBrahmaConfig
    counts: Dict[str, int] = field(default_factory=dict)
    results: List[CycleStepResult] = field(default_factory=list)

    def add_result(self, name: str, ok: bool, message: str = "") -> None:
        self.results.append(CycleStepResult(name=name, ok=ok, message=message))
