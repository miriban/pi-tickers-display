import os
import json
import requests
import urllib.parse


class TwelveDataClient:
    BASE_URI = 'https://api.twelvedata.com'

    def __init__(self):
        try:
            with open(os.getcwd() + '/apis.tmp', 'r') as tmp_file:
                data = json.load(tmp_file)
            self.token = data['twelveDataApiKey']
        except:
            raise Exception("Please create an apis.tmp file and provide your 12data api key!")

    def get_time_series(self, etfs):
        if len(etfs) == 0:
            return {}
        try:
            path = 'time_series?symbol=%s&interval=1min&outputsize=1&apikey=%s' % (','.join(etfs), self.token)
            url = urllib.parse.urljoin(TwelveDataClient.BASE_URI, path)
            response = requests.get(url)
            result = response.json()
            if 'code' in result:
                raise Exception(result['message'])
        except Exception as e:
            print("Error => " + str(e))
            return {}
        if len(etfs) > 1:
            return result
        return {etfs[0]: result}

