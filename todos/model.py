from pydantic import BaseModel
from typing import List

class Todo(BaseModel):
  id: int
  item: str

class TodoItem(BaseModel):
  item: str
  model_config = {
    "json_schema_extra": {
      "examples": [
        {
          "item": "Todo item",
        }
      ]
    }
  }

class TodoItems(BaseModel):
  todos: List[TodoItem]
  model_config = {
    "json_schema_extra": {
      "examples": [
        {
          "todos": [
            {
              "id": 1,
              "item": "Todo item 1"
            },
            {
              "id": 2,
              "item": "Todo item 2"
            }
          ]
        }
      ]
    }
  }
