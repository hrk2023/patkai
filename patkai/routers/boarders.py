import csv
from distutils.command.upload import upload
from os import path

from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination, paginate
from patkai.schemas.boarders import Boarder


def construct_router():

    boarders = APIRouter(
        prefix = "/boarders",
        tags = ["boarders"]
    )

    @boarders.get("/all", response_model=Page[Boarder])
    def get_boarders():
        try:

            filepath = path.abspath(path.dirname(path.dirname(__file__)))
            upload_dir = path.join(filepath, 'uploads')
            with open(path.join(upload_dir,'boarders.csv'), 'r') as csv_file:
                reader = csv.reader(csv_file)

                output = []

                for row in reader:
                    entry = {
                        "wing" : row[0],
                        "room" : row[1],
                        "seat" : row[2],
                        "name" : row[3],
                        "rollno" : row[4],
                        "programme" : row[5],
                        "contact" : row[6],
                        "category" : row[7],
                        "guardian" : row[8],
                        "guardian_contact" : row[9],
                        "address" : row[10]
                    }
                    boarder = Boarder(**entry)

                    output.append(boarder)

                return paginate(output)

        except Exception as e:
            print(e)
            return {"status": 400, "detail": "an unexpected error occured"}
    


    add_pagination(boarders)

    return boarders
