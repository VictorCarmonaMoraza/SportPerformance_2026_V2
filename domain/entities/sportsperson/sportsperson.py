class Sportsperson:
    def __init__(
            self,
            id: int,
            usuario_id: int | None = None,
            nombre: str | None = None,
            edad: int | None = None,
            disciplina_deportiva: str | None = None,
            nacionalidad: str | None = None,
            telefono: str | None = None,
            foto_url: str | None = None,
            tiene_foto: bool = False
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.edad = edad
        self.disciplina_deportiva = disciplina_deportiva
        self.nacionalidad = nacionalidad
        self.telefono = telefono
        self.foto_url = foto_url
        self.tiene_foto = tiene_foto
