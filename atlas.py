import sys
import subprocess

COMMANDS = {
    "prompts_commit": "bash /opt/atlas/scripts/prompts_commit.sh",
    "prompts_write": "bash /opt/atlas/scripts/prompts_write.sh",
    "prompts": "bash /opt/atlas/scripts/prompts_cli.sh",
    "layered_graph": "bash /opt/atlas/scripts/layered_graph_open.sh",
    "layered_build": "python3 /opt/atlas/scripts/layered_relations_build.py",
    "promote_auto_apply": "python3 /opt/atlas/scripts/auto_populate.py apply",
    "promote_auto_export": "python3 /opt/atlas/scripts/auto_populate.py export",
    "autoapply": "python3 /opt/atlas/scripts/auto_populate.py autoapply",
    "guard": "python3 /opt/atlas/scripts/guard_canon.py",
    "review": "bash /opt/atlas/scripts/atlas_review.sh",
    "run": "bash /opt/atlas/scripts/atlas_run.sh",
    "wget_guarded": "bash /opt/atlas/scripts/wget_guarded.sh",
    "ocr_low": "bash /opt/atlas/scripts/ocr_lowtext.sh",
    "lowtext": "python3 /opt/atlas/scripts/find_lowtext_pdfs.py",
    "dashboard": "bash /opt/atlas/scripts/open_dashboard.sh",
    "safeupdate": "bash /opt/atlas/scripts/safeupdate.sh",
    "test": "bash /opt/atlas/scripts/run_tests.sh",
    "adopt": "python3 /opt/atlas/scripts/adopt_staged.py",
    "stage": "python3 /opt/atlas/scripts/stage_candidates.py",
    "aggregate": "python3 /opt/atlas/scripts/aggregate_report.py",
    "corpus_harvest": "python3 /opt/atlas/scripts/corpus_harvest_passages.py",
    "corpus_pdftext": "python3 /opt/atlas/scripts/corpus_extract_pdftext.py",
    "corpus_scan": "python3 /opt/atlas/scripts/corpus_scan.py",
    "corpus_init": "python3 /opt/atlas/scripts/corpus_db.py",
    "cycleauto": "bash /opt/atlas/scripts/cycle_scheduled.sh",
    "pick": "python3 /opt/atlas/scripts/pick_manifest.py",
    "gaps": "python3 /opt/atlas/scripts/gap_score.py",
    "cycle": "bash /opt/atlas/scripts/cycle.sh",
    "snapshot": "bash /opt/atlas/scripts/snapshot.sh",
    "evidencefill": "python /opt/atlas/scripts/evidencefill.py",
    "harvest": "python /opt/atlas/scripts/harvest_text_passages.py",
    "pdftext": "python /opt/atlas/scripts/pdftext_all.py",
    "promote": "python /opt/atlas/scripts/promote_incoming.py",
    "wgetcycle": "bash /opt/atlas/scripts/wget_cycle.sh",
    "rollback": "bash /opt/atlas/scripts/rollback.sh",
    "links": "python /opt/atlas/scripts/links_cycle.py",
    "ingest": "python /opt/atlas/scripts/ingest_all.py",
    "harvestpdf": "python /opt/atlas/scripts/harvest_pdf.py",
    "propose": "python /opt/atlas/scripts/propose_evidence.py",
    "api": "python /opt/atlas/scripts/atlas_api.py",
    "seed": "python /opt/atlas/scripts/seed_relations.py",
    "seedgraph": "python /opt/atlas/scripts/build_seed_graph.py",
    "factcheck": "python /opt/atlas/scripts/factcheck_relations.py",
    "autolink": "python /opt/atlas/scripts/autolink.py",
    # Low-tedium growth
    "refresh":        "python /opt/atlas/scripts/refresh.py",
    "watch":          "python /opt/atlas/scripts/auto_watch.py",
    "nightly":        "python /opt/atlas/scripts/nightly.py",

    # Local research pipeline pieces
    "research":       "python /opt/atlas/scripts/research_ingest.py",
    "concepts":       "python /opt/atlas/scripts/concept_extract.py",
    "graph":          "python /opt/atlas/scripts/graph_viewer.py",

    # Cloud offload (OpenAI)
    "research_cloud": "python /opt/atlas/scripts/research_cloud.py",

    # Canonical layer (if present)
    "cosmology":      "python /opt/atlas/scripts/build_cosmology_graph.py",

    # Utilities
    "chat":           "python /opt/atlas/scripts/ai_router.py",
    "models":         "ollama list",
}

def main():
    if len(sys.argv) < 2:
        print("\nAtlas CLI\n\nCommands:\n")
        for k in sorted(COMMANDS.keys()):
            print(" ", k)
        print("\nExamples:\n  atlas watch\n  atlas refresh\n  atlas nightly\n  atlas research_cloud\n")
        return

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print("Unknown command:", cmd)
        print("Run `atlas` to list commands.")
        return

    base = COMMANDS[cmd]
    extra = " ".join(sys.argv[2:])
    full = base + (f" {extra}" if extra else "")
    subprocess.run(full, shell=True)

if __name__ == "__main__":
    main()
