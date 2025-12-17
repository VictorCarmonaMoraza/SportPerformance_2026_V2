from datetime import date, timedelta


def getFechas(year: int):
    fecha_inicio = date(year, 1, 1)
    fecha_fin = date(year + 1, 1, 1)
    return fecha_inicio, fecha_fin


def getLastYear(date_current: date, n_dias: int):
    fecha_fin = date_current
    fecha_inicio = date_current - timedelta(days=n_dias)
    return fecha_inicio, fecha_fin
