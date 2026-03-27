import threading
import asyncio
from engine.multi_symbol_engine import MultiSymbolEngine
from stream.jsonl_streamer import stream_jsonl
from ui.live_chart import TradingDashboard, signal_queue 
import tkinter as tk
from engine.signal_processor import SignalProcessor
from engine.signal_processor import SignalProcessor
from engine.ranking_engine import RankingEngine

processor = SignalProcessor()
ranking_engine = RankingEngine()
processor = SignalProcessor()
# Path to your live JSONL stream
FILE_PATH = "data/live_data.jsonl"

engine = MultiSymbolEngine()

# Background thread: stream → engine → signal queue
def stream_worker(file_path, engine):
    for tick in stream_jsonl(file_path):
        if "BreakX" not in tick["symbol"]:
            continue

        result = engine.process_tick(tick)

        signal_queue.put(result)

        record = processor.process(result)

        # 🔥 Update ranking
        ranking_engine.update(record)

t = threading.Thread(target=stream_worker, args=(FILE_PATH, engine), daemon=True)
t.start()

# Start UI in main thread
root = tk.Tk()
app = TradingDashboard(root)
root.mainloop()