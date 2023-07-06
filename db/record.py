from time import time, ctime


class Record:
    HEADERS = ["date", "score", "kills", "coins"]

    def __init__(self, score: int, kills: int, coins: int, date: str = None) -> None:
        self.date = date if date else ctime(time())
        self.score = score
        self.kills = kills
        self.coins = coins

    def __str__(self):
        return f"Date : {self.date}, Score : {self.score}, Kills : {self.kills}, Coins : {self.coins}"
