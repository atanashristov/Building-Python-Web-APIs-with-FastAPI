# Building Python Web APIs with FastAPI

Code and notes from studying [Building Python Web APIs with FastAPI](https://github.com/PacktPublishing/Building-Python-Web-APIs-with-FastAPI)

Run the `plannert` project:

```sh
python.exe -m pip install --upgrade pip
cd planner
env/Scripts/activate
pip install -r requirements.txt
# python main.py
uvicorn api:app --port 8000 --reload
```

Run the `todos` project:

```sh
python.exe -m pip install --upgrade pip
cd todos
env/Scripts/activate
pip install -r requirements.txt
uvicorn api:app --port 8000 --reload
```

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

## Chapter 3: Response Models and Error Handling

### Response models

Add model to `model.py`:

```python
class TodoItem(BaseModel):
  item: str

class TodoItems(BaseModel):
  todos: List[TodoItem]
  model_config = {
    "json_schema_extra": {
      "examples": [
        {
          "todos": [
            {
              "item": "This todo will be retrieved without exposing my ID!"
            },
            {
              "item": "And so is this one."
            }
          ]
        }
      ]
    }
  }
```

Then change the route in `todo.py`, specify the type of the response will be `response_model=TodoItems`:

```python
@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos() -> dict:
  return {"todos": todo_list}
```

If you get the todos, you will see that the ID is not returned:

```sh
$ curl -X 'GET'   'http://127.0.0.1:8000/todo'   -H 'accept: application/json'
{"todos":[{"item":"First Todo is to finish this book!"}]}
```

### Error handling

In `todo.py` file import `HTTPException, status` from `fastapi` and add exception:

```python
@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="The ID of the todo to be updated")) -> dict:
...
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )
```

```sh
$ curl -i -X 'GET'   'http://localhost:8000/todo/2'   -H 'accept: application/json'
HTTP/1.1 404 Not Found

{"detail":"Todo with supplied ID doesn't exist"}
```

### Override the default HTTP status code

Edit file `todo.py` and set `status_code=201` for the method:

```python
@todo_router.post("/todo", status_code=201)
async def add_todo(todo: Todo) -> dict:
...
```

## Chapter 4: Templating in FastAPI

Install `jinja2`:

```sh
pip install jinja2
pip install python-multipart
pip freeze > requirements.txt
pip install -r requirements.txt
```

Make templates directory and files:

```sh
mkdir templates
cd templates
touch {home,todo}.html
```

See:

- [Jinja filters](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters)

## Chapter 5: Structuring FastAPI Applications

Building an event planner with application structure to look like this:

```sh
planner/
  main.py
  database/
    __init__.py
    connection.py
  routes/
    __init__.py
    events.py
    users.py
  models/
    __init__.py
    events.py
    users.py
```

This is how the environment is initialized:

```sh
python.exe -m pip install --upgrade pip
pip install virtualenv
mkdir planner && cd planner
virtualenv env
env/Scripts/activate
pip install fastapi uvicorn "pydantic[email]"
pip install jinja2 python-multipart
pip freeze > requirements.txt
pip install -r requirements.txt
python3 -m pip list
```

To signup an user:

```sh
$ curl -i -X 'POST'   'http://127.0.0.1:8000/user/signup'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "email": "fastapi@packt.com",
  "password": "Stro0ng!",
  "username": "FastPackt"
}'
HTTP/1.1 200 OK
date: Sat, 07 Oct 2023 03:35:40 GMT
server: uvicorn
content-length: 43
content-type: application/json

{"message":"User successfully registered!"}
```

Error signup an user:

```sh
$ curl -i -X 'POST'   'http://127.0.0.1:8000/user/signup'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "email": "fastapi@packt.com",
  "password": "Stro0ng!",
  "username": "FastPackt"
}'
HTTP/1.1 409 Conflict
date: Sat, 07 Oct 2023 03:36:04 GMT
server: uvicorn
content-length: 47
content-type: application/json

{"detail":"User with supplied username exists"}
```

To signin an user:

```sh
$ curl -i -X 'POST'   'http://127.0.0.1:8000/user/signin'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "email": "fastapi@packt.com",
  "password": "Stro0ng!"
}'
HTTP/1.1 200 OK
date: Sat, 07 Oct 2023 03:37:17 GMT
server: uvicorn
content-length: 41
content-type: application/json

{"message":"User signed in successfully"}
```

Error signin user:

```sh
$ curl -i -X 'POST'   'http://127.0.0.1:8000/user/signin'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "email": "fastapi12345@packt.com",
  "password": "Stro0ng!"
}'
HTTP/1.1 404 Not Found
date: Sat, 07 Oct 2023 03:37:53 GMT
server: uvicorn
content-length: 32
content-type: application/json

{"detail":"User does not exist"}
```

Create event:

```sh
$ curl -i -X 'POST' 'http://127.0.0.1:8000/event/new' -H 'accept: application/json' -H 'Content-Type: application/json'   -d '{
  "id": 1,
  "title": "FastAPI Book Launch",
  "image": "https://linktomyimage.com/image.png",
  "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
  "tags": [
    "python",
    "fastapi",
    "book",
    "launch"
  ],
  "location": "Google Meet"
}'
HTTP/1.1 200 OK
date: Sat, 07 Oct 2023 03:46:44 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"message":"Event created successfully"}
```

Get events:

```sh
$ curl -i -X 'GET' 'http://127.0.0.1:8000/event/' -H 'accept: application/json'
HTTP/1.1 200 OK
date: Sat, 07 Oct 2023 03:47:07 GMT
server: uvicorn
content-length: 288
content-type: application/json

[{"id":1,"title":"FastAPI Book Launch","image":"https://linktomyimage.com/image.png","description":"We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!","tags":["python","fastapi","book","launch"],"location":"Google Meet"}]
```

Get one event by ID:

```sh
$ curl -i -X 'GET' 'http://127.0.0.1:8000/event/1' -H 'accept: application/json'
HTTP/1.1 200 OK
date: Sat, 07 Oct 2023 03:47:43 GMT
server: uvicorn
content-length: 286
content-type: application/json

{"id":1,"title":"FastAPI Book Launch","image":"https://linktomyimage.com/image.png","description":"We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!","tags":["python","fastapi","book","launch"],"location":"Google Meet"}
```

Error get one event by ID:

```sh
$ curl -i -X 'GET' 'http://127.0.0.1:8000/event/0' -H 'accept: application/json'
HTTP/1.1 404 Not Found
date: Sat, 07 Oct 2023 03:48:13 GMT
server: uvicorn
content-length: 50
content-type: application/json

{"detail":"Event with supplied ID does not exist"}
```

Delete event by ID:

```sh
$ curl -i -X 'DELETE' \
  'http://127.0.0.1:8000/event/1' \
  -H 'accept: application/json'
HTTP/1.1 200 OK
date: Sat, 07 Oct 2023 03:49:08 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"message":"Event deleted successfully"}
```

Error delete event by ID:

```sh
$ curl -i -X 'DELETE' 'http://127.0.0.1:8000/event/0' -H 'accept: application/json'
HTTP/1.1 404 Not Found
date: Sat, 07 Oct 2023 03:49:37 GMT
server: uvicorn
content-length: 50
content-type: application/json

{"detail":"Event with supplied ID does not exist"}
```

See:

- [Code](https://github.com/PacktPublishing/Building-Python-Web-APIs-with-FastAPI/tree/main/ch05/planner)

## Chapter 6: Connecting to a Database

Explains how to connect to a SQL database using SQLModel and a MongoDB database via Beanie.

Add dependencies:

```sh
cd planner
env/Scripts/activate # or bash: source env/Scripts/activate
pip install sqlmodel
pip freeze > requirements.txt
pip install -r requirements.txt
python3 -m pip list
```

Define SQL model:

```python
from sqlmodel import Field, SQLModel, Optional

class Event(SQLModel, BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
...
```

See:

- [pip sqlmodel](https://pypi.org/project/sqlmodel/)
