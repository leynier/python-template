from os.path import join

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

api = FastAPI(title="FastAPI Template")


@api.get("/", include_in_schema=False, tags=["General"])
def index(request: Request):
    return RedirectResponse(join(request.url.path, "docs"))


@api.get("/hello-world", tags=["General"])
def run():
    return {"message": "Hello World!"}
