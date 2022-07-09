from operator import attrgetter
from unicodedata import category
from pydantic import BaseModel

class Boarder(BaseModel):
    wing: str
    room: str
    seat: str
    name: str
    rollno: str
    programme: str
    contact: str
    category: str
    guardian: str
    guardian_contact: str
    address: str