# domain/entities/user/user.py
from datetime import datetime
from typing import Optional


class User:
    def __init__(
            self,
            id: int,
            username: str,
            email: str,
            password_hash: str,
            rol: str,
            created: Optional[datetime] = None,
            has_photo: bool = False
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.rol = rol
        self.created = created or datetime.utcnow()
        self.has_photo = has_photo
