import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR="/opt/atlas/research"
DEBOUNCE_SECONDS=2.5
_last = 0.0

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        global _last
        if event.is_directory:
            return
        now = time.time()
        if now - _last < DEBOUNCE_SECONDS:
            return
        _last = now
        print(f"\nChange detected: {event.src_path}")
        subprocess.run("atlas refresh", shell=True)

def run():
    print("Atlas watch running (auto refresh on change)")
    print("Watching:", WATCH_DIR)
    obs = Observer()
    obs.schedule(Handler(), WATCH_DIR, recursive=True)
    obs.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()

if __name__ == "__main__":
    run()
