import os
import operator
from repository import Repository
from player import Player
from utils.exceptions import ServerError
from utils.iterable import mymap
from utils.summoner_spells import summoner_spells
from utils.request import Request


class Summoner:
    def __init__(self, summoner_name):
        [game_name, tag_line] = summoner_name.split('#')
        url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name.replace(' ', '%20')}/{tag_line}'
        response = Request.make_request(url)
        try:
            data = Request.get_data(response)
            self.puuid = data['puuid']
            self.game_name = data['gameName']
            self.tag_line = data['tagLine']
            self.repo = Repository(self.puuid)
        except ServerError:
            print('Could not receive summoner')

    def __get_games(self, count):
        url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count={count}'
        return Request.make_request(url)

    def __get_game(self, game):
        try:
            return Request.get_data(Request.make_request(f'https://europe.api.riotgames.com/lol/match/v5/matches/{game}'))
        except ServerError:
            return None

    def get_games(self, count=20):
        games = self.__get_games(count)
        return mymap(self.__get_game, Request.get_data(games))

    def get_champion_data(self, champion):
        data = self.repo.read()
        return data[champion]

    def get_played_with_champion(self, champion):
        data = self.repo.read()
        count = 0
        for game in data[champion]:
            count += game['duration']
        return [count // 86400, count % 86400 // 3600, count % 86400 % 3600 // 60]

    def get_winrate(self, champion):
        data = self.repo.read()
        win = lose = 0
        for game in data[champion]:
            if game['win']:
                win += 1
            else:
                lose += 1
        return [win, lose]

    def get_kda_with_champion(self, champion):
        data = self.repo.read()
        kda = [0, 0, 0]
        for game in data[champion]:
            player = Player(game)
            kda = [x + y for (x, y) in zip(kda, player.get_kda())]
        return kda

    def get_abilities_used(self, champion):
        data = self.repo.read()
        abilities = [0, 0, 0, 0]
        for game in data[champion]:
            player = Player(game)
            abilities = map(operator.add, abilities, player.get_abilities())
        return list(abilities)

    def get_summoner_spells_used(self, champion):
        data = self.repo.read()
        spells = {}
        for game in data[champion]:
            player = Player(game)
            game_spells = player.get_summoner_spells()
            spells = {**spells, **game_spells, **{k: spells[k] + game_spells[k] for k in spells.keys() & game_spells}}
        return {summoner_spells[key]: value for key, value in spells.items()}

    def get_multi_kill_on_champion(self, champion):
        data = self.repo.read()
        kills = [0, 0, 0, 0]
        for game in data[champion]:
            player = Player(game)
            kills = map(operator.add, kills, player.get_multi_kill())
        return list(kills)

    def get_roles_on_champion(self, champion):
        data = self.repo.read()
        roles = {'TOP': 0, 'JUNGLE': 0, 'MIDDLE': 0, 'BOTTOM': 0, 'UTILITY': 0}
        for game in data[champion]:
            roles['teamPosition'] += 1
        return roles

    def get_played_with(self):
        data = self.repo.read()
        counts = {}
        for game in sum(data.values(), []):
            for key in game['participants']:
                if key != self.puuid:
                    (count, games) = counts.get(key, (0, []))
                    counts[key] = (count + 1, games + [game])
        return {key: (count, games) for key, (count, games) in counts.items() if count > 1}

    def get_played_with_details(self, data):
        res = {}
        for key, (count, games) in data.items():
            summoner = self.get_by_puuid(key)
            res[summoner.game_name] = {'with': {True: [], False: []}, 'against': {True: [], False: []}}
            for game in games:
                if self.puuid in game['participants'][:5] and key in game['participants'][:5] or self.puuid in game['participants'][5:] and key in game['participants'][5:]:
                    res[summoner.game_name]['with'][game['win']].append(game)
                else:
                    res[summoner.game_name]['against'][game['win']].append(game)
        return res

    def update_stats(self):
        data = self.repo.read()
        games = self.get_games(50)
        for game in games:
            game_id = game['metadata']['matchId']
            duration = game['info']['gameDuration']
            queueId = game['info']['queueId']
            participants = game['metadata']['participants']
            game = game['info']['participants'][game['metadata']['participants'].index(self.puuid)]

            game['id'] = game_id
            game['duration'] = duration
            game['queueId'] = queueId
            game['participants'] = participants
            champion = game['championName']
            if champion not in data:
                data[champion] = [game]
            else:
                if self.repo.get_game_by_champion_and_id(champion, game_id) is None:
                    data[champion].append(game)
        self.repo.write(data)

    @staticmethod
    def get_by_puuid(puuid):
        url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
        response = Request.make_request(url)
        data = Request.get_data(response)
        return Summoner(f'{data['gameName']}#{data['tagLine']}')
        

