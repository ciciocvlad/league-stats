class Player:
    def __init__(self, game):
        self.game = game

    def get_kda(self):
        return [self.game['kills'], self.game['deaths'], self.game['assists']]

    def get_abilities(self):
        return [self.game['spell1Casts'], self.game['spell2Casts'], self.game['spell3Casts'], self.game['spell4Casts']]

    def get_summoner_spells(self):
        return {
            self.game['summoner1Id']: self.game['summoner1Casts'],
            self.game['summoner2Id']: self.game['summoner2Casts']
        }

    def get_multi_kill(self):
        return [self.game['doubleKills'], self.game['tripleKills'], self.game['quadraKills'], self.game['pentaKills']]

