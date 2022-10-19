from typing import Union
from pydantic import BaseModel
import fastapi
import logging
import os
from deta import Base

logger = logging.getLogger(__name__)

app = fastapi.FastAPI()

# Database
db = Base(f'core-db-{os.getenv("DETA_PATH", "local")}')

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
    return {'items': db.fetch().items}


@app.get("/items/{item_id}", status_code = 200)
def read_item(item_id: int):
    items = db.fetch({"id": item_id}).items
    print(items)
    if items: # If list is not empty return the first item only
         return items[0]
    else:
        raise fastapi.HTTPException(status_code = 404)

@app.delete("/items/{item_id}", status_code = 202)
def delete_item(item_id: int):
    for item in db.fetch({"id": item_id}).items:
        db.delete(item["key"])


@app.post("/items", status_code=201)
def add_item(itemObject: Item):
    # Check existence
    id = itemObject.id
    if db.fetch({"id": id}).items:
        raise fastapi.HTTPException(
            status_code = 409, detail = f"Item with id {id} already exists")

    item = itemObject.dict()
    print(f"Adding:\n{item}")
    logger.info(f"Adding:\n{item}")
    db.insert(item)
