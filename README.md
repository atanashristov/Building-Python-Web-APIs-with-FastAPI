# Building Python Web APIs with FastAPI

Code and notes from studying [Building Python Web APIs with FastAPI](https://github.com/PacktPublishing/Building-Python-Web-APIs-with-FastAPI)

## Chapter 1: Getting started

Create directory, create and activate a virtual environment, verify `pip` is installed:

```sh
pip install virtualenv
mkdir todos && cd todos
virtualenv env
env/Scripts/activate
python3 -m pip list
```

Deactivate the virtual environment:

```sh
deactivate
```

Install `fastapi` and create/freeze `requirements.txt`:

```sh
pip install fastapi
pip freeze > requirements.txt
```

To install packages from `requirements.txt` file we run:

```sh
pip install -r requirements.txt
```

Create `api.py` file:

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def welcome() -> dict:
  return { "message": "Hello World" }
```

And run the API:

```sh
uvicorn api:app --port 8000 --reload
```

In the preceding command, `uvicorn` takes the following arguments:

- file:instance: The file containing the instance of FastAPI and the name variable holding the FastAPI instance.
- --port PORT: The port the application will be served on.
- --reload: An optional argument included to restart the application on every file change.

Check the API:

```sh
curl http://127.0.0.1:8000/
{"message":"Hello World"}
```

Oops - remove `__pycache__`, add "__pycache__" to `.gitignore` and run:

```sh
git rm -r --cached __pycache__
git commit -a --amend --no-edit
git push --force
```

See:

- [Pip and virtualenv on Windows](https://programwithus.com/learn/python/pip-virtualenv-windows)

## Chapter 2: Routing in FastAPI

See `todo.py` for using `APIRouter`. See `api.py` for importing and including the router.

Run `curl` to POST data:

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/todo' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "item": "First Todo is to finish this book!"
}'
{"message":"Todo added successfully"}
```

Run `curl` to update data:

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/todo' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "item": "Example Schema!"
}'
{"message":"Todo added successfully"}
```

Run `curl` to get data:

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/todo' \
  -H 'accept: application/json'
{"message":"Hello World"}
```

Run `curl` to delete one todo item:

```sh
curl -X 'DELETE' \
  'http://127.0.0.1:8000/todo/1' \
  -H 'accept: application/json'
{"message":"Todo deleted successfully."}
```

Run `curl` to delete all todo items:

```sh
curl -X 'DELETE' \
  'http://127.0.0.1:8000/todo' \
  -H 'accept: application/json'
{"message":"Todos deleted successfully."}
```

See:

- [Fast API APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter)

### Validating request bodies using Pydantic models

See `model.py` for using `Pydantic` models.

See:

- [Pydantic](https://docs.pydantic.dev/latest/)

### Path and query parameters

```python
@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="The ID of the todo to retrieve.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    return {
        "message": "Todo with supplied ID doesn't exist."
    }
```

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/todo/2' \
  -H 'accept: application/json'
{"todo":{"id":2,"item":"Validation models help with input types"}}
```

See:

- [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [Request Body](https://fastapi.tiangolo.com/tutorial/body/)

### Documentation

Fast API exposes documentation in both `ReDoc` and interactive `Swagger`. Hit the urls:

- [Swagger](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

You can define examples for the objects your API can receive:

```python
class TodoItem(BaseModel):
  item: str
  model_config = {
    "json_schema_extra": {
      "examples": [
        {
          "item": "Todo item example",
        }
      ]
    }
  }
```

See:

- [Schema examples](https://fastapi.tiangolo.com/tutorial/schema-extra-example/)
