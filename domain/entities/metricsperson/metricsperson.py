from datetime import date
from decimal import Decimal


class Metricsperson:
    def __init__(
        self,
        id: int,
        deportista_id: int,
        fecha: date,
        peso: Decimal | None = None,
        altura: Decimal | None = None,
        frecuencia_cardiaca: int | None = None,
        velocidad_media: Decimal | None = None,
        distancia: Decimal | None = None,
        calorias: int | None = None
    ):
        self.id = id
        self.deportista_id = deportista_id
        self.fecha = fecha
        self.peso = peso
        self.altura = altura
        self.frecuencia_cardiaca = frecuencia_cardiaca
        self.velocidad_media = velocidad_media
        self.distancia = distancia
        self.calorias = calorias
