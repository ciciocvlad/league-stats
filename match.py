from utils.request import Request


class Match:
    start_time=1735689600

    @staticmethod
    def get_by_id(match_id):
        url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}'
        return Request.make_request(url)

