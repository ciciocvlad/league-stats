class Games:
    @staticmethod
    def __get_played_with_teammates(game, team):
        for teammate in team:
            if teammate.puuid not in game['metadata']['participants']:
                return False
        return True

    @staticmethod
    def __get_played_with_champions_in_game(game, champions):
        for champion in champions:
            if champion not in map(lambda x: x['championName'], game['info']['participants']):
                return False
        return True

    @staticmethod
    def __get_played_with_champions_on_side(game, champions, side):
        side = game['info']['participants'][:5] if side == 'blue' else game['info']['participants'][5:]
        for champion in champions:
            if champion not in map(lambda x: x['championName'], side):
                return False
        return True

    @staticmethod
    def __get_side(summoner, game, side):
        if summoner.puuid in game['metadata']['participants'][:5] and side == 'team' or summoner.puuid in game['metadata']['participants'][5:] and side == 'enemy':
            return game['info']['participants'][:5]
        else:
            return game['info']['participants'][5:]

    @staticmethod
    def __get_played_with_champions(game, champions, summoner, side):
        team = Games.__get_side(summoner, game, side)
        for champion in champions:
            if champion not in map(lambda x: x['championName'], team):
                return False
        return True

    @staticmethod
    def __filter_games(games, fun, *args):
        return list(filter(lambda x: fun(x, *args), games))

    @staticmethod
    def __find_summoner(game, summoner):
        return game['info']['participants'][game['metadata']['participants'].index(summoner.puuid)]

    @staticmethod
    def get_played_with_teammates(games, team):
        return Games.__filter_games(games, Games.__get_played_with_teammates, team)

    @staticmethod
    def get_played_with_champions_in_game(games, champions):
        return Games.__filter_games(games, Games.__get_played_with_champions_in_game, champions)

    @staticmethod
    def get_played_with_champions_on_side(games, champions, side):
        return Games.__filter_games(games, Games.__get_played_with_champions_on_side, champions, side)

    @staticmethod
    def get_played_with_champions(games, champions, summoner, side):
        return Games.__filter_games(games, Games.__get_played_with_champions, champions, summoner, side)

    @staticmethod
    def get_champions(games):
        return list(map(lambda x: map(lambda y: y['championName'], x['info']['participants']), games))

    @staticmethod
    def get_solo_queue(games):
        return list(filter(lambda x: x['info']['queueId'] == 420, games))

    @staticmethod
    def get_summoner_champion_stats(games, summoner):
        data = summoner.repo.read()
        for game in games:
            game_id = game['metadata']['matchId']
            game = Games.__find_summoner(game, summoner)
            game['id'] = game_id
            champion = game['championName']
            if champion not in data:
                data[champion] = [game]
            else:
                if game_id not in map(lambda x: x['id'], data[champion]):
                    data[champion].append(game)
        repo.write(data)
        return data

    @staticmethod
    def get_games_compared_to_time(games, func, seconds):
        return list(filter(lambda game: func(game['info']['gameDuration'], seconds), games))

