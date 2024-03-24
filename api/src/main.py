import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from api.views import router

app = FastAPI(
    docs_url='/docs',
    openapi_url='/docs.json',
    default_response_class=ORJSONResponse,
)

static_dir = os.path.join(Path(__file__).parents[2], 'generated')
app.mount("/generated", StaticFiles(directory=static_dir))

app.include_router(router, prefix='/api/v1')
