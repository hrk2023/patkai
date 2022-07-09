from os import path

from dotenv import load_dotenv
from fastapi import FastAPI

from patkai.database import engine
from patkai.models import admin_model as model
from patkai.routers import admin_crud, boarders


def main():

    app = FastAPI()

    BASE_PATH = path.abspath(path.dirname(path.dirname(__file__)))
    load_dotenv(path.join(BASE_PATH,".env"))

    # Create all tables
    model.Base.metadata.create_all(bind=engine)

    @app.get("/")
    def status():
        return "<h1>Running</h1>"

    # Register routers
    app.include_router(admin_crud.construct_router())
    app.include_router(boarders.construct_router())

    return app
