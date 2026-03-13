import subprocess
import os

def run_step(name, cmd):
    print(f"\n==> {name}")
    subprocess.run(cmd, shell=True)

def main():
    print("\nAtlas nightly\n")
    run_step("refresh (local ingest+concepts+graph)", "atlas refresh")

    # Only run cloud step if key is present
    if os.getenv("OPENAI_API_KEY", "").strip():
        run_step("research_cloud (OpenAI synthesis)", "atlas research_cloud")
    else:
        print("\n==> research_cloud skipped (OPENAI_API_KEY not set)")

    print("\nNightly done.\n")

if __name__ == "__main__":
    main()
