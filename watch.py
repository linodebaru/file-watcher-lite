#!/usr/bin/env python3
"""Watch a directory and log created / modified / deleted files via polling."""

import hashlib
import os
import sys
import time

WATCH_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
LOG_PATH = sys.argv[2] if len(sys.argv) > 2 else "watch.log"
POLL_SECONDS = 5


def file_fingerprint(path: str) -> tuple[int, str]:
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return os.path.getsize(path), hasher.hexdigest()[:10]


def snapshot(root: str) -> dict:
    state = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            full = os.path.join(dirpath, name)
            try:
                state[full] = file_fingerprint(full)
            except OSError:
                pass
    return state


def main() -> None:
    print(f"watching {WATCH_DIR} -> {LOG_PATH} (ctrl+c to stop)")
    previous = snapshot(WATCH_DIR)
    while True:
        time.sleep(POLL_SECONDS)
        current = snapshot(WATCH_DIR)
        with open(LOG_PATH, "a") as f:
            stamp = time.strftime("%F %T")
            for path in current:
                if path not in previous:
                    f.write(f"{stamp} NEW {path}\n")
                elif current[path] != previous[path]:
                    f.write(f"{stamp} CHG {path}\n")
            for path in previous:
                if path not in current:
                    f.write(f"{stamp} DEL {path}\n")
        previous = current


if __name__ == "__main__":
    main()
