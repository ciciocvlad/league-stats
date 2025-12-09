import os
import requests
from dotenv import load_dotenv
from utils.exceptions import ServerError


class Request:
    @staticmethod
    def make_request(url):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        response = requests.get(url, headers={'X-Riot-Token': api_key})
        return {'status': response.status_code, 'data': response.json()}

    @staticmethod
    def get_data(response):
        if response['status'] == 200:
            return response['data']
        raise ServerError(response['status'])

