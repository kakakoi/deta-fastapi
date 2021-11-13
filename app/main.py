from fastapi import BackgroundTasks, FastAPI
import requests
from starlette.responses import Response
# from deta import Deta  # Import Deta
from deta import Deta
from pandas import json_normalize
import os
import numpy as np


app = FastAPI()


@app.get("/")
def read_root():
    return request_api()


@app.post("/put/rank/{api_name}")
def put_rank(api_name: str, background_tasks: BackgroundTasks):
    message = "none"
    if(api_name == 'rakuten'):
        background_tasks.add_task(put_rakuten_rank)
        message = "put_rank in the background"
    return {"message": message}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


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


def putdb(json_result):
    df = json_normalize(json_result['Items']).loc[:, [
        'Item.affiliateRate', 'Item.catchcopy', 'Item.shopName', 'Item.itemUrl', 'Item.mediumImageUrls']]
    items = df.to_dict(orient='records')
    putdb(items)

    deta = Deta()
    db = deta.Base("products")
    for item in items:
        db.put(item)


def put_rakuten_rank():
    items = request_api()
