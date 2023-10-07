from fastapi import Form
from pydantic import BaseModel
from typing import List, Optional


class Todo(BaseModel):
    id: Optional[int]
    item: str

    @classmethod
    def as_form(
        cls,
        item: str = Form(...)
    ):
        return cls(item=item)


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
