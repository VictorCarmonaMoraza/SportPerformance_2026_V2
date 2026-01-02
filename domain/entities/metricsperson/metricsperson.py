from datetime import date, datetime
from decimal import Decimal


class Metricsperson:
    def __init__(
        self,
        id: int,
        deportista_id: int,
        fecha: date,

        # Datos físicos
        peso: Decimal | None = None,
        altura: Decimal | None = None,

        # Cardio
        frecuencia_cardiaca: int | None = None,
        fc_media: int | None = None,
        fc_max: int | None = None,

        # Rendimiento
        velocidad_media: Decimal | None = None,
        distancia: Decimal | None = None,
        duracion_min: int | None = None,
        ritmo_medio: Decimal | None = None,
        rpe: int | None = None,
        calorias: int | None = None,

        # Auditoría (normalmente BD)
        created_at: datetime | None = None
    ):
        self.id = id
        self.deportista_id = deportista_id
        self.fecha = fecha

        self.peso = peso
        self.altura = altura

        self.frecuencia_cardiaca = frecuencia_cardiaca
        self.fc_media = fc_media
        self.fc_max = fc_max

        self.velocidad_media = velocidad_media
        self.distancia = distancia
        self.duracion_min = duracion_min
        self.ritmo_medio = ritmo_medio
        self.rpe = rpe
        self.calorias = calorias

        self.created_at = created_at
