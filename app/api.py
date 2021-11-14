import requests
import os

def request_api():
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
    id = os.environ.get('RAKUTEN_API_ID')
    print(id)
    params = {
        'format': 'json',
        'applicationId': id
    }

    response = requests.get(url, params)
    return response.json()
