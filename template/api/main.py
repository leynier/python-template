from os.path import join

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from .v1.main import api as api_v1

api = FastAPI(docs_url=None, redoc_url=None)

api.mount("/v1", api_v1)


@api.get("/", include_in_schema=False)
def index(request: Request):
    return RedirectResponse(join(request.url.path, "v1", ""))
