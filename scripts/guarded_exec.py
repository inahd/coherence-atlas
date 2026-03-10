import subprocess
import sys

def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Command failed:")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: guarded_exec <command>")
        sys.exit(1)

    run(" ".join(sys.argv[1:]))
