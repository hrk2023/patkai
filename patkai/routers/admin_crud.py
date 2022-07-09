from contextlib import contextmanager
from datetime import datetime
from os import path
from uuid import uuid4

import pytz
from fastapi import APIRouter, File, HTTPException, UploadFile
from passlib.hash import pbkdf2_sha256
from patkai.database import SessionLocal
from patkai.models import admin_model as model
from patkai.schemas import admin_schema
from sqlalchemy import inspect


@contextmanager
def db_session(session):

    try:
        yield session

    finally:
        session.close()


def construct_router():

    admin = APIRouter(
        prefix = "/admin",
        tags = ["admin"]
    )

    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


    @admin.get("/all")
    def list_admins(limit: int = 10):
        with db_session(SessionLocal()) as db:
            admins = db.query(model.Admin).filter()
            output = []
            for admin in admins:
                output.append(object_as_dict(admin))
                print(type(admin))
            if len(output) != 0:
                return output
        
        return HTTPException(status_code=404, detail="no users found")

    @admin.get("/")
    def get_admins(id: str):
        with db_session(SessionLocal()) as db:
            admin = db.query(model.Admin).filter(model.Admin.id == id).first()
            print(type(admin))
            if admin is not None:
                admin = object_as_dict(admin)
                return admin
        
        return HTTPException(status_code=404, detail="user not found")

    @admin.post("/create")
    def create_admin(admin: admin_schema.Admin):
        admin = model.Admin(**admin.dict())
        admin.password = pbkdf2_sha256.hash(admin.password)

        with db_session(SessionLocal()) as db:
            user = db.query(model.Admin).filter(model.Admin.id == admin.id).first()

            if user is not None:
                return HTTPException(status_code=400, detail="user already exists")

            admin.id = str(uuid4())

            db.add(admin)
            db.commit()
        
        return {"status": 200, "detail": "admin created"}

    @admin.put("/update")
    def update_admin(id: str, admin: admin_schema.Admin):
        
        if id is None:
            return HTTPException(status_code=404, detail="empty query parameter id")

        with db_session(SessionLocal()) as db:
            user = db.query(model.Admin).filter(model.Admin.id == id).first()

            if user is None:
                return HTTPException(status_code=404, detail="user not found")

            user.updated_at = datetime.now(pytz.timezone("Asia/Kolkata"))
            user.username = admin.username
            user.is_active = admin.is_active
            user.password = pbkdf2_sha256.hash(admin.password)

            db.commit()
        
        return {"status": 200, "detail": "admin updated"}

    @admin.delete("/delete")
    def delete_admin(id: str):
        if id is None:
            return HTTPException(status_code=400, detail="empty query parameter id")

        with db_session(SessionLocal()) as db:
            user = db.query(model.Admin).filter(model.Admin.id == id).first()

            if user is None:
                return HTTPException(status_code=404, detail="user not found")

            db.delete(user)
            db.commit()
        
        return {"status": 200, "detail": "admin deleted"}


    @admin.post("/upload")
    def upload_file(data: UploadFile = File(...)):

        try:
            filepath = path.abspath(path.dirname(path.dirname(__file__)))
            upload_dir = path.join(filepath, 'uploads')
            ext = data.filename.split(".")[-1]

            open(path.join(upload_dir, f"boarders.{ext}"), 'wb').write(data.file.read())

            return {"filename": data.filename}

        except Exception as e:

            return {"status": 500, "detail": "file upload cancelled"}



    return admin

