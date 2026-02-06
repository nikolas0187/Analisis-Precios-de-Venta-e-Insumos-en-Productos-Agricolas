# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 20:47:07 2026

@author: nikol
"""

import pandas as pd

precios = pd.read_csv('precios_2021_2025.csv')

insumos = pd.read_csv('insumos_filtrados.csv')

pd_precios = precios.copy()

pd_insumos = insumos.copy()

# Igualo los nombres de la columna municipio y fecha para análisis

pd_insumos = pd_insumos.rename(columns={
    'Nombre municipio': 'municipio'
    })

pd_precios = pd_precios.rename(columns={
    'Fecha': 'fecha'
    })
   
pd_precios.columns
pd_insumos.columns 

# Verifico si municipios coinciden entre precios e insumos

set_precios = set(pd_precios['municipio'].unique())
set_insumos = set(pd_insumos['municipio'].unique())

# Verfico cuales estan en precios y no en insumos
solo_precios = set_precios - set_insumos

# Verifico cuales estan en insumos y no en precios
solo_insumos = set_insumos - set_precios

# saco municipios comunes

municipios_comunes = set_precios & set_insumos 

# Filtro datasets solo con esos municipios

pd_precios = pd_precios[pd_precios['municipio'].isin(municipios_comunes)]

pd_insumos = pd_insumos[pd_insumos['municipio'].isin(municipios_comunes)]

# Verifico fechas comunes

fechas_precios = pd_precios['fecha'].unique()
fechas_insumos = pd_insumos['fecha'].unique()

fechas_comunes = set(fechas_precios).intersection(set(fechas_insumos))

len(fechas_comunes)
sorted(fechas_comunes)

# Filtro datasets con fechas comunes

pd_precios = pd_precios[pd_precios['fecha'].isin(fechas_comunes)]

pd_insumos = pd_insumos[pd_insumos['fecha'].isin(fechas_comunes)]

pd_insumos.nunique()
pd_precios.nunique()

pd_precios['fecha'].min(), pd_precios['fecha'].max()
pd_insumos['fecha'].min(), pd_insumos['fecha'].max()

# Verfico productos y tipos de insumos 

pd_precios['Producto'].nunique()
pd_insumos['tipo_insumo'].nunique()

pd_precios['Producto'].unique()[:50]

pd_precios['Producto'].value_counts()

# Me quedo con los productos del datasets precios que tienen mas de 500 registros

conteo_productos = pd_precios['Producto'].value_counts()

productos_validos = conteo_productos[conteo_productos > 500].index

pd_precios = pd_precios[pd_precios['Producto'].isin(productos_validos)]

pd_precios['Producto'].value_counts()

# Creo dataset agrupado por municipio, fecha, producto y precio promedio
# en pd_precios

pd_precios.columns

precios_municipio_mensual = (
    pd_precios
    .groupby(['municipio', 'fecha', 'Producto'], as_index=False)
    ['Precio_kg']
    .mean()
    )

precios_municipio_mensual = precios_municipio_mensual.rename(
    columns={
        'Precio_kg': 'precio_promedio_kg',
        'Producto': 'producto'
        }
    )

# Creo dataset agrupado por municipio, fecha, producto y precio promedio
# en pd_insumos

pd_insumos.columns

insumos_municipio_mensual = (
    pd_insumos
    .groupby(['municipio', 'fecha'], as_index=False)
    ['Precio promedio'].mean()
    )

insumos_municipio_mensual = insumos_municipio_mensual.rename(
    columns={'Precio promedio': 'precio_promedio'}
    )

# Uno las dos bases de datos para el análisis

dataset_analisis = precios_municipio_mensual.merge(
    insumos_municipio_mensual,
    on=['municipio', 'fecha'],
    how='left'
    )

# Verifico tipo de datos y corrijo

dataset_analisis.dtypes

dataset_analisis['fecha'] = pd.to_datetime(dataset_analisis['fecha'])

# Verifico nulos

dataset_analisis.isnull().sum()

# Realizo interpolación lineal para compensar nulos

dataset_analisis['precio_promedio'] = (
    dataset_analisis
    .sort_values(['municipio', 'fecha'])
    .groupby('municipio')['precio_promedio']
    .transform(lambda x: x.interpolate())
    )

dataset_analisis.isnull().sum()

# Creo KPI principal en dataset unido

dataset_analisis['relacion_precio_insumo'] = (
    dataset_analisis['precio_promedio_kg'] / 
    dataset_analisis['precio_promedio']
    )

# Margen relativo

dataset_analisis['margen_relativo'] = (
    dataset_analisis['precio_promedio_kg'] - 
    dataset_analisis['precio_promedio']
    )                                                 

# Extraigo año y mes

dataset_analisis['anio'] = dataset_analisis['fecha'].dt.year
dataset_analisis['mes'] = dataset_analisis['fecha'].dt.month

# Verifico nulos

dataset_analisis.isnull().sum()

# Analizo el comportamiento con el tiempo 

import matplotlib.pyplot as plt 

dataset_analisis.groupby('fecha')[['precio_promedio_kg', 'precio_promedio']].mean().plot()
plt.show()

# Evolucion margen relativo 

margen_tiempo = dataset_analisis.groupby('fecha')['margen_relativo'].mean()

plt.figure(figsize=(10,5))
plt.plot(margen_tiempo.index, margen_tiempo.values)

plt.title('Evolución del margen relativo en el tiempo')
plt.ylabel('Margen relativo')
plt.xlabel('Fecha')

plt.show()

# Margen por municipio 
margen_municipio = (
    dataset_analisis.groupby('municipio')['margen_relativo']
    .mean()
    .sort_values()
    )


# Visualizo margen por municipio (10 con peor margen)

margen_municipio.head(10).plot(kind='barh')

plt.title('Municipios con peor margen relativo')
plt.xlabel('Margen promedio')
plt.ylabel('Municipio')

plt.show()

# Visualizo margen por municipio (10 con mejor margen)

margen_municipio.tail(10).plot(kind='barh')

plt.title('Municipios con mejor margen relativo')
plt.xlabel('Margen promedio')
plt.ylabel('Municipio')

plt.show()


# Exporto dataset para analizar en power BI

dataset_analisis.to_csv('dataset_powerbi.csv', index=False)

