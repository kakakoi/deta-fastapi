from deta import Deta
from pandas import json_normalize
import datetime
import os

project_key = os.environ.get('DETA_PROJECT_KEY')
deta = Deta(project_key)

async def get_item(key: str):
    db = deta.Base("products")
    # resp = db.get(key)
    # resp = db.query(query=[{"key": key}])
    resp = await db.fetch({'key': key}, limit=1)

    # resp = await db.fetch(query={"key": key})
    return resp

def get_rank(rank_num: int):
    db = deta.Base("products")
    resp = db.fetch(query={"Item.affiliateRate?gt": rank_num}, limit=1, last=None)
    return resp

def put_rakuten_rank(json_result):
    df = json_normalize(json_result['Items']).loc[:, [
        'Item.affiliateRate', 'Item.catchcopy', 'Item.shopName', 'Item.itemUrl', 'Item.mediumImageUrls']]
    df['Item.affiliateRate'] = df['Item.affiliateRate'].astype(float)

    items = df.to_dict(orient='records')

    db = deta.Base("products")
    for item in items:
        res = db.put(item)
        print(f'put_rakuten_rank-{res}')


def put_request_log(name: str):
    dt_now = datetime.datetime.now().isoformat()
    db = deta.Base("request_log")
    res = db.put({'name':name, 'createdAt':dt_now})
    print(f'put_request_log-{res}')