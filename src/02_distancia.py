import numpy as np
import pandas as pd

RADIO_TIERRA_KM = 6371.0
RUTA_DATASETS = "datasets"


# Fórmula del semiverseno (haversine): calcula distancia en línea recta
# entre dos puntos de la esfera terrestre usando latitud/longitud.
# a = sin²(Δlat/2) + cos(lat1)·cos(lat2)·sin²(Δlon/2)
# c = 2·arcsin(√a)  →  distancia = R·c  (R = 6371 km)
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))
    return RADIO_TIERRA_KM * c


def cargar_geo():
    return pd.read_csv(f"{RUTA_DATASETS}/olist_geolocation_dataset.csv")


def cargar_sellers():
    return pd.read_csv(f"{RUTA_DATASETS}/olist_sellers_dataset.csv")


def asignar_coordenadas(df, geo, prefijo_col, sufijo):
    lat_col = f"lat_{sufijo}"
    lon_col = f"lng_{sufijo}"
    geo_agg = geo.groupby("geolocation_zip_code_prefix").agg(
        lat=("geolocation_lat", "first"),
        lng=("geolocation_lng", "first"),
    ).reset_index()
    geo_agg.columns = ["geolocation_zip_code_prefix", lat_col, lon_col]
    df = df.merge(
        geo_agg, left_on=prefijo_col, right_on="geolocation_zip_code_prefix",
        how="left"
    )
    return df


def calcular_distancias(orders, customers, items, sellers, geo):
    merged = orders.merge(
        items[["order_id", "seller_id", "price", "freight_value"]],
        on="order_id", how="inner"
    )
    merged = merged.merge(
        customers,
        on="customer_id", how="left"
    )
    merged = merged.merge(
        sellers,
        on="seller_id", how="left"
    )
    merged = asignar_coordenadas(
        merged, geo, "customer_zip_code_prefix", "customer"
    )
    merged = asignar_coordenadas(
        merged, geo, "seller_zip_code_prefix", "seller"
    )
    valido = merged.dropna(subset=["lat_customer", "lng_customer",
                                    "lat_seller", "lng_seller"])
    valido["distancia_km"] = haversine(
        valido["lat_customer"], valido["lng_customer"],
        valido["lat_seller"], valido["lng_seller"]
    )
    return valido
