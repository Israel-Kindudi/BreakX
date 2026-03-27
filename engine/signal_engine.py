class SignalEngine:
    def __init__(self, short_bias=0.516):
        self.short_bias = short_bias

    def generate(self, jump_event):
        if jump_event is None:
            return None

        direction = jump_event["direction"]

        # Optional bias adjustment
        if direction == "up":
            action = "buy"
        else:
            action = "sell"

        return {
            "action": action,
            "strength": abs(jump_event["z_score"]),
            "type": "jump_reaction"
        }