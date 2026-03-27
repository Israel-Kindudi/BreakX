import json
import time

class SignalProcessor:
    def __init__(self, output_file="data/signals.jsonl"):
        self.output_file = output_file
        self.history = {}

    def process(self, data):
        symbol = data["symbol"]
        jump = data["jump"]
        signal = data["signal"]

        if symbol not in self.history:
            self.history[symbol] = {"jumps": 0, "ticks": 0}

        self.history[symbol]["ticks"] += 1

        if jump:
            self.history[symbol]["jumps"] += 1

        ticks = self.history[symbol]["ticks"]
        jumps = self.history[symbol]["jumps"]

        jump_prob = jumps / max(ticks, 1)
        strength = signal["strength"] if signal else 0

        confidence = min(strength * jump_prob, 1.0)
        ranking_score = confidence * 100

        record = {
            "timestamp": time.time(),
            "symbol": symbol,
            "price": data["price"],
            "jump_probability": jump_prob,
            "signal": signal,
            "confidence": confidence,
            "ranking_score": ranking_score
        }

        # 🔥 Append to JSONL (history)
        with open(self.output_file, "a") as f:
            f.write(json.dumps(record) + "\n")

        return record