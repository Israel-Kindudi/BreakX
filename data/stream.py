import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time
import json
import os

# --- CONFIG ---
SYMBOLS = ["BreakX 600", "BreakX 1200", "BreakX 1800"]
TIMEFRAME = mt5.TIMEFRAME_M1

OUTPUT_FILE = "data/live_data.json"

os.makedirs("data", exist_ok=True)

# --- CONNECT ---
if not mt5.initialize():
    print("MT5 init failed")
    quit()

def compute_volatility(symbol, n=50):
    rates = mt5.copy_rates_from_pos(symbol, TIMEFRAME, 0, n)
    if rates is None:
        return 0
    
    df = pd.DataFrame(rates)
    returns = df['close'].pct_change().dropna()
    
    return returns.std()

try:
    print("🔴 Streaming engine started...\n")

    while True:
        snapshot = {}

        for sym in SYMBOLS:
            mt5.symbol_select(sym, True)

            rates = mt5.copy_rates_from_pos(sym, TIMEFRAME, 0, 1)

            if rates is None or len(rates) == 0:
                continue

            bar = rates[0]

            volatility = compute_volatility(sym)

            snapshot[sym] = {
                "time": datetime.fromtimestamp(bar['time']).isoformat(),
                "close": bar['close'],
                "volatility": float(volatility)
            }

            print(f"[{sym}] {bar['close']} | vol: {volatility:.6f}")

        # --- WRITE TO FILE ---
        OUTPUT_FILE = "data/live_data.jsonl"

        with open(OUTPUT_FILE, "a") as f:
            for sym, values in snapshot.items():
                record = {
                    "symbol": sym,
                    **values
                }
                f.write(json.dumps(record) + "\n")

                time.sleep(0.45)
        
except KeyboardInterrupt:
    print("Stopped.")
finally:
    mt5.shutdown()