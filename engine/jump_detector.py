import numpy as np

class JumpDetector:
    def __init__(self, window=50, z_threshold=3.0):
        self.window = window
        self.z_threshold = z_threshold
        self.prices = []

    def update(self, price):
        self.prices.append(price)

        if len(self.prices) < self.window:
            return None

        returns = np.diff(self.prices[-self.window:])
        mean = np.mean(returns)
        std = np.std(returns)

        if std == 0:
            return None

        latest_return = returns[-1]
        z_score = (latest_return - mean) / std

        if abs(z_score) > self.z_threshold:
            return {
                "type": "jump",
                "direction": "up" if z_score > 0 else "down",
                "z_score": z_score,
                "return": latest_return
            }

        return None