from fastapi import BackgroundTasks, FastAPI, Body, applications
# import db
from mongodb import db
import api
from bson.json_util import dumps, loads

app = FastAPI()


@app.get("/")
def read_root():
    return api.request_api()


@app.post("/put/rank/{api_name}")
def put_rank(api_name: str, background_tasks: BackgroundTasks):
    message = "none"
    if(api_name == 'rakuten'):
        background_tasks.add_task(put_rakuten_rank)
        message = "put_rank in the background"
    return {"message": message}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return db.get_item(item_id)

@app.get("/rank/{rank_num}")
def read_rank(rank_num: int):
    return db.get_rank(rank_num)

def put_rakuten_rank():
    name = 'rakuten_rank'
    db.put_request_log(name)
    result = api.request_api()
    db.put_rakuten_rank(result)


@app.post('/')
def create_post(body=Body(...)):
    """postの作成

    ----------
    Parameters:

    body: body
        任意のjson
    """
    post = body['payload']
    db.posts.insert(post)
    return {'post': "ok"}

@app.get('')
def read_post():
    """postの取得

    ----------
    Parameters:

    なし
    """
    db_post = db.posts.find_one()
    return {'item': dumps(db_post)}