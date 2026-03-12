import os
import sys
import subprocess

TASK_DIR = "/opt/atlas/atlas_codex/tasks"
OUTPUT_DIR = "/opt/atlas/atlas_codex/outputs"

def run(task):
    task_path = os.path.join(TASK_DIR, task)

    if not os.path.exists(task_path):
        print("Task not found:", task)
        return

    print("Running Codex task:", task)

    # placeholder: call OpenAI / Codex here
    subprocess.run(f"cat {task_path}", shell=True)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: run_codex_task.py <taskfile>")
        sys.exit()

    run(sys.argv[1])
