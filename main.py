import importlib
import sys

# Punto de entrada: orquesta los 4 pasos del pipeline (limpieza → distancia → flota → exportar)

sys.path.insert(0, "src")
step01 = importlib.import_module("01_limpieza")
step02 = importlib.import_module("02_distancia")
step03 = importlib.import_module("03_flota")
step04 = importlib.import_module("04_exportar")


def main():
    orders, items, customers = step01.ejecutar()
    sellers = step02.cargar_sellers()
    geo = step02.cargar_geo()
    df = step02.calcular_distancias(orders, customers, items, sellers, geo)
    df = step03.asignar_flota(df)
    step04.exportar_csv(df)


if __name__ == "__main__":
    main()
