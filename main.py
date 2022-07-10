from os import path

from fastapi import FastAPI

from patkai.database import engine
from patkai.models import admin_model as model
from patkai.routers import admin_crud, boarders

app = FastAPI()

# Create all tables
model.Base.metadata.create_all(bind=engine)

@app.get("/")
def status():
    return {"status": 200}

# Register routers
app.include_router(admin_crud.construct_router())
app.include_router(boarders.construct_router())

