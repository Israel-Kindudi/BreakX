from .jump_detector import JumpDetector
from .signal_engine import SignalEngine

class MultiSymbolEngine:
    def __init__(self):
        self.engines = {}

    def get_engine(self, symbol):
        if symbol not in self.engines:
            self.engines[symbol] = {
                "detector": JumpDetector(),
                "signal_engine": SignalEngine()
            }
        return self.engines[symbol]

    def process_tick(self, tick):
        symbol = tick["symbol"]
        price = tick["close"]

        engine = self.get_engine(symbol)

        jump = engine["detector"].update(price)
        signal = engine["signal_engine"].generate(jump)

        return {
            "symbol": symbol,
            "price": price,
            "jump": jump,
            "signal": signal
        }