import sys
import subprocess

def run():

    if len(sys.argv) < 2:
        print("Usage: atlas codex <task>")
        return

    task = sys.argv[1]

    subprocess.run(
        f"python /opt/atlas/atlas_codex/scripts/run_codex_task.py {task}",
        shell=True
    )

if __name__ == "__main__":
    run()
