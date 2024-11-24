from enum import Enum

class UserType(str, Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    MEMBER = "member"

    @classmethod
    def as_choices(cls):
        return [(member.value, member.name) for member in cls] 
    