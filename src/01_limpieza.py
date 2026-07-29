import pandas as pd

RUTA_DATASETS = "datasets"


def cargar_datos():
    orders = pd.read_csv(f"{RUTA_DATASETS}/olist_orders_dataset.csv")
    items = pd.read_csv(f"{RUTA_DATASETS}/olist_order_items_dataset.csv")
    customers = pd.read_csv(f"{RUTA_DATASETS}/olist_customers_dataset.csv")
    return orders, items, customers


def filtrar_entregados(orders):
    return orders.loc[orders["order_status"] == "delivered"].copy()


def ejecutar():
    orders, items, customers = cargar_datos()
    orders = filtrar_entregados(orders)
    return orders, items, customers
