import pandas as pd

RUTA_SALIDA = "output/entregas_enriquecidas.csv"

COLUMNAS_FINALES = [
    "order_id",
    "customer_id",
    "seller_id",
    "customer_city",
    "customer_state",
    "lat_customer",
    "lng_customer",
    "seller_city",
    "seller_state",
    "lat_seller",
    "lng_seller",
    "distancia_km",
    "tipo_vehiculo",
    "rendimiento_km_gal",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "price",
    "freight_value",
]


def exportar_csv(df):
    df = df[COLUMNAS_FINALES].copy()
    df.to_csv(RUTA_SALIDA, index=False)
    print(f"Exportado: {RUTA_SALIDA} ({len(df)} registros)")
    return df
