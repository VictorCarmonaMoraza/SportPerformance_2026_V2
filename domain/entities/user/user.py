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
        foto_url: Optional[str] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.rol = rol
        self.created = created or datetime.utcnow()
        self.foto_url = foto_url

    @property
    def has_photo(self) -> bool:
        return self.foto_url is not None
