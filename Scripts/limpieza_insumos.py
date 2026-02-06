# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 14:54:37 2026

@author: nikol
"""

import pandas as pd

insumos_2021_2025 = pd.read_excel('anex-SIPSAInsumos-SeriesHistoricasMun-2021-2025.xlsx',
                                  sheet_name=None)

# Consulto hojas para saber cuales no son útiles
insumos_2021_2025.keys()

# Elimino esas hojas

hojas_no_utiles = [
    'Índice',
    'Metodología',
    'Listado',
    'ESRI_MAPINFO_SHEET'
    ]

insumo_utiles = {
    nombre: df
    for nombre, df in insumos_2021_2025.items()
    if nombre not in hojas_no_utiles
    }

insumo_utiles.keys()

# Limpio la primera hoja 

df_prueba = list(insumo_utiles.values())[0]
df_prueba.head(12)

# Extraigo el tipo de insumo 
tipo_insumo = df_prueba.iloc[3, 0]

# Limpio filas superiroes 
df_prueba = df_prueba.iloc[7:]

# Nombramos las columnas con la primera fila
df_prueba.columns = df_prueba.iloc[0]

# Elimino la primera fila repetida con los nombres de las columas y resteo index
df_prueba = df_prueba.iloc[1:].reset_index(drop=True)

df_prueba.head(10)

# Elimino últimas filas basura

ultimo_dato = df_prueba['Mes'].last_valid_index()

df_prueba = df_prueba.loc[:ultimo_dato]

df_prueba.tail()

# Elimino ultima columna vacía

df_prueba = df_prueba.dropna(axis=1, how='all')

df_prueba.columns

df_prueba.isnull().sum()

# Normalizo nombres de columnas

df_prueba.columns = df_prueba.columns.str.strip()

df_prueba.columns

# Convierto mes a número

mapa_meses = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
    'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
    'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }

df_prueba['Mes'] = df_prueba['Mes'].map(mapa_meses)

df_prueba['Mes'].unique()

# Verfico tipo de datos

df_prueba.dtypes

df_prueba['Año'] = pd.to_numeric(df_prueba['Año'], errors='coerce')
df_prueba['Precio promedio'] = pd.to_numeric(df_prueba['Precio promedio'],
                                             errors='coerce')

df_prueba.dtypes

# Normalizamos texto en columnas

columnas_texto = ['Nombre departamento', 'Nombre municipio',
                  'Nombre del producto', 'Presentación del producto']

for col in columnas_texto:
    df_prueba[col] = (
        df_prueba[col]
        .str.strip()
        .str.lower()
        .str.replace('  ', ' ')
        )
 
### Funcion final de limpieza ###

def limpiar_insumos(df):
    df = df.copy()
    
    # Extraer tipo de insumo
    
    tipo_insumo = df.iloc[3, 0]
    
    # Eliminar filas superiores basura
    
    df = df.iloc[7:]
    
    # Nombrar columnas usando la primera fila
    
    df.columns = df.iloc[0]
    
    # Eliminar la fila de encabezados y resetear el índice
    
    df = df.iloc[1:].reset_index(drop=True)
    
    # Corte de filas basura finales 
    
    ultimo_dato = df['Mes'].last_valid_index()
    df = df.loc[:ultimo_dato]
    
    # Eliminar columnas vacías
    
    df = df.dropna(axis=1, how='all')
    
    # Normalizar nombres de columnas
    
    df.columns = df.columns.str.strip()
    
    # Convertir mes a número
    
    mapa_meses = {
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
        'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
        'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
    
    df['Mes'] = df['Mes'].map(mapa_meses)
    
    # Convertir columnas numéricas
    
    df['Año'] = pd.to_numeric(df['Año'], errors='coerce')
    df['Precio promedio'] = pd.to_numeric(df['Precio promedio'], errors='coerce')
    
    # Normalizar texto 
    
    columnas_texto = [
        'Nombre departamento',
        'Nombre municipio',
        'Nombre del producto',
        'Presentación del producto'
        ]
    
    for col in columnas_texto:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r'\s+', ' ', regex=True)
            )
    
    # Agregar tipo de insumo
    
    df['tipo_insumo'] = tipo_insumo
    
    return df


### Aplico la función a las hojas útiles ###

insumos_limpios = {}

for nombre, df in insumo_utiles.items():
    try:
        df_limpio = limpiar_insumos(df)
        insumos_limpios[nombre] = df_limpio
    except Exception as e:
        print(f'Hoja omitida: {nombre}')
        
### Concateno ###

df_insumos = pd.concat(
    insumos_limpios.values(), 
    ignore_index=True
    )

# Extraigo codigo y tipo de insumo

df_insumos[['codigo_insumo', 'tipo_insumo']] = (
    df_insumos['tipo_insumo']
    .str.extract(r'^(\d+(?:\.\d+)?)\s*(.*)')
    )

df_insumos.head(5)

# Limpiamos columnas nuevas codigo y tipo de insumo

df_insumos['tipo_insumo'] = (
    df_insumos['tipo_insumo']
    .str.strip()
    .str.lstrip('.')
    .str.strip()
    )

# Verifico 

df_insumos.head(5)
df_insumos['tipo_insumo'].value_counts().head(10)
df_insumos['codigo_insumo'].value_counts().sort_index()

df_insumos.tail()
df_insumos.info()
df_insumos.isnull().sum()

# Creo la columna Fecha 

df_insumos.columns

df_insumos['fecha'] = pd.to_datetime(
    dict(year=df_insumos['Año'], month=df_insumos['Mes'], day=1)
    )

df_insumos[['Año', 'Mes', 'fecha']].head()
df_insumos['fecha'].min(), df_insumos['fecha'].max()

# # Filtro para quitar tipos de insumos que no son utiles 

excluir = [
    'alimentos', 'suplementos', 'vitaminas', 'sales', 'minerales',
    'medicamentos', 'hormonales', 'antibióticos', 'antibioticos',
    'antiparasitarios', 'antisépticos', 'antisepticos', 'higiene'
    ]

permitir_agricola = [
    'insecticidas', 'acaricidas', 'nematicidas',
    'molusquicidas', 'reguladores', 'plaguicidas'
    ]
 
def filtrar_insumos(df_insumos):
    tipo = df_insumos['tipo_insumo']
    
    # Marco lo que debe excluirse
    mask_excluir = tipo.str.contains('|'.join(excluir), 
                                     case=False, na=False)
    
    # Marco lo que es agrícola
    mask_agricola = tipo.str.contains('|'.join(permitir_agricola),
                                      case=False, na=False)
    
    # Excluyo solo si es excluible y no agrícola
    df_filtrado = df_insumos[~(mask_excluir & ~mask_agricola)]
    
    return df_filtrado
    
# Aplico la función a df_insumos 

df_insumos_filtrados = filtrar_insumos(df_insumos)

# Verifico

df_insumos['tipo_insumo'].value_counts()
df_insumos_filtrados['tipo_insumo'].value_counts()

# Defino nivel de analisis Departamento - Mensual

insumos_dpto_mensual = (
    df_insumos_filtrados
    .groupby(
        ['Nombre departamento', 'fecha', 'tipo_insumo'],
        as_index=False
        )['Precio promedio']
    .mean()
    )

# Exporto 

df_insumos_filtrados.to_csv('insumos_filtrados.csv', index=False)
insumos_dpto_mensual.to_csv('insumos_dpto_mensual.csv', index=False)


    


