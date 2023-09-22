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

See:

- [Pip and virtualenv on Windows](https://programwithus.com/learn/python/pip-virtualenv-windows)

## Chapter 2: Routing in FastAPI
