# Eficiencia de Combustible — Análisis Logístico Olist

Pipeline de preprocesamiento y dashboard analítico para medir eficiencia de combustible en entregas del e-commerce brasileño Olist. Construido con **Python/Pandas** + **Power BI**.

---

## Stack Tecnológico

| Componente | Herramienta |
|---|---|
| Preprocesamiento | Python 3.13, Pandas, NumPy |
| Visualización | Power BI |
| Georreferenciación | Fórmula del Semiverseno (Haversine) |
| Datos | Olist Brazilian E-Commerce (Kaggle) |

---

## Pipeline (Fase 1: Python/Pandas)

```
datasets/ → 01_limpieza → 02_distancia → 03_flota → 04_exportar → CSV
```

### 1. Limpieza Inicial
- Carga de datasets: orders, order_items, customers, sellers, geolocation
- Filtro de pedidos con estado `delivered`
- Eliminación de registros con coordenadas nulas

### 2. Cálculo de Distancia (Haversine)

La distancia real entre dos puntos sobre la esfera terrestre se calcula con la fórmula del semiverseno:

```
a = sen²(Δφ/2) + cos(φ₁)·cos(φ₂)·sen²(Δλ/2)
c = 2 · arcsen(√a)
d = R · c    (R = 6371 km)
```

Donde:
- `φ` = latitud, `λ` = longitud (en radianes)
- `R` = radio de la Tierra (≈ 6371 km)
- `d` = distancia en línea recta (distancia geodésica)

**Justificación:** Haversine es la fórmula estándar para distancias geodésicas sin necesidad de API externa de rutas. Es el punto de partida óptimo para análisis agregado de eficiencia logística.

### 3. Asignación de Flota
Asignación determinista por umbrales de distancia para estimar consumo de combustible (no hay dato real de vehículo):

| Distancia | Vehículo | Rendimiento |
|---|---|---|
| < 50 km | Furgoneta Urbana | 30 km/gal |
| 50 – 400 km | Camión Rígido | 18 km/gal |
| ≥ 400 km | Tráiler Articulado | 10 km/gal |

### 4. Exportación
CSV unificado con 109,661 registros y 19 columnas listo para Power BI.

---

## Modelo de Datos (Fase 2: Esquema Estrella)

```
┌────────────────┐     ┌─────────────────┐
│  Dim_Calendario │     │  Fact_Despachos │
│  (Date, Year,   │────>│  (order_id,     │
│   Month, etc)   │     │   customer_id,  │
└────────────────┘     │   seller_id,     │
                        │   distancia_km,  │
┌────────────────┐     │   freight_value, │
│  Dim_Vehiculos  │────>│   price,         │
│  (tipo,         │     │   fechas...)    │
│   rendimiento)  │     └─────────────────┘
└────────────────┘
```

**Relaciones:**
- `Dim_Vehiculos[Tipo_Vehiculo]` → `Fact_Despachos[tipo_vehiculo]` (1:\*, activa)
- `Dim_Calendario[Date]` → `Fact_Despachos[order_purchase_timestamp]` (1:\*, activa)
- `Dim_Calendario[Date]` → fechas de entrega/promesa (1:\*, inactivas)

---

## Medidas DAX (Fase 3)

### Inteligencia de Tiempo
```DAX
Dias_Desviacion = DATEDIFF(order_estimated_delivery_date, order_delivered_customer_date, DAY)

Entregas_A_Tiempo = CALCULATE(COUNTROWS(Fact_Despachos), Dias_Desviacion <= 0)
```

### Rentabilidad Logística
```DAX
Consumo_Galones = SUMX(Fact_Despachos, distancia_km / RELATED(Dim_Vehiculos[rendimiento_km_gal]))

Costo_Operativo_Combustible = [Consumo_Galones] * 4.50

Margen_Flete = SUM(Fact_Despachos[freight_value]) - [Costo_Operativo_Combustible]
```

---

## Dashboard (Fase 4)

**Pregunta guía:** *¿En qué rutas estamos perdiendo eficiencia y dinero?*

| Nivel | Visual | Propósito |
|---|---|---|
| Nivel 1 | Tarjetas KPI | OTD %, Margen Flete Total, Promedio Retraso |
| Nivel 2 | Mapa | Volumen de envíos (tamaño) y retraso (color) |
| Nivel 3 | Scatter Plot | Correlación distancia vs días de desviación |
| Nivel 3 | Matriz | Rentabilidad por Estado Origen > Estado Destino > Vehículo |

---

## Cómo Ejecutar el Pipeline

```bash
pip install pandas numpy
python main.py
```

El CSV de salida se genera en `output/entregas_enriquecidas.csv`.

---

## Dataset

Olist Brazilian E-Commerce Public Dataset (Kaggle): órdenes, ítems, clientes, vendedores y geolocalización de Brasil.
