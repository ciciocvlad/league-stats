import json
from pathlib import Path


class Repository:
    def __init__(self, puuid):
        home = Path.home()
        Path(home / 'lol/stats').mkdir(parents=True, exist_ok=True)
        self.file = home / f'lol/stats/{puuid}.json'

    def read(self):
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return {}
        except json.decoder.JSONDecodeError:
            return {}

    def write(self, data):
        with open(self.file, 'w') as f:
            json.dump(data, f)

    def get_game_by_champion_and_id(self, champion, game_id):
        data = self.read()
        return next((game for game in data.get(champion, []) if game['id'] == game_id), None)

