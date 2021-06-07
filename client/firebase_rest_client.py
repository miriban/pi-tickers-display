import requests
import urllib.parse


class Firebase:
    BASE_URI = 'https://pi-2021-default-rtdb.europe-west1.firebasedatabase.app/'

    @staticmethod
    def get_user_data(code):
        url = urllib.parse.urljoin(Firebase.BASE_URI + '/users/', code + '.json')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_user_etfs(code):
        url = urllib.parse.urljoin(Firebase.BASE_URI + '/users/', code + '/etfs.json')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

