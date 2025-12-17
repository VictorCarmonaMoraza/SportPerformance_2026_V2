from datetime import date

def getFechas(year: int):
    fecha_inicio = date(year, 1, 1)
    fecha_fin = date(year + 1, 1, 1)
    return fecha_inicio, fecha_fin

