import json, os

DEFAULTS = {
    "bankroll":100, 
    "hands_played":0,
    "hands_won_total":0,
    "hands_won_conseq":0,
    "all_time_winnings":0,
    "all_time_loss":0,
    "bankruptcys":0
}

def load(path="save.json"):
    stats = dict(DEFAULTS)
    if os.path.exists(path):
        with open(path) as f:
            stats.update(json.load(f))
    return stats

def save(stats, path="save.json"):
    with open(path, "w") as f:
        json.dump(stats, f, indent=2)