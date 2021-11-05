from enum import Enum

class User(Enum):
    GUEST = 0
    STUDENT = 1
    FACULTY = 2
    STAFF = 3

class Option(Enum):
    ADD = 0
    UPDATE = 1
