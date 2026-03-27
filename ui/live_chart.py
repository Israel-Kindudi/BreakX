import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import queue
from collections import deque

signal_queue = queue.Queue()


class TradingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("BreakX Candlestick Dashboard")
        self.root.geometry("1200x800")

        # Config
        self.max_candles = 100
        self.candle_size = 5  # ticks per candle

        # Data
        self.candles = {}
        self.current_candle = {}
        self.signals = {}
        self.jump_counts = {}
        self.last_signal = {}

        self.symbols = ["BreakX 600", "BreakX 800", "BreakX 1200"]

        # Layout
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(root, height=150)
        self.bottom_frame.pack(fill=tk.X)

        self.figures = {}
        self.axes = {}
        self.canvases = {}

        for i, symbol in enumerate(self.symbols):
            frame = tk.Frame(self.top_frame)
            frame.grid(row=0, column=i, sticky="nsew")

            fig, ax = plt.subplots(figsize=(4, 3))
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.figures[symbol] = fig
            self.axes[symbol] = ax
            self.canvases[symbol] = canvas

            self.candles[symbol] = deque(maxlen=self.max_candles)
            self.current_candle[symbol] = None
            self.signals[symbol] = []
            self.jump_counts[symbol] = 0
            self.last_signal[symbol] = "None"

        # Stats panel
        self.stats_labels = {}
        for symbol in self.symbols:
            label = tk.Label(self.bottom_frame, text="", font=("Arial", 10), anchor="w")
            label.pack(fill=tk.X)
            self.stats_labels[symbol] = label

        self.update_dashboard()

    def update_dashboard(self):
        while not signal_queue.empty():
            data = signal_queue.get()
            if data is None:
                continue

            symbol = data["symbol"]
            price = data["price"]
            signal = data["signal"]
            jump = data["jump"]

            if symbol not in self.candles:
                continue

            # --- BUILD CANDLE ---
            candle = self.current_candle[symbol]

            if candle is None:
                self.current_candle[symbol] = {
                    "open": price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "ticks": 1
                }
            else:
                candle["high"] = max(candle["high"], price)
                candle["low"] = min(candle["low"], price)
                candle["close"] = price
                candle["ticks"] += 1

                if candle["ticks"] >= self.candle_size:
                    self.candles[symbol].append(candle)
                    self.current_candle[symbol] = None

            # --- TRACK EVENTS ---
            if jump:
                self.jump_counts[symbol] += 1

            if signal:
                idx = len(self.candles[symbol])
                self.signals[symbol].append((idx, price, signal["action"]))
                self.last_signal[symbol] = signal["action"]

        # --- DRAW ---
        for symbol in self.symbols:
            ax = self.axes[symbol]
            ax.clear()

            candles = list(self.candles[symbol])

            for i, c in enumerate(candles):
                color = "green" if c["close"] >= c["open"] else "red"

                # wick
                ax.plot([i, i], [c["low"], c["high"]], color=color)

                # body
                ax.plot([i, i], [c["open"], c["close"]], linewidth=6, color=color)

            # Signals
            for idx, price, action in self.signals[symbol]:
                color = "lime" if action == "buy" else "red"
                marker = "^" if action == "buy" else "v"
                ax.scatter(idx, price, color=color, marker=marker, s=80)

            ax.set_title(symbol)
            ax.grid(True)

            self.canvases[symbol].draw()

        # --- STATS ---
        for symbol in self.symbols:
            total = max(len(self.candles[symbol]), 1)
            intensity = self.jump_counts[symbol] / total

            text = (
                f"{symbol} | Candles: {total} | "
                f"Jumps: {self.jump_counts[symbol]} | "
                f"Intensity: {intensity:.4f} | "
                f"Last: {self.last_signal[symbol]}"
            )

            self.stats_labels[symbol].config(text=text)

        self.root.after(100, self.update_dashboard)