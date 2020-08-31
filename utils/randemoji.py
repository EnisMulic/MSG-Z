import json
import random


def Get():
    with open(".\\emoji.json", "r", encoding="utf-8") as jsonDataFile:
        emojis = json.load(jsonDataFile)

    emoji = random.sample(emojis.items(), 1)
    for key, value in emoji:
        return f"<:{key}:{value}>" 