# domain/entities/user/user.py
from datetime import datetime


class User:
    ## Constructor
    def __init__(self, id: int, username: str, password_hash: str, rol: str, created: datetime | None = None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.created = created or datetime.utcnow()
