# file-watcher

Poll a directory and log created, modified and deleted files to a log file, with md5 + size fingerprinting.

```bash
python3 watch.py /var/log ~/watch.log
```

Works fine as a lightweight systemd service for servers where inotify-based watchers are overkill.
