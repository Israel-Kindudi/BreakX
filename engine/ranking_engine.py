import json

class RankingEngine:
    def __init__(self, output_file="data/rankings.json"):
        self.output_file = output_file
        self.latest = {}

    def update(self, record):
        symbol = record["symbol"]

        self.latest[symbol] = {
            "symbol": symbol,
            "confidence": record["confidence"],
            "jump_probability": record["jump_probability"],
            "ranking_score": record["ranking_score"],
            "signal": record["signal"]
        }

        self.write_rankings()

    def write_rankings(self):
        ranked = sorted(
            self.latest.values(),
            key=lambda x: x["ranking_score"],
            reverse=True
        )

        with open(self.output_file, "w") as f:
            json.dump(ranked, f, indent=2)