# Asigna vehículo según distancia para estimar consumo de combustible (no hay dato real de flota)
VEHICULOS = [
    {"tipo": "Furgoneta Urbana", "dist_max": 50, "rendimiento": 30},
    {"tipo": "Camión Rígido", "dist_max": 400, "rendimiento": 18},
    {"tipo": "Tráiler Articulado", "dist_max": float("inf"), "rendimiento": 10},
]


def asignar_vehiculo(distancia_km):
    for v in VEHICULOS:
        if distancia_km < v["dist_max"]:
            return v["tipo"], v["rendimiento"]
    return "Tráiler Articulado", 10


def asignar_flota(df):
    resultado = zip(*df["distancia_km"].apply(asignar_vehiculo))
    tipos, rendimientos = resultado
    df["tipo_vehiculo"] = list(tipos)
    df["rendimiento_km_gal"] = list(rendimientos)
    return df
