from typing import Union
from pydantic import BaseModel
import fastapi
import logging


logger = logging.getLogger(__name__)

app = fastapi.FastAPI()

db = {}


class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    logger.info("Got root")
    return {"status": "alive"}


@app.get("/items")
def read_items():
    return {'items': [db[id] for id in db]}


@app.get("/items/{item_id}", status_code = 200)
def read_item(item_id: int):
    if item_id in db:
        return db[item_id]
    else:
        raise fastapi.HTTPException(status_code = 404)


@app.post("/items", status_code=201)
def add_item(item: Item):
    logger.info(f"Adding:\n{item}")
    db[item.id] = item
    