import json
import time

def stream_jsonl(file_path):
    """Generator: yields new JSON ticks from an append-only JSONL file"""
    with open(file_path, "r") as f:
        f.seek(0, 2)  # go to end

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.01)
                continue

            try:
                yield json.loads(line.strip())
            except:
                continue