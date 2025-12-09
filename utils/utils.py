class Utils:
    @staticmethod
    def get_winrate(games):
        wins = len(games[True])
        total = len(games[False]) + wins
        return '{:.2f}'.format(wins / total * 100)

    @staticmethod
    def no_games(games):
        return games[True] == [] and games[False] == []

    @staticmethod
    def games_count(games):
        return len(games[True]) + len(games[False])

