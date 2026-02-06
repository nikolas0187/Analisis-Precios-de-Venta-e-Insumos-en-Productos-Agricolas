# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 14:57:44 2026

@author: nikol
"""

import pandas as pd

## Limpieza de datos 2021 ## 

df_2021 = pd.read_excel('series-historicas-precios-mayoristas-2021.xlsx',
                        sheet_name=None, header=6
                        )

# Elimino hoja índice inncesaria

df_2021_sin_indice = {
    k: v for k, v in df_2021.items()
    if k != 'Índice'
    }

df_2021_sin_indice.keys()

# Elimino filas basura al final de las hojas

for mes, df in df_2021_sin_indice.items():
    ultima_fila_2021 = df['Producto'].last_valid_index()
    df_2021_sin_indice[mes] = df.loc[:ultima_fila_2021]
    
df_2021_sin_indice['Ene 21'].tail()

# Elimino columas al final vacías

for mes, df in df_2021_sin_indice.items():
    df_2021_sin_indice[mes] = df.dropna(axis=1, how='all')

# Creo columa mes en cada hoja

for mes, df in df_2021_sin_indice.items():
    df['mes'] = mes

df_2021_sin_indice['Ene 21'].head(2)

# Concateno todos los meses en un dataframe

df_2021_final = pd.concat(df_2021_sin_indice.values(), ignore_index=True)

df_2021_final.isnull().sum()   

# Consulto tipo de datos y corrijo

df_2021_final.dtypes

df_2021_final['Fecha'] = pd.to_datetime(df_2021_final['Fecha'],
                                        errors='coerce')

df_2021_final.dtypes

# Extraigo mes como número y año

df_2021_final['anio'] = df_2021_final['Fecha'].dt.year
df_2021_final['mes_num'] = df_2021_final['Fecha'].dt.month

# Reorganizo

df_2021_final.columns

df_2021_final = df_2021_final[[
    'Fecha',
    'anio',
    'mes_num',
    'Grupo',
    'Producto',
    'Mercado',
    'Precio promedio por kilogramo*'
    ]]

df_2021_final.columns


# Exporto 

df_2021_final.to_csv('precios_mayoristas_2021_limpio.csv', index=False)

### Limpieza de datos 2022 ##

df_2022 = pd.read_excel('series-historicas-precios-mayoristas-2022.xlsx',
                        sheet_name=None, header=6)

# Elimino hoja índice basura

df_2022_sin_indice = {
    k: v for k, v in df_2022.items()
    if k != 'Índice'
    }

# Elimino filas basuras al final de cada hoja

for mes, df in df_2022_sin_indice.items():
    ultima_fila_2022 = df['Producto'].last_valid_index()
    df_2022_sin_indice[mes] = df.loc[:ultima_fila_2022]
    
df_2022_sin_indice['Feb 22'].tail()

# Elimino columas vacias al final

for mes, df in df_2022_sin_indice.items():
    df_2022_sin_indice[mes] = df.dropna(axis=1, how='all')
    
# creo la columna mes en cada hoja para al momento de concatenar
# se conserve el orden

for mes, df in df_2022_sin_indice.items():
    df['mes'] = mes
    
df_2022_sin_indice['Mar 22'].head(5)

# Concateno

df_2022_final = pd.concat(df_2022_sin_indice.values(), ignore_index=True)

# consulto tipo de datos y corrijo

df_2022_final.dtypes

df_2022_final['Fecha'] = pd.to_datetime(df_2022_final['Fecha'],
                                        errors='coerce')

df_2022_final.dtypes

# Extraigo mes como numero y año

df_2022_final['anio'] = df_2022_final['Fecha'].dt.year
df_2022_final['mes_num'] = df_2022_final['Fecha'].dt.month

# Reorganizo 

df_2022_final.columns

df_2022_final = df_2022_final[[
    'Fecha',
    'anio',
    'mes_num',
    'Grupo',
    'Producto',
    'Mercado',
    'Precio promedio por kilogramo*'
    ]]

# Exporto limpio

df_2022_final.to_csv('precios_mayoristas_2022_limpio.csv', index=False)

## Limpieza de datos 2023 ##

df_2023 = pd.read_excel('anex-SIPSA-SerieHistoricaMayorista-Dic2023.xlsx', 
                        sheet_name=None, header=6
                        )

# Elimino hoja indice que es basura

df_2023_sin_indice = {
    k: v for k, v in df_2023.items()
    if k != 'Índice'
    } 

# Eliminamos filas basura al final de cada hoja

for mes, df in df_2023_sin_indice.items():
    ultima_fila_2023 = df['Producto'].last_valid_index()
    df_2023_sin_indice[mes] = df.loc[:ultima_fila_2023]

df_2023_sin_indice['Enero'].tail()

# Elimino columnas vacias en las hojas

for mes, df in df_2023_sin_indice.items():
    df_2023_sin_indice[mes] = df.dropna(axis=1, how='all')
    
# Creo la columna mes en cada hoja

for mes, df in df_2023_sin_indice.items():
    df['mes'] = mes

df_2023_sin_indice['Enero'].head()

# Ya lo puedo concatenar

df_2023_final = pd.concat(df_2023_sin_indice.values(), ignore_index=True)    

# Consulto nulos

df_2023_final.isnull().sum()

# Verfico y corrijo tipos de datos

df_2023_final.dtypes

df_2023_final['Fecha'] = pd.to_datetime(df_2023_final['Fecha'], 
                                        errors='coerce')

# Extraigo mes y anio

df_2023_final['anio'] = df_2023_final['Fecha'].dt.year
df_2023_final['mes_num'] = df_2023_final['Fecha'].dt.month

# Organizo columnas

df_2023_final.columns

df_2023_final = df_2023_final[[
    'Fecha',
    'anio',
    'mes_num',
    'Grupo',
    'Producto',
    'Mercado',
    'Precio promedio por kilogramo*']]

# Exporto base de datos unida y limpia

df_2023_final.to_csv('precios_mayoristas_2023_limpio.csv', index=False)

## Limpieza de datos 2024 ##

df_2024 = pd.read_excel('anex-SIPSA-SerieHistoricaMayorista-2024.xlsx',
                        header=5)

# Identifico nulos y los elimino

df_2024.isnull().sum()

ultima_fila_2024 = df_2024['Producto'].last_valid_index()

df_2024 = df_2024.loc[:ultima_fila_2024]

df_2024.isnull().sum()

# Identifico tipo de datos y corrijo

df_2024.dtypes

df_2024['Fecha'] = pd.to_datetime(df_2024['Fecha'], errors='coerce')

df_2024.dtypes

# Extraigo mes como número y año

df_2024['anio'] = df_2024['Fecha'].dt.year
df_2024['mes_num'] = df_2024['Fecha'].dt.month

# Reorganizo

df_2024.columns

df_2024 = df_2024[[
    'Fecha',
    'anio',
    'mes_num',
    'Grupo',
    'Producto',
    'Mercado',
    'Precio promedio por kilogramo*'
    ]]

df_2024.columns

# Exporto

df_2024.to_csv('precios_mayoristas_2024_limpio.csv', index=False)

## Limpieza de datos 2025 ## 

df_2025 = pd.read_excel('anex-SIPSA-SerieHistoricaMayorista-2025.xlsx',
                        header=5)

# Identifico nulos y corrijo

df_2025.isnull().sum()

ultima_fila_2025 = df_2025['Producto'].last_valid_index()

df_2025 = df_2025.loc[:ultima_fila_2025]

df_2025.isnull().sum()

# Identifico tipo de columnas y corrijo

df_2025.dtypes

df_2025['Fecha'] = pd.to_datetime(df_2025['Fecha'], errors='coerce')

df_2025.dtypes

# Extraigo mes como numero y anio

df_2025['anio'] = df_2025['Fecha'].dt.year
df_2025['mes_num'] = df_2025['Fecha'].dt.month

# Reorganizo
 
df_2025.columns


df_2025 = df_2025[[
    'Fecha',
    'anio',
    'mes_num',
    'Grupo',
    'Producto',
    'Mercado',
    'Precio promedio por kilogramo*'
    ]]

# Exporto

df_2025.to_csv('precios_mayoristas_2025_limpio.csv', index=False)

# Concateno todas las bases de datos en un dataframe

df_precios = pd.concat([df_2021, df_2022, df_2023, df_2024, df_2025], 
                       ignore_index=True
                       )

df_precios.info()
df_precios["anio"].value_counts()
df_precios.isnull().sum()

# Cambio el nombre de la columna de los precios para mejor visualización

df_precios = df_precios.rename(
    columns={'Precio promedio por kilogramo*': "Precio_kg" }
    )


# Armonizo los datos 

cols = ['Grupo', 'Producto', 'Mercado']

df_precios[cols] = df_precios[cols].apply(
    lambda x: x.str.strip().str.lower()
) 

# Identifico tipos de datos y corrijo

df_precios.dtypes

df_precios['Fecha'] = pd.to_datetime(df_precios['Fecha'],
                                     errors='coerce')
df_precios.dtypes

# Confirmo consistencia de la base de datos

df_precios.shape
df_precios.info()

# Confirmo si estan todos los años

df_precios['anio'].value_counts().sort_index()

# Verifico cuantos productos y mercados hay
df_precios['Producto'].nunique()
df_precios['Mercado'].nunique()

# Verifico extremos en precio

df_precios['Precio_kg'].describe()

# Extraigo el municipio de la columna mercado y normalizo

df_precios['municipio'] = (
    df_precios['Mercado']
    .str
    .split(',')
    .str[0]
    )

df_precios['municipio'] = (
    df_precios['municipio']
    .str.replace(r'\(.*?\)', '', regex=True)
    .str.strip()
    .str.lower()
    )

df_precios['municipio'].value_counts().head(20)


# Exporto

df_precios.to_csv('precios_2021_2025.csv', index=False)
