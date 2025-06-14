#INDICE CONFORT AMBIENTAL
import dash
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import os
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import requests
import json
import numpy as np
from dash import ctx
import requests
import unicodedata
import re



# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ICAM PARQUES BOGOTÁ"
app.config.suppress_callback_exceptions = True  # Permitir callbacks dinámicos

# Nombre del archivo Excel
archivo_excel = 'matriz_general_de_indicadores'

# Definir las hojas que queremos cargar
sheets_to_load = ['ICA-BD', 'IRA-BD', 'ICT-BD', 'ICAM-BD', 'DE_ICA', 'DE_ICT', 'DE_IRA', 'DE_ICAM']


# 📌 Ruta del archivo Excel
file_path = r"matriz_general_de_indicadores"

# 🔹 Cargar datos de cada hoja
try:
    df_ira = pd.read_excel(file_path, sheet_name="TAB_EST_IRA")
    df_ict = pd.read_excel(file_path, sheet_name="TAB_EST_ICT")
    df_ica = pd.read_excel(file_path, sheet_name="TAB_EST_ICA")
except Exception as e:
    print(f"Error cargando hojas: {e}")
    df_ira, df_ict, df_ica = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


# Cargar los datos desde el archivo Excel (todas las hojas)
data_dict = pd.read_excel(archivo_excel, sheet_name=sheets_to_load, engine='openpyxl')

# -------------------------------
# Datos de Ruido Ambiental (ICA)
# -------------------------------
data_ica = data_dict['ICA-BD'].rename(columns={
    'Nombre del parque': 'parque',
    'Nombre Localidad': 'localidad',
    'PM2.5': 'pm25',
    'Valor ICA(PM2.5)': 'ica_pm25',
    'Estado calidad del aire(PM2.5)': 'estado_pm25',
    'PM10': 'pm10',
    'Valor ICA(PM10)': 'ica_pm10',
    'Estado calidad del aire(PM10)': 'estado_pm10',
    'Indice de Calidad del aire (ICA)': 'ica_general',
    'Estado Calidad del Aire General': 'Estado',
    'latitud': 'lat',
    'longitud': 'lon'
})

# -------------------------------
# D1_DIAGNÓSTICO CALIDAD DEL AIRE (ICA)
# -------------------------------
data_de_ica = data_dict['DE_ICA'].copy()
# Renombrar columnas correctamente
data_de_ica = data_de_ica.rename(columns={
    'rango ica': 'rango_ica',  # Asegurar que coincida con el nombre en minúsculas
    'Diagnostico ICA': 'diagnostico_ica',  # Renombrar Diagnóstico ICA a diagnostico_ica
    'Numero estrategia ICA': 'numero_estrategia_ica',  # Renombrar Número estrategia
})

# -------------------------------
# Datos de Ruido Ambiental (IRA)
# -------------------------------
data_ira = data_dict['IRA-BD'].rename(columns={
    
    'Nombre del parque': 'parque',
    'Indice de Ruido ambiental (IRA)': 'ira',
    'Decibelios por parque': 'decibelios',
    'Nivel Ruido Ambiental': 'nivel_ruido'
})

# -------------------------------
# Datos de Confort Termico (ICT)
# -----------------------------

data_ict = data_dict['ICT-BD'].rename(columns={
    'Nombre del parque': 'parque',
    'Nombre Localidad': 'localidad',
    'Temperatura Superficial promedio (C°)': 'temperatura',
    'Humedad Promedio (%)': 'humedad',
    'Velocidad del viento promedio (m-s)': 'velocidad_viento',
    'Indice de Confort Termico(ICT)': 'ict',
    'Sensación Termica': 'sensasion_termica',
    'latitud': 'lat',
    'longitud': 'lon'  
})



# -------------------------------
# D2_DIAGNÓSTICO CONFORT TÉRMICO (ICT)
# -------------------------------
data_de_ict = data_dict['DE_ICT'].copy()

# Renombrar columnas correctamente
data_de_ict = data_de_ict.rename(columns={
    'rango_ict': 'rango_ict',  # Asegurar que el nombre sea consistente
    'diagnostico_ict': 'diagnostico_ict',  # Asegurar el nombre correcto
    'Numero estrategia ICT': 'numero_estrategia_ict',  # Renombrar Número estrategia
})


# -------------------------------
# D2_DIAGNÓSTICO ÍNDICE DE RUIDO AMBIENTAL (IRA)
# -------------------------------
data_de_ira = data_dict['DE_IRA'].copy()

# Renombrar columnas correctamente
data_de_ira = data_de_ira.rename(columns={
    "rango_ira": "rango_ira",
    "caracterizacion": "caracterizacion",
    "diagnostico_ira": "diagnostico_ira",
    "numero_estrategia_ira": "numero_estrategia_ira",
    "nombre_estrategia_ira": "nombre_estrategia_ira",
    "descripcion_estrategia_ira": "descripcion_estrategia_ira"
})

print("Columnas en data_de_ira después del renombrado:", data_de_ira.columns)
# Verificar que los datos se han cargado correctamente
print(data_de_ira.head())



# Filtrar estrategias únicas
estrategias_unicas = data_de_ira["numero_estrategia_ira"].dropna().unique()


# -------------------------------
# Datos de Confort Ambiental (ICAM)
# ----------------------------------

data_icam = data_dict['ICAM-BD'].rename(columns={
    'Nombre del parque': 'parque',
    'Nombre Localidad': 'localidad', 
    'Nombre del parque': 'parque',
    'Indice de Confort Ambiental(ICAM)': 'icam',  
    'Comfort Ambiental del parque(ICAM)': 'comfort-ambiental', 
    'Nota Confort Ambiental(ICT)': 'nota-icam-ict',
    'Caracterización(ICT)': 'caracterizacion-ict',
    'Nota Confort Ambiental(ICA)': 'nota-icam-ica',
    'Caracterización(ICA)': 'caracterizacion-ica',
    'Nota Confort Ambiental(IRA)': 'nota-icam-ira',
    'Caracterización(IRA)': 'caracterizacion-ira',
    'latitud': 'lat',
    'longitud': 'lon'  
})


# -------------------------------
# DIAGNÓSTICO CONFORT AMBIENTAL (ICAM)
# ----------------------------------

data_de_icam = data_dict['DE_ICAM'].rename(columns={
    "rango_icam": "rango_icam",
    "caracterizacion": "caracterizacion",
    "diagnostico_icam": "diagnostico_icam",
})

# Renombrar columnas correctamente
data_de_ira = data_de_ira.rename(columns={
    "rango_ira": "rango_ira",
    "caracterizacion": "caracterizacion",
    "diagnostico_ira": "diagnostico_ira",
    "numero_estrategia_ira": "numero_estrategia_ira",
    "nombre_estrategia_ira": "nombre_estrategia_ira",
    "descripcion_estrategia_ira": "descripcion_estrategia_ira"
})

# Si necesitas fusionar todas las hojas en un solo DataFrame
data_combined = pd.concat([df.assign(Hoja=sheet) for sheet, df in data_dict.items()], ignore_index=True)


# Calcular el valor promedio del ICA general
valor_promedio_icam = data_icam['icam'].mean()

# Función para obtener el estado y color según el valor ICA
def obtener_estado_color(icam):
    for rango, (estado, color) in rango_colores.items():
        if rango[0] <= icam < rango[1]:
            return estado, color
    return "Desconocido", "black"

# Función para obtener la categoría de confort ambiental basada en el valor ICAM
def obtener_diagnostico(icam):
    if 80 <= icam <= 100:
        return "Óptimo: Excelente confort ambiental."
    elif 60 <= icam < 80:
        return "Bueno: Buen confort ambiental con mínimas molestias."
    elif 40 <= icam < 60:
        return "Moderado: Confort aceptable, pero podría haber algunas molestias."
    elif 20 <= icam < 40:
        return "Bajo: Confort ambiental bajo, pueden presentarse molestias significativas."
    elif 0 <= icam < 20:
        return "Malo: Confort ambiental muy bajo, condiciones desfavorables."
    else:
        return "Valor ICAM fuera de rango. Debe estar entre 0 y 100."

# -------------------------------
# Categorización de rangos ICAM
# -------------------------------
def clasificar_icam(valor):
    if 80 <= valor <= 100:
        return "Óptimo"
    elif 60 <= valor < 80:
        return "Bueno"
    elif 40 <= valor < 60:
        return "Moderado"
    elif 20 <= valor < 40:
        return "Bajo"
    elif 0 <= valor < 20:
        return "Malo"
    else:
        return "Valor fuera de rango"

# Aplicar clasificación directamente al DataFrame
data_icam["confort_ambiental"] = data_icam["icam"].apply(clasificar_icam)

# -------------------------------
# Definir Colores para ICAM
# -------------------------------
color_icam = {
    "Óptimo": "darkgreen",
    "Bueno": "lightgreen",
    "Moderado": "khaki",
    "Bajo": "orange",
    "Malo": "orangered"
}

# Generar el diagnóstico para todos los parques
diagnostico_general = obtener_diagnostico(valor_promedio_icam)

# Calcular el valor promedio de la calidad del aire
valor_promedio = data_icam['icam'].mean()

# -------------------------------
# Definir colores para los rangos del ICAM
# -------------------------------
rango_colores = {
    (0, 19): ("Malo", "orangered"),
    (20, 39): ("Bajo", "orange"),
    (40, 59): ("Moderado", "khaki"),
    (60, 79): ("Bueno", "lightgreen"),
    (80, 100): ("Óptimo", "darkgreen"),
}

# Función para asignar el color y etiqueta basado en el valor
def obtener_color(valor):
    for rango, (etiqueta, color) in rango_colores.items():
        if rango[0] <= valor <= rango[1]:
            return color, etiqueta
    return "gray", "Desconocido"

# Obtener el color y etiqueta para el valor promedio
color, etiqueta = obtener_color(valor_promedio)


barra_estatica = html.Div(
    style={
        'width': '15vw', 
        'height': '3.5vh', 
        'background-color': 'rgba(206, 204, 204, 0.7)', 
        'border-radius': '5px',
        'zIndex': '1000'
    },
    children=[ 
        html.Div(
            style={
                'width': f'{max(min(valor_promedio, 100), 0)}%',
                'height': '100%',
                'background-color': color,
                'border-radius': '5px',
            }
        ),
    ]
)

# 🔹 Cantidad de Parques por estado de Calidad del Aire

grafico_confort = px.bar(
    data_icam.groupby('confort_ambiental').size().reset_index(name='cantidad_parques'),
    x='confort_ambiental', y='cantidad_parques',
    title='Cantidad de parques por confort ambiental',
    text='cantidad_parques',
    color='confort_ambiental',
    color_discrete_map={etiqueta: color for _, (etiqueta, color) in rango_colores.items()}
)

# 🔹 Modificar fuente y tamaño de texto en el gráfico
grafico_confort.update_layout(
    font=dict(
        family="Franklin Gothic Condensed, sans-serif",  # 🔹 Cambia la fuente general
        size=11,  # 🔹 Cambia el tamaño del texto
        color="black"  # 🔹 Cambia el color del texto
    ),
    title=dict(
        text="<b>Cantidad de parques vecinales por confort ambiental</b>",  # 🔹 Texto en negrita
        font=dict(size=13, family="Franklin Gothic Condensed, sans-serif", color="black"),  # 🔹 Fuente personalizada
        x=0.01,  # 🔹 Desplaza el título hacia la izquierda (0 = extremo izquierdo, 0.5 = centrado, 1 = extremo derecho)
        xanchor="left"  # 🔹 Asegura que el anclaje del texto esté alineado a la izquierda
    ),
    xaxis=dict(
        title="Confort Ambiental",
        titlefont=dict(family="Franklin Gothic Condensed, sans-serif", size=11, color="black"),  # Fuente del eje X
        tickfont=dict(family="Franklin Gothic Condensed, sans-serif", size=11, color="black")  # Fuente de valores en el eje X
    ),
    yaxis=dict(
        range=[0, 4000],  # 🔹 Limita la altura máxima de las barras
        title="Cantidad de Parques",
        titlefont=dict(family="Franklin Gothic Condensed, sans-serif", size=11, color="black"),  # Fuente del eje Y
        gridcolor="grey",  # 🔹 Cambia el color de las líneas horizontales del eje X
        tickfont=dict(family="Franklin Gothic Condensed, sans-serif", size=11, color="black")  # Fuente de valores en el eje Y
    ),
    height=200,  # 🔹 Ajusta la altura del gráfico
    margin=dict(l=10, r=10, t=40, b=10),  # 🔹 Reduce los márgenes: l=left, r=right, t=top, b=bottom
    bargap=0.2,  # 🔹 Espacio entre barras (0 = sin espacio, 1 = máximo espacio)
    bargroupgap=0.2,  # 🔹 Espacio entre grupos de barras (si hay agrupación)
    paper_bgcolor='#f5f5f5',  
    plot_bgcolor='#f5f5f5'
)

# 🔹 Modificar texto dentro de las barras
grafico_confort.update_traces(
    textfont=dict(family="Franklin Gothic Condensed, sans-serif", size=12, color="black"),  # Fuente de los valores dentro de las barras
    textposition="outside"  # Ubica los valores fuera de las barras
)
#--------------------------------------------------------------------------------------------#

grafico_localidades = px.bar(
    data_icam.groupby(['localidad', 'confort_ambiental']).size().reset_index(name='cantidad_parques'),
    x='localidad', y='cantidad_parques',
    color='confort_ambiental',
    title='Cantidad de Parques por localidad y sensasión térmica',
    text='cantidad_parques',
    color_discrete_map={etiqueta: color for _, (etiqueta, color) in rango_colores.items()},
    barmode='stack'
)

# 🔹 Modificar fuente, márgenes y espaciado de las barras
grafico_localidades.update_layout(
    font=dict(
        family="Franklin Gothic Condensed, sans-serif",  # 🔹 Fuente general
        size=12,  
        color="black"
    ),
    title=dict(
        text="<b>Cantidad de Parques por localidad y confort ambiental</b>",  # 🔹 Negrita
        font=dict(size=13, family="Franklin Gothic Condensed, sans-serif", color="black"),  # 🔹 Fuente personalizada
        x=0.01,  # 🔹 Desplaza el título hacia la izquierda
        xanchor="left"  # 🔹 Anclaje alineado a la izquierda
    ),
    xaxis=dict(
        title="Localidad",
        titlefont=dict(family="Franklin Gothic Condensed, sans-serif", size=12, color="black"),  
        tickfont=dict(family="Franklin Gothic Condensed, sans-serif", size=12, color="black"),  
        tickangle=-45  # 🔹 Inclina etiquetas para mejor legibilidad
    ),
    yaxis=dict(
        range=[0, 850],  # 🔹 Limita la altura máxima de las barras
        title="Cantidad de Parques",
        titlefont=dict(family="Franklin Gothic Condensed, sans-serif", size=12, color="black"),  
        gridcolor="grey",  # 🔹 Cambia el color de las líneas horizontales del eje X
        tickfont=dict(family="Franklin Gothic Condensed, sans-serif", size=12, color="black")  
    ),
    height=200,  # 🔹 Ajusta la altura del gráfico
    margin=dict(l=10, r=10, t=40, b=10),  # 🔹 Reduce los márgenes: l=left, r=right, t=top, b=bottom
    bargap=0.2,  # 🔹 Espacio entre barras (0 = sin espacio, 1 = máximo espacio)
    bargroupgap=0.2,  # 🔹 Espacio entre grupos de barras (si hay agrupación)
    paper_bgcolor='#f5f5f5',  
    plot_bgcolor='#f5f5f5'
)

# 🔹 Función para limpiar nombres
def limpiar_nombre(nombre):
    """Normaliza el nombre quitando tildes, mayúsculas y símbolos raros"""
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
    nombre = re.sub(r'[^a-zA-Z0-9 ]', '', nombre)  # Elimina guiones, comas, etc.
    return nombre.lower().strip()

# 🔹 Obtener datos de la API
url_api = "https://bogota-laburbano.opendatasoft.com/api/explore/v2.1/catalog/datasets/poligonos-localidades/records?limit=20"
response = requests.get(url_api)

if response.status_code == 200:
    data_localidades = response.json().get("results", [])
else:
    raise Exception("Error al obtener los datos de la API")

# 🔹 Transformar datos a formato GeoJSON
geojson_localidades = {
    "type": "FeatureCollection",
    "features": []
}

for localidad in data_localidades:
    if "geometry" in localidad and "geometry" in localidad["geometry"]:
        feature = {
            "type": "Feature",
            "geometry": localidad["geometry"]["geometry"],
            "properties": {
                "ID": str(localidad["Identificador unico de la localidad"]),
                "Nombre": localidad["Nombre de la localidad"],
                "Nombre_normalizado": limpiar_nombre(localidad["Nombre de la localidad"])
            }
        }
        geojson_localidades["features"].append(feature)



# 🔹 Modificar texto dentro de las barras
grafico_localidades.update_traces(
    textfont=dict(family="Franklin Gothic Condensed, sans-serif", size=12, color="black"),  # 🔹 Fuente de los valores dentro de las barras
    textposition="outside"  # 🔹 Ubica los valores fuera de las barras
)


# 🔹 Función para limpiar nombres
def limpiar_nombre(nombre):
    """Normaliza el nombre quitando tildes, mayúsculas y símbolos raros"""
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
    nombre = re.sub(r'[^a-zA-Z0-9 ]', '', nombre)  # Elimina guiones, comas, etc.
    return nombre.lower().strip()

# 🔹 Obtener datos de la API
url_api = "https://bogota-laburbano.opendatasoft.com/api/explore/v2.1/catalog/datasets/poligonos-localidades/records?limit=20"
response = requests.get(url_api)

if response.status_code == 200:
    data_localidades = response.json().get("results", [])
else:
    raise Exception("Error al obtener los datos de la API")

# 🔹 Transformar datos a formato GeoJSON
geojson_localidades = {
    "type": "FeatureCollection",
    "features": []
}

for localidad in data_localidades:
    if "geometry" in localidad and "geometry" in localidad["geometry"]:
        feature = {
            "type": "Feature",
            "geometry": localidad["geometry"]["geometry"],
            "properties": {
                "ID": str(localidad["Identificador unico de la localidad"]),
                "Nombre": localidad["Nombre de la localidad"],
                "Nombre_normalizado": limpiar_nombre(localidad["Nombre de la localidad"])
            }
        }
        geojson_localidades["features"].append(feature)

# 🔹 MAPA BASE  
fig_mapa = px.scatter_mapbox(
    data_icam, lat="lat", lon="lon", hover_name="parque",
    color="confort_ambiental", zoom=11,
    mapbox_style="carto-positron",
    color_discrete_map={etiqueta: color for _, (etiqueta, color) in rango_colores.items()},
    hover_data={"confort_ambiental": True, "localidad": True}  
)

fig_mapa.update_layout(
    mapbox=dict(
        center={"lat": 4.65, "lon": -74.1},
        zoom=10,
        style="carto-positron"
    ),
    uirevision="mapa-fijo",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    autosize=True  # ✅ permite que se adapte al contenedor
)

# 🔹 Capa de localidades (sin interactividad)
choropleth = px.choropleth_mapbox(
    geojson=geojson_localidades,
    locations=[f["properties"]["ID"] for f in geojson_localidades["features"]],
    featureidkey="properties.ID",
    color=[1] * len(geojson_localidades["features"]),
    color_continuous_scale="Viridis",
    range_color=(0, 1),
    opacity=0.1  # Ajustar opacidad para que los puntos se vean mejor
).data[0]

# 🔹 Aumentar grosor de líneas de contorno
choropleth.update(
    hoverinfo="skip",  # Evita que se muestre información al pasar el mouse
    hovertemplate=None,  # Evita que aparezca la caja de información
    showscale=False,  # Oculta la barra de colores
    coloraxis=None,  # Desvincula la capa de cualquier escala de color
    marker_line_width=2,  # 🔹 Aumenta el grosor de las líneas de contorno
    marker_line_color="black"  # 🔹 Color del contorno (puedes cambiarlo)
)

# 🔹 Agregar la capa de polígonos al mapa
fig_mapa.add_trace(choropleth)

# 🔹 Filtrar solo las localidades que tienen coordenadas
coords_localidades = [
    localidad["geo_point_2d"] for localidad in data_localidades if "geo_point_2d" in localidad
]
nombres_localidades = [
    localidad["Nombre de la localidad"] for localidad in data_localidades if "geo_point_2d" in localidad
]

# 🔹 Verificar que hay coordenadas disponibles
if not coords_localidades:
    raise ValueError("No se encontraron coordenadas para las localidades.")

# Mover la leyenda abajo y hacerla horizontal
fig_mapa.update_layout(
    legend=dict(
        orientation="h",  # Leyenda en formato horizontal
        yanchor="bottom",  # Anclar en la parte inferior
        y=0.01,  # Un poco arriba del borde
        xanchor="center",  # Centrar horizontalmente
        x=0.5  # Centrar en la parte inferior
    )
)

# Aumentar el tamaño de los puntos (solo para scatter_mapbox)
fig_mapa.update_traces(marker=dict(size=12), selector=dict(type="scattermapbox"))  

fig_mapa.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    autosize=True  # 🔹 Asegúrate de que esté activado
)

# Calcular las localidades con la mejor y peor calidad del aire
localidades_promedio = data_icam.groupby('localidad')['icam'].mean().reset_index()
mejor_localidad = localidades_promedio.loc[localidades_promedio['icam'].idxmax()]
peor_localidad = localidades_promedio.loc[localidades_promedio['icam'].idxmin()]


#LAYOUT DEL MAPA

app.layout = html.Div(

    style={
        'backgroundColor': '#F5F5F5',
        'width': '100vw',
        'height': '100vh',
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',
        'gridTemplateRows': 'auto auto auto auto',
        'gridTemplateAreas': """
            'titulo titulo'
            'mapa  mapa'
            'grafico1 grafico2'
            'info info'
        """,
        'justifyItems': 'center',
    },
    children=[
        # 🔹 Contenedor del mapa (ubicado en 'mapa' del grid)
        html.Div(
            style={
                "gridArea": "mapa",         # ✅ Asegura que se ubique en el área 'mapa' del grid
                "width": "38vw",
                "height": "calc(100vh - 5vh)",  # ✅ Usa altura relativa consistente
                "position": "fixed",
                "top": "5vh",
                "left": "35.5vw",
            },
            children=[
                dcc.Graph(
                    id="mapa",
                    figure=fig_mapa,
                    config={"scrollZoom": True},
                    style={
                        "width": "100%",
                        "height": "100%",  # ✅ Se adapta al contenedor
                    }
                )
            ]
        ),

        dcc.Location(id="url", refresh=True),  # Necesario para la redirección

        # 🔹 DROPDOWN DE FILTROS POR INDICADORES
        html.Div(
            id="contenedor-dropdown",
            style={
                'position': 'fixed',
                'top': '1vh',
                'left': '35.5vw',
                'width': '38vw',
                'backgroundColor': '#BEBEBE',
                'padding': '0.5vh',
                'zIndex': '1000',
                'borderRadius': '1vh'
            },
            children=[
                dcc.Markdown(
                    "**FILTRO POR INDICADOR**",
                    style={
                        'fontSize': '0.7vw',
                        'fontFamily': 'Arial, sans-serif',
                        'textAlign': 'center',
                        'color': '#333',
                        'marginBottom': '0.5vh'
                    }
                ),
                dcc.Dropdown(
                    id='selector-indicador',
                    options=[
                        {'label': 'Índice de Ruido Ambiental (IRA)', 'value': 'IRA'},
                        {'label': 'Índice de Confort Térmico (ICT)', 'value': 'ICT'},
                        {'label': 'Índice de Calidad del Aire (ICA)', 'value': 'ICA'},
                        {'label': 'Índice de Confort Ambiental (ICAM)', 'value': 'ICAM'}
                    ],
                    value='ICAM',  # Valor inicial cuando estás en el ICT
                    clearable=False,
                    style={
                        'fontSize': '0.7vw',
                        'fontFamily': 'Arial, sans-serif',
                        'textAlign': 'left',
                        'width': '100%',
                        'borderRadius': '0.1vh',
                        'overflow': 'visible'
                    }
                )
            ]
        ),

        # 📌 Botones para abrir cada matriz
        html.Div([
            html.Div(
                style={
                    'position': 'fixed',
                    'top': '69vh',
                    'left': '91vw',  # Ajuste de posición
                    'zIndex': '1000',
                    'textAlign': 'center'
                },
                children=[
                    html.Button("Estrategias IRA", id="mostrar-matriz-ira", n_clicks=0,
                        style={ 
                            "fontSize": "0.65vw", "cursor": "pointer", "borderRadius": "0.5vw",
                            "backgroundColor": "#D3D3D3", 'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                            "color": "black", "width": "6vw", "height": "2vh"
                        }
                    )
                ]
            ),

            html.Div(
                style={
                    'position': 'fixed',
                    'top': '87vh',
                    'left': '91vw',  # Ajuste de posición
                    'zIndex': '1000',
                    'textAlign': 'center'
                },
                children=[
                    html.Button("  Ver Estrategias ICT  ", id="mostrar-matriz-ict", n_clicks=0,
                        style={ 
                            "fontSize": "0.70vw", "cursor": "pointer", "borderRadius": "0.5vw",
                            "backgroundColor": "#D3D3D3", 'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                            "color": "black", "width": "6vw", "height": "2vh"
                        }
                    )
                ]
            ),

            html.Div(
                style={
                    'position': 'fixed',
                    'top': '51vh',
                    'left': '91vw',  # Ajuste de posición
                    'zIndex': '1000',
                    'textAlign': 'center'
                },  
                children=[
                    html.Button("Estrategias ICA", id="mostrar-matriz-ica", n_clicks=0,
                        style={ 
                            "fontSize": "0.70vw", "cursor": "pointer", "borderRadius": "0.5vw",
                            "backgroundColor": "#D3D3D3", 'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                            "color": "black", "width": "6vw", "height": "2vh"
                        }
                    )
                ]
            ),
        ]),

        # 📌 Modales para cada tabla
        dbc.Modal(
            [dbc.ModalHeader(dbc.ModalTitle("Estrategias IRA"), close_button=True),
             dbc.ModalBody(html.Div(id="tabla-estrategias-ira")),
             dbc.ModalFooter(dbc.Button("Cerrar", id="cerrar-tabla-ira", className="ml-auto", color="secondary"))],
            id="modal-tabla-ira", is_open=False, centered=True, size="xl"
        ),

        dbc.Modal(
            [dbc.ModalHeader(dbc.ModalTitle("Estrategias ICT"), close_button=True),
             dbc.ModalBody(html.Div(id="tabla-estrategias-ict")),
             dbc.ModalFooter(dbc.Button("Cerrar", id="cerrar-tabla-ict", className="ml-auto", color="secondary"))],
            id="modal-tabla-ict", is_open=False, centered=True, size="xl"
        ),

        dbc.Modal(
            [dbc.ModalHeader(dbc.ModalTitle("Estrategias ICA"), close_button=True),
             dbc.ModalBody(html.Div(id="tabla-estrategias-ica")),
             dbc.ModalFooter(dbc.Button("Cerrar", id="cerrar-tabla-ica", className="ml-auto", color="secondary"))],
            id="modal-tabla-ica", is_open=False, centered=True, size="xl"
        ),


        dcc.Store(id="imagen-modal-mostrado", data=False, storage_type="session"),


        # 📌 BOTÓN DE FICHA EXPLICATIVA
        html.Div(
            style={
                'position': 'fixed',
                'top': '1vh',
                'left': '32vw',
                'transform': 'translateX(-50%)',
                'textAlign': 'top',
                'zIndex': '1000'
            },
            children=[
                html.Button(
                    "?",
                    id="mostrar-imagen-btn",
                    n_clicks=0,
                    style={
                        "fontSize": "1vw",
                        "padding": "0.1vh",
                        "cursor": "pointer",
                        "borderRadius": "8px",
                        "backgroundColor": "#000000",
                        "color": "white",
                        "border": "none",
                        'position': 'fixed',
                        "width": "3vw",
                        "height": "1.5vw"
                    }
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle("GUÍA INTRODUCTORIA"),
                            close_button=True
                        ),
                        dbc.ModalBody(
                            html.Img(
                                src="/assets/Indicador_calidad_del_Aire.jpg",
                                style={
                                    "maxWidth": "100%",
                                    "maxHeight": "90vh",
                                    "width": "auto",
                                    "height": "auto",
                                    "display": "block",
                                    "margin": "0 auto",
                                    "borderRadius": "8px",
                                    "objectFit": "contain"
                                }
                            )
                        ),
                        dbc.ModalFooter([
                            html.A(
                                dbc.Button(
                                    "Ficha técnica indicador ICAM",
                                    color="info",
                                    className="me-2"
                                ),
                                href="/assets/Indice_Confort_Ambiental_ICAM_Ficha_Indicador.pdf",
                                download="Indice_Confort_Ambiental_ICAM_Ficha_Indicador.pdf",
                                target="_blank"
                            ),

                            html.A(
                                dbc.Button(
                                    "Matriz general de indicadores(base de datos general)",
                                    color="info",
                                    className="me-2"
                                ),
                                href="/assets/matriz_general_de_indicadores",
                                download="matriz_general_de_indicadores",
                                target="_blank"
                            ),

                            html.A(
                                dbc.Button(
                                    "Video Explicativo Aplicativo",
                                    color="secondary"
                                ),
                                href="https://www.youtube.com/watch?v=WlT294GW5dU",
                                target="_blank"
                            )
                        ])
                    ],
                    id="imagen-modal",  
                    is_open=False,
                    centered=True,
                    style={
                        "maxWidth": "100vw",
                        "width": "100vw",
                        "maxHeight": "100vh",
                        "height": "100vh"
                    },
                    backdrop="static",
                    size="xl"
                )
            ]
        ),


        # 📊 Gráfico de cantidad de parques
        html.Div(
        style={
            'gridArea': 'grafico1',
            'width': '34vw',  # 🔹 Ancho relativo al tamaño de la pantalla
            'height': '20vh',  # 🔹 Altura relativa (ajusta según necesites)
            'marginTop': '0px',
            'alignSelf': 'center',
            'position': 'fixed',
            'left': '1vw',  # 🔹 Ajuste proporcional a la pantalla
            'top': '49.5vh'  # 🔹 Se mueve en proporción a la altura de la pantalla
        },
        children=[ 
            dcc.Graph(
                figure=grafico_confort.update_layout(
                height=400,  # 🔹 Se debe usar un número en píxeles
                paper_bgcolor='#f5f5f5',
                plot_bgcolor='#f5f5f5',
                margin=dict(l=10, r=10, t=40, b=10),
                ),
                style={"width": "100%", "height": "100%"}  # 🔹 Aquí sí se puede usar "100%"
                )
        ]
        ),

        # 📈 Gráfico de parques por localidad
        html.Div(
            style={
                'gridArea': 'grafico2',
                'width': '34vw',  # 🔹 Ancho relativo al tamaño de la pantalla
                'height': '35vh',  # 🔹 Altura proporcional
                'marginTop': '5vh',  # 🔹 Espacio proporcional arriba
                'alignSelf': 'center',
                'position': 'fixed',
                'left': '1vw',  # 🔹 Ajuste proporcional a la pantalla
                'top': '62vh'  # 🔹 Se mueve en función del alto de la pantalla
            },
            children=[
                dcc.Graph(
                figure=grafico_localidades.update_layout(
                height=400,  # 🔹 Se usa un valor numérico en píxeles (ajústalo según necesidad)
                paper_bgcolor='#f5f5f5',
                plot_bgcolor='#f5f5f5',
                margin=dict(l=10, r=10, t=40, b=10),
                ),
                style={"width": "100%", "height": "100%"}  # 🔹 Permite que el gráfico se adapte a su contenedor
                )
]
        ),


        # Barra de progreso
        html.Div(
            style={
            'width': '13vw',  # 🔹 Ancho relativo a la pantalla
            'position': 'fixed',  # 🔹 Se mantiene en la misma posición aunque hagas scroll
            'top': '8vh',  # 🔹 Altura relativa
            'left': '1vw',  # 🔹 Espacio desde la izquierda
            'margin': '0',
            'height': '6vh',  # 🔹 Define una altura fija en vh
            'minHeight': '6vh',  # 🔹 Evita que se haga más grande
            'maxHeight': '6vh',  # 🔹 Evita que se haga más pequeña  
            'zIndex': '1000'  # 🔹 Asegura que esté sobre otros elementos
            },
            children=[barra_estatica]
            ),

            html.Div(
                style={
                    'fontSize': '0.7vw',  # 🔹 Tamaño de fuente ajustado para mejor visibilidad
                    'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                    'textAlign': 'justify',
                    'width': '30vw',  # 🔹 Ancho más equilibrado para diferentes tamaños de pantalla
                    'position': 'fixed',  # 🔹 Se mantiene fijo en la pantalla aunque hagas scroll
                    'top': '6vh',  # 🔹 Ajusta la separación desde la parte superior
                    'left': '1vw',  # 🔹 Ajuste fino para mejor alineación
                    'zIndex': '1000',  # 🔹 Asegura que esté sobre otros elementos
                    'whiteSpace': 'nowrap',  # 🔹 Evita que el texto haga saltos de línea innecesarios
                    'overflow': 'hidden',  # 🔹 Evita desbordamientos
                },
                children=[
                    dcc.Markdown("**Barra Indicador Confort Ambiental (ICAM General)**")
                ]
            ),


  # 📌 Titulo General
        html.Div(
            style={
                'fontSize': '0.8vw',  # 🔹 Tamaño de fuente ajustado para adaptarse a la pantalla
                'fontFamily': 'Arial, sans-serif',  
                'textAlign': 'left',  # 🔹 Centra el texto para mejor presentación
                'width': '30.5vw',  # 🔹 Ancho proporcional a la pantalla
                'position': 'fixed',  # 🔹 Se mantiene en la misma posición aunque hagas scroll
                'top': '1vh',  # 🔹 Ajusta la separación desde la parte superior
                'left': '1vw',  # 🔹 Ajuste fino para mejor alineación
                'backgroundColor': '#000000',
                'color': '#FFFFFF',
                'padding': '0,5vh',  # 🔹 Espaciado interno relativo para evitar que el texto se pegue a los bordes
                'borderRadius': '1vh',  
                'maxHeight': '3vh',  
                'zIndex': '1000',  # 🔹 Asegura que esté sobre otros elementos
                'whiteSpace': 'nowrap',  # 🔹 Evita que el texto haga saltos de línea innecesarios
                'overflow': 'hidden'  # 🔹 Evita desbordamientos
            },
            children=[
                dcc.Markdown("**CONFORT AMBIENTAL EN PARQUES VECINALES DE BOGOTÁ**")
            ]
        ),

     # 📌 DIAGNÓSTICO INDIVIDUAL DEL PARQUE
        html.Div(
            style={
                'fontSize': '0.7vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'justify',
                'width': '55vw',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '1vh',  # Lo mueve hacia la parte superior
                'left': '74vw',  # Lo alinea a la izquierda
                'maxHeight': '4vh',  
            },
            children=[
                dcc.Markdown("**DIAGNÓSTICO INDIVIDUAL POR PARQUE**")
            ]
        ),

        # 📌 Información adicional del promedio
            html.Div(
            style={
                'textAlign': 'center',  
                'fontSize': '0.8vw',  # 🔹 Equivalente a 15px aprox.
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  
                'marginTop': '0.3vh',  # 🔹 Equivalente a 2px
                'backgroundColor': '#949191',  
                'padding': '0.4vh',  # 🔹 Equivalente a 2px de padding  
                'borderRadius': '1vh',  # 🔹 Equivalente a 8px
                'position': 'fixed',  # 🔹 Se mantiene fijo aunque hagas scroll
                'width': '18vw',  # 🔹 Equivalente a 18% del ancho de la pantalla
                'left': '16.5vw',  # 🔹 Equivalente a 390px en relación con el ancho
                'top': '8vh',  # 🔹 Equivalente a 80px en relación con la altura  
                'zIndex': '1000',  # 🔹 Asegura que esté sobre otros elementos
                'maxHeight': '4vh',  
                'whiteSpace': 'nowrap',  # 🔹 Evita saltos de línea innecesarios
                'overflow': 'hidden'  # 🔹 Previene desbordamientos
            },
            children=[
                html.Span("Promedio de Confort Ambiental(ICAM): ", style={'color': 'black'}),  
                html.Span(f"{valor_promedio:.2f}", style={'color': color, 'fontSize': '0.8vw'}),  
                html.Span(f" - {etiqueta}", style={'color': color, 'fontSize': '0.8vw'})  
            ], 
        ),

        # 📌 RANGOS CALIDAD DEL AIRE (TÍTULO)
                html.Div(
                style={
                    'fontSize': '0.7vw',  # 🔹 Equivalente a 14px aprox.
                    'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                    'textAlign': 'justify',
                    'width': '35vw',  # 🔹 Equivalente a 35% del ancho de la pantalla
                    'position': 'fixed',  # 🔹 Se mantiene en su lugar aunque hagas scroll
                    'top': '12.5vh',  # 🔹 Equivalente a 115px en relación con la altura
                    'left': '1vw',  # 🔹 Equivalente a 10px en relación con el ancho
                    'zIndex': '1000',  # 🔹 Asegura que esté sobre otros elementos
                },
                children=[
                    dcc.Markdown("**Rangos de Confort Ambiental**")
                ]
            ),

                html.Div(
                style={
                    'backgroundColor': '#D3D3D3',
                    'color': 'white',
                    'fontSize': '0.55vw',
                    'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                    'borderRadius': '1vw',
                    'marginTop': '0.5vh',
                    'textAlign': 'left',
                    'width': '34vw',
                    'position': 'fixed',
                    'top': '14vh',
                    'left': '1vw',
                    'padding': '1vh',  # 🔹 Agrega un poco de espacio interno
                    'maxHeight': '4vh',  
                    'overflow': 'hidden',  
                    'whiteSpace': 'nowrap'  
                },
                children=[
                    html.P([
                        html.Span("Malo (0-19) ", style={'color': 'black', 'fontWeight': 'normal'}), html.Span("| "), 
                        html.Span("Bajo (20-39) ", style={'color': 'black', 'fontWeight': 'normal'}), html.Span("| "), 
                        html.Span("Moderado (40-59) ", style={'color': 'black', 'fontWeight': 'normal'}), html.Span("| "), 
                        html.Span("Bueno (60-79) ", style={'color': 'black', 'fontWeight': 'normal'}), html.Span("| "), 
                        html.Span("Óptimo (80-100)", style={'color': 'black', 'fontWeight': 'normal'})
                    ])
                ]
),



     # 📌 TITULO DIAGNÓSTICO ICAM
        html.Div(
            style={
                'fontSize': '0.70vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'left',
                'width': '25%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '31vh',  # Lo mueve hacia la parte superior
                'left': '74vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**🏡Diagnóstico Confort Ambiental (ICAM) (Parque Vecinal)**")
            ]
        ),

        # 📌 CRÉDITOS
                html.Div(
                    style={
                        'fontSize': '0.70vw',
                        'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                        'textAlign': 'left',
                        'width': '25%',
                        'position': 'fixed',  # Posiciona el elemento de manera absoluta
                        'top': '97vh',  # Lo mueve hacia la parte superior
                        'left': '74vw',  # Lo alinea a la izquierda
                    },
                    children=[
                        dcc.Markdown("**Desarrollado por: Cristian Camilo Melan Sanchez - cristian.melan@estudiantes.uamerica.edu.co**")
                    ]
                ),



# 📌 TÍTULO DIAGNÓSTICO ICAM GENERAL 
        html.Div(
            style={
                'fontSize': '0.7vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'justify',
                'width': '31%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '20vh',  # Lo mueve hacia la parte superior
                'left': '1vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**Diagnóstico ICAM General**")
            ]
        ),

           # 📌 TITULO DIAGNÓSTICO IRA
        html.Div(
            style={
                'fontSize': '0.70vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'left',
                'width': '25%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '57.5vh',  # Lo mueve hacia la parte superior
                'left': '74vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**🔊Diagnóstico de Ruido Ambiental(IRA) (Parque Vecinal)**")
            ]
        ),

            # 📌 ESTRATEGIAS IRA PARQUES VECINAL
        html.Div(
            style={
                'fontSize': '0.70vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'left',
                'width': '8%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '57.5vh',  # Lo mueve hacia la parte superior
                'left': '91vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**🔊Estrategias de mejora (IRA)**")
            ]
        ),

    

    # 📌 TITULO DIAGNOSTICO ICT PARQUES
        html.Div(
            style={
                'fontSize': '0.70vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'left',
                'width': '25%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '76vh',  # Lo mueve hacia la parte superior
                'left': '74vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**🌡️Diagnóstico  Confort Térmico(ICT) (Parque Vecinal)**")
            ]
        ),

    
     # 📌 TITULO ESTRATEGIAS ICT PARQUES VECINAL
        html.Div(
            style={
                'fontSize': '0.70vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'left',
                'width': '25%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '76vh',  # Lo mueve hacia la parte superior
                'left': '91vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**🌡️Estrategias de mejora (ICT)**")
            ]
        ),


 # 📌 Titulo
    html.Div(
    style={
        'fontSize': '0.7vw',
        'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
        'textAlign': 'justify',
        'width': '35%',
        'position': 'fixed',  # Posiciona el elemento de manera absoluta
        'top': '20vh',  # Lo mueve hacia la parte superior
        'left': '16.5vw',  # Lo alinea a la izquierda
    },
    children=[
        dcc.Markdown("**Diagnóstico ICAM parques vecinales por localidad**")
    ]
),

    # 📌 Balance de las localidades por calidad del aire en parques vecinales
        html.Div(
            style={
                'fontSize': '0.7vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'justify',
                'width': '35%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '44vh',  # Lo mueve hacia la parte superior
                'left': '1vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**Balance de las localidades por Confort Ambiental en parques vecinales**")
            ]
        ),


 # 📌 Diagnóstico individual ICA - Titulo
        html.Div(
            style={
                'fontSize': '0.7vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'justify',
                'width': '35%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '40vh',  # Lo mueve hacia la parte superior
                'left': '74vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**🍃Diagnóstico de Calidad del Aire(ICA) (Parque vecinal)**")
            ]
        ),


    # 📌 TITULO ESTRATEGIAS ICA
        html.Div(
            style={
                'fontSize': '0.7vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'textAlign': 'justify',
                'width': '35%',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '40vh',  # Lo mueve hacia la parte superior
                'left': '91vw',  # Lo alinea a la izquierda
            },
            children=[
                dcc.Markdown("**🍃Estrategias de mejora(ICA)**")
            ]
        ),

    # 📌 SELECCIONADOR LOCALIDADES
        html.Div([
        dcc.Dropdown(
            id='dropdown-localidad',
            options=[{'label': loc, 'value': loc} for loc in data_icam['localidad'].dropna().unique()],
            value=data_icam['localidad'].dropna().unique()[0],  # Asegúrate de que no haya valores nulos en el valor inicial
            clearable=False,
            style={
                'backgroundColor': '#D3D3D3',
                'fontSize': '0.55vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                'padding': '0.1vw',
                'fontWeight': 'bold',
                'borderRadius': '0.5vw',
                'textAlign': 'top',
                'marginBottom': '0.1vh',
                'height': '3vh',
                'maxHeight': '8vh',  
                'width': '6%',  # Ajusta el ancho para mejor visualización
                'position': 'fixed',
                'top': '22vh',
                'left': '16.5vw'
            },
            maxHeight=130,   # Ajusta la altura del dropdown cuando se despliega
            optionHeight=20  # Ajusta la altura de cada opción individual
        ),
    ]),

         html.Div(id='output-info', style={'margin-top': '0.1vh'}),

                html.Div(id='output-details', style={
                    'fontSize': '0.55vw',
                    'fontWeight': 'bold',
                    'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                    'padding': '0.1vw',
                    'borderRadius': '0.5vw',
                    'textAlign': 'left',
                    'marginBottom': '0.1vh',
                    'width': '20%',
                    'height': '3vh',
                    'position': 'fixed',
                    'top': '10vh',
                    'left': '22vw'

                }, children=[

                    # 📌 Promedio ICAM
                    html.H3(id='promedio-icam', style={
                        'fontSize': '0.75vw',
                        'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                        'backgroundColor': '#949191',
                        'textAlign': 'left',
                        'width': '12%',
                        'position': 'fixed',
                        'top': '22vh',
                        'height': '2vh',
                        'left': '23vw',
                        'borderRadius': '0.1vw'
                    }),

                    # 📌 CARACTERIZACIÓN CONFORT AMBIENTAL
                    html.P(id='comfort-ambiental', style={
                        'fontSize': '0.8vw',
                        'backgroundColor': '#949191',
                        'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                        'textAlign': 'left',
                        'width': '35%',
                        'position': 'fixed',
                        'top': '28vh',
                        'height': '3vh',
                        'left': '23vw',
                        'borderRadius': '0.5vw'
                    }),

                # 📌 NOTA DE CONFORT AMBIENTAL SOBRE EL CONFORT TÉRMICO
                    html.Div([
                    html.P(id='promedio-nota-icam-ict'),
                    html.P(id='caracterizacion-ict'),


                ], style={
                    'display': 'flex',
                    'backgroundColor': '#949191',
                    'fontSize': '0.75vw',
                    'fontWeight': 'bold',
                    'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                    'textAlign': 'left',
                    'padding': '0.1vw',
                    'position': 'fixed',
                    'width': '12%',
                    'top': '29.5vh',
                    'left': '23vw',
                    'height': '3vh',
                    'borderRadius': '0.1vw'
                }),


                # 📌 CALIFICACIÓN  CONFORT AMBIENTAL DE LA CALIDAD DEL AIRE
                    html.Div([
                    html.P(id='promedio-nota-icam-ica'),
                    html.P(id='caracterizacion-ica'),


                ], style={
                    'display': 'flex',
                    'backgroundColor': '#949191',
                    'fontSize': '0.75vw',
                    'fontWeight': 'bold',
                    'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                    'textAlign': 'left',
                    'padding': '0.1vw',
                    'position': 'fixed',
                    'width': '12%',
                    'top': '33vh',
                    'left': '23vw',
                    'height': '3vh',
                    'borderRadius': '0.1vw'
                }),


                # 📌 CALIFICACIÓN CONFORT AMBIENTAL DEL RUIDO AMBIENTAL
                    html.Div([
                    html.P(id='promedio-nota-icam-ira'), 
                    html.P(id='caracterizacion-ira'),

                ], style={
                    'display': 'flex',
                    'backgroundColor': '#949191',
                    'fontSize': '0.75vw',
                    'fontWeight': 'bold',
                    'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                    'textAlign': 'left',
                    'position': 'fixed',
                    'width': '12%',
                    'top': '36.5vh',
                    'left': '23vw',
                    'height': '3vh',
                    'borderRadius': '0.1vw'
                }),



        # 📌 Total de parques
        html.P(
        id='total-parques',
        style={
            'fontSize': '0.70vw',  # Tamaño de fuente adaptable
            'fontFamily': 'Franklin Gothic Condensed, sans-serif',
            'fontWeight': 'bold',
            'textAlign': 'Left',  # Alineación del texto
            'backgroundColor': '#949191',  # Fondo gris claro
            'borderRadius': '5px',  # Bordes redondeados
            'padding': '0.1vw',  # Espaciado interno
            'width': '12%',  # Ancho del contenedor
            'position': 'fixed',
            'height': '3vh',
            'top': '40vh',
            'left': '23vw'
        }
        ),   

            # Diagnóstico general
            html.Div(
            style={
            'backgroundColor': '#D3D3D3',
            "fontSize": "0.75vw",  
            'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
            'color': 'white',
            'padding': '0.5vw',
            'borderRadius': '5px',
            'marginTop': '1vh',
            'textAlign': 'Top',
            'width': '15vw',
            'height': '21vh',  # 🔹 Define una altura fija en vh
            'position': 'fixed',  # Posiciona el elemento de manera absoluta
            'top': '21vh',  # Lo mueve hacia la parte superior
            'left': '1vw',  # Lo alinea a la izquierda
            'margin': '1',  # Elimina márgenes automáticos
            },
                children=[
                html.P(f"El confort ambiental en los parques vecinales de Bogotá es moderado, con un Índice de Confort Ambiental (ICAM) promedio de 45.43. Esto sugiere que las condiciones no son óptimas, pero tampoco deficientes. Los principales problemas se relacionan con la calidad del aire y el ruido ambiental, lo que puede manifestarse en estrés leve o problemas respiratorios en la población vulnerable, y a su vez, reduce el disfrute y la relajación en estos espacios públicos. ", 
                    style={'textAlign': 'justify', 'color': 'black', 'fontSize': '0.7vw', 'fontWeight': 'normal'}),
                ]
            ),


# 📌 Confort Ambiental Por Localidad
html.Div(
    style={
        'backgroundColor': "#949191",
        'fontSize': '0.75vw',
        'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
        'padding': '0.1vw',
        'borderRadius': '5px',
        'marginTop': '0.1vh',
        'textAlign': 'left',
        'width': '34%',
        'position': 'fixed',  # Posiciona el elemento de manera absoluta
        'top': '46vh',  # Lo mueve hacia la parte superior
        'left': '1vw',  # Lo alinea a la izquierda
        'margin': '0',  # Elimina márgenes automáticos
},

children=[
    html.B("Mejor Localidad: ", style={'color': 'black'}),
    html.Span(f"{mejor_localidad['localidad']} - ICAM promedio de {mejor_localidad['icam']:.2f}", 
    style={'fontSize': '0.75vw', 'color': 'lightgreen', 'fontWeight': 'bold'}),  
    html.Span("| "),  
    html.B("Peor Localidad: ", style={'color': 'black'}), 
    html.Span(f"{peor_localidad['localidad']} - ICAM promedio de {peor_localidad['icam']:.2f}", 
            style={'fontSize': '0.75vw', 'color': 'khaki', 'fontWeight': 'bold'})  
    ]
),

# 📌 INFORMACIÓN DE PARQUE SELECCIONADO
        html.Div(
            id="info-parque",
            style={
                'backgroundColor': '#D3D3D3',
                "marginTop": "1vw",  
                "fontSize": "0.65vw",  
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                "textAlign": "left",  
                "padding": "6px",  
                "borderRadius": "8px",  
                'width': '25%',
                'height': '27vh',  # 🔹 Define una altura fija en vh
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '3.5vh',  # Lo mueve hacia la parte superior
                'left': '74vw',  # Lo alinea a la izquierda
                'margin': '0',  # Elimina márgenes automáticos
            }
        ),

        ])
    ])


# Callback para redirigir según el indicador seleccionado
@app.callback(
    Output("url", "href"),
    Input("selector-indicador", "value"),
    prevent_initial_call=True
)
def redirigir_por_indicador(indicador):
    if indicador == "ICA":
        return "http://localhost:8050"
    elif indicador == "ICT":
        return "http://localhost:8051"
    elif indicador == "IRA":
        return "http://localhost:8052"
    elif indicador == "ICAM":
        return "http://localhost:8053"  
    return dash.no_update

# 🔹 Función para calcular el zoom según el tamaño del polígono
def calcular_zoom(latitudes, longitudes):
    lat_diff = max(latitudes) - min(latitudes)
    lon_diff = max(longitudes) - min(longitudes)
    max_diff = max(lat_diff, lon_diff)

    if max_diff > 0.3:
        return 9
    elif max_diff > 0.15:
        return 11
    elif max_diff > 0.07:
        return 12
    elif max_diff > 0.03:
        return 13
    else:
        return 14

# 🔹 Callback para actualizar mapa
@app.callback(
    Output('mapa', 'figure'),
    Input('dropdown-localidad', 'value'),
    prevent_initial_call=True
)
def actualizar_zoom(localidad):
    if not localidad:
        return dash.no_update

    nombre_input = limpiar_nombre(localidad)

    # 🔍 Buscar la localidad con nombre normalizado
    feature = next(
        (f for f in geojson_localidades["features"]
         if f["properties"]["Nombre_normalizado"] == nombre_input),
        None
    )

    if feature is None:
        print(f"No se encontró la localidad: {nombre_input}")
        return dash.no_update

    # 🔹 Manejo robusto de estructuras geométricas
    coords_raw = feature["geometry"]["coordinates"]
    tipo_geo = feature["geometry"]["type"]

    if tipo_geo == "Polygon":
        coords = np.array(coords_raw[0])
    elif tipo_geo == "MultiPolygon":
        coords = np.array(coords_raw[0][0])
    else:
        print(f"Tipo de geometría no soportado: {tipo_geo}")
        return dash.no_update

    if coords.ndim == 3:
        coords = np.vstack(coords)

    latitudes = coords[:, 1]
    longitudes = coords[:, 0]

    centro_lat = np.mean(latitudes)
    centro_lon = np.mean(longitudes)
    zoom_nivel = calcular_zoom(latitudes, longitudes)

    # 🔹 Actualizar figura del mapa
    fig_mapa.update_traces(selector=dict(name="Localidad Seleccionada"), visible=False)

    fig_mapa.add_trace(
        go.Scattermapbox(
            name="Localidad Seleccionada",
            lon=np.append(longitudes, longitudes[0]),
            lat=np.append(latitudes, latitudes[0]),
            mode="lines",
            line=dict(width=3, color="black"),
            fill=None
        )
    )

    fig_mapa.update_layout(
    mapbox=dict(
        center={"lat": centro_lat, "lon": centro_lon},
        zoom=zoom_nivel,
        style="carto-positron"
    ),
    autosize=True,  # ✅ Para que use el tamaño del contenedor
    margin={"r": 0, "t": 0, "l": 0, "b": 0},  # ✅ Para que no añada espacios internos
    uirevision="mapa-fijo"  # ✅ Para mantener la vista si no cambia el zoom
)

    return fig_mapa



# Callback para mostrar información cuando se selecciona un parque en el mapa
@app.callback(
    Output("info-parque", "children"),
    Input("mapa", "clickData")
)
def mostrar_info(clickData):
    if not clickData:
        return "Información Parque Vecinal."

    try:
        punto = clickData["points"][0]
        nombre = punto["hovertext"]

        # Filtrar información de cada índice ambiental
        parque_info_ica = data_ica[data_ica["parque"] == nombre]
        parque_info_ira = data_ira[data_ira["parque"] == nombre]
        parque_info_ict = data_ict[data_ict["parque"] == nombre]
        parque_info_icam = data_icam[data_icam["parque"] == nombre]

        if parque_info_ica.empty:
            return "⚠️ No se encontró información del parque seleccionado."

        parque_info = parque_info_ica.iloc[0]
        valor_ica = parque_info["ica_general"]
        
        
        # Obtener diagnóstico ICA según el rango
        diagnostico_ica = "No hay diagnóstico disponible."
        numero_estrategia_ica = [] 

        if "rango_ica" in data_de_ica.columns:
            for _, row in data_de_ica.iterrows():
                rango = str(row["rango_ica"]).strip()

                # Convertir rango a valores numéricos
                if "-" in rango:
                    try:
                        lim_inf, lim_sup = map(int, rango.split("-"))
                        
                        # Comparación segura con valores numéricos
                        if lim_inf <= valor_ica <= lim_sup:
                            diagnostico_ica = row["diagnostico_ica"]
                            numero_estrategia_ica.append(row["numero_estrategia_ica"])
                            break  
                    except ValueError:
                        print(f"⚠️ Error al procesar el rango: {rango} (Formato incorrecto)")
                else:
                    print(f"⚠️ Advertencia: El valor '{rango}' no es un rango válido.")
        else:
            print("⚠️ Error: La columna 'rango_ica' no está en el DataFrame.")

                # Ver los nombres de las columnas originales antes del renombramiento
        print("Columnas originales en data_dict['DE_ICA']:", data_dict['DE_ICA'].columns)


        # 📌 DIAGNÓSTICO ICAM
        diagnostico_icam = "No hay diagnóstico disponible."

        if not parque_info_icam.empty:
            valor_icam = float(parque_info_icam.iloc[0]['icam'])  # 🔹 Convertir a número flotante

            if "rango_icam" in data_de_icam.columns:
                for _, row in data_de_icam.iterrows():
                    rango = str(row["rango_icam"]).strip()
                    if "-" in rango:
                        try:
                            lim_sup, lim_inf = map(float, rango.split("-"))  # 🔹 Orden corregido: sup -> inf
                            if lim_inf <= valor_icam <= lim_sup:
                                diagnostico_icam = row["diagnostico_icam"]
                                break  # 🔹 Salir del loop al encontrar el diagnóstico
                        except ValueError:
                            print(f"⚠️ Error al procesar el rango: {rango} (Formato incorrecto)")
                
        
        # Obtener diagnóstico ICT según el rango
        diagnostico_ict = "No hay diagnóstico disponible."
        numero_estrategia_ict = []  # Lista para almacenar múltiples estrategias

        if not parque_info_ict.empty:
            valor_ict = parque_info_ict.iloc[0]['ict']
            if "rango_ict" in data_de_ict.columns:
                for _, row in data_de_ict.iterrows():
                    rango = str(row["rango_ict"]).strip()
                    if "-" in rango:
                        try:
                            lim_inf, lim_sup = map(float, rango.split("-"))
                            if lim_inf <= valor_ict <= lim_sup:
                                diagnostico_ict = row["diagnostico_ict"]
                                numero_estrategia_ict.append(row["numero_estrategia_ict"])  # Agregar número de estrategia a la lista
                        except ValueError:
                            print(f"⚠️ Error al procesar el rango: {rango} (Formato incorrecto)")
                            
        # Inicializar valor_ira con un valor predeterminado
        valor_ira = None  

        # Verificar si el DataFrame de IRA está vacío
        if parque_info_ira.empty:
            print("⚠️ No se encontró información del parque seleccionado en parque_info_ira.")
            valor_ira = None
        else:
            try:
                valor_ira = float(str(parque_info_ira.iloc[0]['ira']).replace(',', '.'))
                print(f"✅ Valor IRA obtenido: {valor_ira}")
            except ValueError:
                print(f"⚠️ Error: el valor IRA no es un número válido -> {parque_info_ira.iloc[0]['ira']}")
                valor_ira = None

        # Si no se obtuvo un valor válido, detener el proceso
        if valor_ira is None:
            print("🚨 Error: No se pudo obtener un valor válido para valor_ira.")
        else:
            # Asegurar que la columna "diagnostico_ira" no tenga valores vacíos
            data_de_ira["diagnostico_ira"].fillna("No disponible", inplace=True)

            # Inicializar diagnóstico y estrategias
            diagnostico_ira = "No hay diagnóstico disponible."
            numero_estrategia_ira = []

            # Recorrer los datos de IRA y verificar rangos
            for _, row in data_de_ira.iterrows():
                rango = str(row["rango_ira"]).strip()  # Asegurar que es string y limpiar espacios

                if "-" in rango:
                    try:
                        lim_sup, lim_inf = map(float, rango.split("-"))  # Convertir los límites en números
                        print(f"🔹 Procesando rango: {lim_inf} - {lim_sup}")

                        # Verificar si el valor IRA está dentro del rango
                        if lim_inf <= valor_ira <= lim_sup:
                            diagnostico_ira = row["diagnostico_ira"]
                            numero_estrategia_ira.append(row["numero_estrategia_ira"])
                            print(f"✅ {valor_ira} está en el rango {lim_inf}-{lim_sup}")
                            print(f"✅ Diagnóstico asignado: {diagnostico_ira}")
                            print(f"✅ Estrategia agregada: {row['numero_estrategia_ira']}")
                    except ValueError:
                        print(f"⚠️ Error al convertir los valores del rango: {rango}")
                else:
                    print(f"⚠️ Rango inválido encontrado: {rango}")

            # Mostrar resultados finales
            print(f"📝 Diagnóstico final: {diagnostico_ira}")
            print(f"📋 Estrategias asignadas: {numero_estrategia_ira}")


        # Extraer datos de IRA
        ira = parque_info_ira.iloc[0]["ira"] if not parque_info_ira.empty else "N/A"
        nivel_ruido = parque_info_ira.iloc[0]["nivel_ruido"] if not parque_info_ira.empty else "N/A"
        decibelios = parque_info_ira.iloc[0]["decibelios"] if not parque_info_ira.empty else "N/A"

        # Extraer datos de ICT
        temperatura = f"{parque_info_ict.iloc[0]['temperatura']:.2f}°C" if not parque_info_ict.empty else "N/A"
        humedad = f"{parque_info_ict.iloc[0]['humedad']:.2f}%" if not parque_info_ict.empty else "N/A"
        velocidad_viento = f"{parque_info_ict.iloc[0]['velocidad_viento']:.2f} m/s" if not parque_info_ict.empty else "N/A"
        ict = f"{parque_info_ict.iloc[0]['ict']:.2f}" if not parque_info_ict.empty else "N/A"
        sensacion_termica = parque_info_ict.iloc[0]["sensasion_termica"] if not parque_info_ict.empty else "N/A"

        # Extraer datos de ICAM
        icam = f"{parque_info_icam.iloc[0]['icam']:.2f}" if not parque_info_icam.empty else "N/A"
        confort_ambiental = parque_info_icam.iloc[0]["confort_ambiental"] if not parque_info_icam.empty else "N/A"

        return html.Div([
            html.Div([
                html.Span(f"📍 {nombre}", style={'fontSize': '0.7vw', 'backgroundColor': '#A9A9A9', 'padding': '5px', 'borderRadius': '5px', 'marginRight': '10px'}),
                html.Span(f"🏙 Localidad: {parque_info['localidad']}", style={'fontSize': '0.7vw', 'backgroundColor': '#A9A9A9', 'padding': '5px', 'borderRadius': '5px'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),

            html.Div([
                html.Span(f"🍃 Índice de Calidad del Aire (ICA): {parque_info['ica_general']:.2f}", style={'fontSize': '0.7vw','fontWeight': 'bold'}),
                html.Span(f" |  🍃 Estado ICA Parque: {parque_info['Estado']}", style={'fontSize': '0.7vw','fontWeight': 'bold'})
            ], style={'display': 'flex', 'alignItems': 'center'}),

            html.Div([
                html.Span(f"🍃 Estado ICA (PM2.5): {parque_info['estado_pm25']}", style={'fontSize': '0.65vw'}),
                html.Span(f"🍃 Valor ICA (PM2.5): {parque_info['ica_pm25']:.2f}", style={'fontSize': '0.65vw', 'marginLeft': '10px'}),
                html.Span(f"🍃 PM2.5: {parque_info['pm25']:.2f} µg/m³", style={'fontSize': '0.65vw', 'marginLeft': '10px'})
            ], style={'display': 'flex', 'alignItems': 'center'}),

            html.Div([
                html.Span(f"🍃 Estado ICA (PM10): {parque_info['estado_pm10']}", style={'fontSize': '0.65vw'}),
                html.Span(f"🍃 Valor ICA (PM10): {parque_info['ica_pm10']:.2f}", style={'fontSize': '0.65vw', 'marginLeft': '10px'}),
                html.Span(f"🍃 PM10: {parque_info['pm10']:.2f} µg/m³", style={'fontSize': '0.65vw', 'marginLeft': '10px'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),


            html.Div([
                html.Span(f"🔊 Índice de Ruido Ambiental (IRA): {ira:.2f}", style={'fontSize': '0.7vw','fontWeight': 'bold'}),
                html.Span(f" |  🔊 Nivel Ruido Ambiental: {nivel_ruido}", style={'fontSize': '0.7vw','fontWeight': 'bold'})
            ], style={'display': 'flex', 'alignItems': 'center'}),

            html.Div([
                html.Span(f"🔊 Decibelios por parque: {decibelios}", style={'fontSize': '0.65vw'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),


html.Div([
# DIAGNÓSTICO ICAM
html.Div([
    html.Span(f"📝: {diagnostico_icam}", 
            style={
                'backgroundColor': '#D3D3D3',
                'fontSize': '0.63vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  
                'padding': '0.3vw',
                'borderRadius': '5px',
                'textAlign': 'justify',
                'marginBottom': '0.1vh',
                'width': '25%',
                'height': '6.2vh',
                'position': 'fixed',  
                'top': '33.5vh',  
                'left': '74vw',  
            })
    ])
]),



html.Div([
# DIAGNÓSTICO ICA
html.Div([
    html.Span(f"📝: {diagnostico_ica}", 
            style={
                'backgroundColor': '#D3D3D3',
                'fontSize': '0.65vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  
                'padding': '0.5vw',
                'borderRadius': '5px',
                'textAlign': 'justify',
                'marginBottom': '0.5vh',
                'width': '16.5%',
                'height': '15vh',
                'position': 'fixed',  
                'top': '42vh',  
                'left': '74vw',  
            })
    ])
]),


html.Div([
# ESTRATEGIAS ICA
html.Div([
    html.Span(f"📝: {numero_estrategia_ica}", 
            style={
                'backgroundColor': '#D3D3D3',
                'fontSize': '0.70vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'fontWeight': 'normal',
                'padding': '0.5vw',
                'borderRadius': '5px',
                'textAlign': 'justify',
                'width': '8%',
                'height': '8vh',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '42vh',  # Lo mueve hacia la parte superior
                'left': '91vw',  # Lo alinea a la izquierda
            })
    ])
]),


html.Div([
# DIAGNÓSTICO IRA
html.Div([
    html.Span(f"📝: {diagnostico_ira}", 
            style={
                'backgroundColor': '#D3D3D3',
                'fontSize': '0.70vw',
                'fontWeight': 'normal',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
                'padding': '0.5vw',
                'borderRadius': '5px',
                'textAlign': 'justify',
                'width': '16.5%',
                'height': '15vh',
                'position': 'fixed',  # Posiciona el elemento de manera absoluta
                'top': '60vh',  # Lo mueve hacia la parte superior
                'left': '74vw',  # Lo alinea a la izquierda
            })
    ])
]),

html.Div([
# ESTRATEGIAS IRA
html.Div([
    html.Span(f"📝: {numero_estrategia_ira}", 
            style={
              'backgroundColor': '#D3D3D3',
            'fontSize': '0.70vw',
            'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
            'fontWeight': 'normal',
            'padding': '0.5vw',
            'borderRadius': '5px',
            'textAlign': 'justify',
            'width': '8%',
            'height': '8vh',
            'position': 'fixed',  # Posiciona el elemento de manera absoluta
            'top': '60vh',  # Lo mueve hacia la parte superior
            'left': '91vw',  # Lo alinea a la izquierda
            })
    ])
]),

            html.Div([
                html.Span(f"🌡️ Índice de Confort Térmico (ICT): {ict}", style={'fontSize': '0.7vw','fontWeight': 'bold'}),
                html.Span(f" |  🌡️ Sensación Térmica: {sensacion_termica}", style={'fontSize': '0.7vw','fontWeight': 'bold'})
            ], style={'display': 'flex', 'alignItems': 'center'}),

            html.Div([
                html.Span(f"🌡️ Temperatura: {temperatura}", style={'fontSize': '0.65vw'}),
                html.Span(f" |  🌡️ Humedad: {humedad}", style={'fontSize': '0.65vw'}),
                html.Span(f" |  🌡️ Viento: {velocidad_viento}", style={'fontSize': '0.65vw'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),

html.Div([
# DIAGNOSTICO ICT
html.Div([
    html.Span(f"📝: {diagnostico_ict}", 
            style={
                'backgroundColor': '#D3D3D3',
                'fontweight': 'normal',
                'fontSize': '0.65vw',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',  
                'padding': '0.5vw',
                'borderRadius': '0.5vw',
                'textAlign': 'justify',
                'marginBottom': '0.5vh',
                'width': '16.5%',
                'height': '15vh',
                'position': 'fixed',  
                'top': '78vh',  
                'left': '74vw',  
            })
    ])
]),

html.Div([
# ESTRATEGIAS ICT
html.Div([
    html.Span(f"📝: {numero_estrategia_ict}", 
            style={
             'backgroundColor': '#D3D3D3',
            'fontSize': '0.70vw',
            'fontFamily': 'Franklin Gothic Condensed, sans-serif',  # Cambia la fuente
            'fontWeight': 'normal',
            'padding': '0.5vw',
            'borderRadius': '5px',
            'textAlign': 'justify',
            'width': '8%',
            'height': '8vh',
            'position': 'fixed',  # Posiciona el elemento de manera absoluta
            'top': '78vh',  # Lo mueve hacia la parte superior
            'left': '91vw',  # Lo alinea a la izquierda
            })
    ])
]),


            html.Div([
                html.Span(f"🏡 Índice de Confort Ambiental (ICAM): {icam}", style={'fontSize': '0.7vw','fontWeight': 'bold'}),
                html.Span(f" |  🏡 Confort Ambiental Parque : {confort_ambiental}", style={'fontSize': '0.7vw','fontWeight': 'bold'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ])
    
    except Exception as e:
        return f"Error al obtener la información: {str(e)}"



@app.callback(
    Output("imagen-modal", "is_open"),              
    Output("imagen-modal-mostrado", "data"),       
    Input("mostrar-imagen-btn", "n_clicks"),
    Input("imagen-modal-mostrado", "data"),
    prevent_initial_call=False
)
def toggle_modal(n_clicks, ya_mostrado):
    ctx = dash.callback_context

    # Si no se ha mostrado aún, lo mostramos al cargar
    if not ya_mostrado:
        return True, True

    # Si el usuario hace clic en el botón
    if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("mostrar-imagen-btn"):
        return True, True

    # Por defecto, no se muestra nada
    return False, ya_mostrado


# ----------------------------------
# Obtener estado y color basado en valor ICAM
# ----------------------------------
def obtener_estado_color(value):
    if 0 <= value <= 19:
        return 'Malo', 'orangered'
    elif value <= 39:
        return 'Bajo', 'orange'
    elif value <= 59:
        return 'Moderado', 'khaki'
    elif value <= 79:
        return 'Bueno', 'lightgreen'
    elif value <= 100:
        return 'Óptimo', 'darkgreen'
    else:
        return 'Fuera de Rango', 'gray'


@app.callback(
    [
        Output('promedio-icam', 'children'),
        Output('comfort-ambiental', 'children'),
        Output('comfort-ambiental', 'style'),
        Output('promedio-nota-icam-ict', 'children'),
        Output('caracterizacion-ict', 'children'),
        Output('promedio-nota-icam-ica', 'children'),
        Output('caracterizacion-ica', 'children'),
        Output('promedio-nota-icam-ira', 'children'),
        Output('caracterizacion-ira', 'children'),
        Output('total-parques', 'children')
    ],
    Input('dropdown-localidad', 'value')
)
def actualizar_info(localidad):
    df_localidad = data_icam[data_icam['localidad'] == localidad]

    if df_localidad.empty:
        no_datos = html.Span("No hay datos")
        return (no_datos, no_datos, {'color':'black'},
                no_datos, no_datos, no_datos,
                no_datos, no_datos, no_datos,
                html.Span("Total de parques: 0"))

    # numéricos
    promedio_icam = df_localidad['icam'].mean(skipna=True)
    confort_ambiental, color_icam = obtener_estado_color(promedio_icam)

    promedio_nota_icam_ict = df_localidad['nota-icam-ict'].mean(skipna=True)
    promedio_nota_icam_ica = df_localidad['nota-icam-ica'].mean(skipna=True)
    promedio_nota_icam_ira = df_localidad['nota-icam-ira'].mean(skipna=True)

    # textuales: extraer la moda (valor más frecuente)
    def moda_textual(col):
        m = df_localidad[col].mode()
        return m.iloc[0] if not m.empty else "No hay datos"

    caracterizacion_ict = moda_textual('caracterizacion-ict')
    caracterizacion_ica = moda_textual('caracterizacion-ica')
    caracterizacion_ira = moda_textual('caracterizacion-ira')

    total_parques = len(df_localidad)

    return (
        # Promedio ICAM
        html.Span([
            "Promedio ICAM: ",
            html.Span(f"{promedio_icam:.2f}", style={'color': color_icam, 'fontWeight': 'bold'})
        ]),


        # Estado ICAM
        html.Span([
            html.Span("Estado ICAM: ", style={'color': 'black', 'fontWeight': 'bold'}),
            f"{confort_ambiental}"
        ]),
        
        # Estilo del badge
        {
            'color': color_icam,
            'fontSize': '0.7vw',
            'fontFamily': 'Franklin Gothic Condensed, sans-serif',
            'textAlign': 'justify',
            'width': '12%',
            'position': 'fixed',
            'height': '3vh',
            'top': '25.5vh',
            'left': '23vw',
            'backgroundColor': '#949191',
            'borderRadius': '0.1vw',
            'fontWeight': 'bold'
        },
        # Nota ICT
        html.Span([
            "Nota ICT: ",
            html.Span(f"{promedio_nota_icam_ict:.2f}%", style={'color': color_icam, 'fontWeight': 'bold'})
        ]),

        # Caracterización ICT
        html.Span(caracterizacion_ict, style={'color': color_icam, 'fontWeight': 'bold'}),


        # Nota ICA
        html.Span([
            "Nota ICA: ",
            html.Span(f"{promedio_nota_icam_ica:.2f}% - ", style={'color': color_icam, 'fontWeight': 'bold'})
        ]),

        # Caracterización ICA
        html.Span( caracterizacion_ica, style={'color': color_icam, 'fontWeight': 'bold'}),


        # Nota IRA
        html.Span([
            "Nota IRA: ",
            html.Span(f"{promedio_nota_icam_ira:.2f}%", style={'color': color_icam, 'fontWeight': 'bold'})
        ]),
        # Caracterización IRA
        html.Span(caracterizacion_ira, style={'color': color_icam, 'fontWeight': 'bold'}),


        # Total de parques
        html.Span(f"Total de parques en {localidad}: {total_parques}")
    )


# 📌 CALLBACK para mostrar/ocultar las tablas
@app.callback(
    [Output("modal-tabla-ira", "is_open"), Output("tabla-estrategias-ira", "children"),
     Output("modal-tabla-ict", "is_open"), Output("tabla-estrategias-ict", "children"),
     Output("modal-tabla-ica", "is_open"), Output("tabla-estrategias-ica", "children")],

    [Input("mostrar-matriz-ira", "n_clicks"), Input("cerrar-tabla-ira", "n_clicks"),
     Input("mostrar-matriz-ict", "n_clicks"), Input("cerrar-tabla-ict", "n_clicks"),
     Input("mostrar-matriz-ica", "n_clicks"), Input("cerrar-tabla-ica", "n_clicks")],

    prevent_initial_call=True
)
def toggle_modals(n_ira, c_ira, n_ict, c_ict, n_ica, c_ica):
    ctx = dash.callback_context  
    if not ctx.triggered:
        return dash.no_update  

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    def generar_tabla(df):
        if df.empty:
            return html.P("⚠️ No se pudieron cargar los datos.")

        return dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),

            # 🔹 Hacer la tabla desplazable horizontalmente
            style_table={'overflowX': 'auto'},

            # 🔹 Estilo de las celdas
            style_cell={
                'textAlign': 'left',  # Alineación del texto
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                'fontSize': '1.5vh',
                'color': '#333',
                'padding': '8px',
                'whiteSpace': 'normal',  # 🔹 Permitir saltos de línea
                'wordBreak': 'break-word',  # 🔹 Dividir palabras largas
                'maxWidth': '150px',  # 🔹 Ancho máximo de celdas
            },

            # 🔹 Estilo del encabezado
            style_header={
                'backgroundColor': '#4CAF50',
                'fontFamily': 'Franklin Gothic Condensed, sans-serif',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'fontSize': '1.5vh'
            },

            # 🔹 Estilo de filas alternas (zebra)
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f2f2f2'
                }
            ],
            
            page_size=10  # 🔹 Muestra 10 filas por página
        )

    if trigger_id == "mostrar-matriz-ira":
        return True, generar_tabla(df_ira), False, None, False, None
    if trigger_id == "cerrar-tabla-ira":
        return False, None, False, None, False, None

    if trigger_id == "mostrar-matriz-ict":
        return False, None, True, generar_tabla(df_ict), False, None
    if trigger_id == "cerrar-tabla-ict":
        return False, None, False, None, False, None

    if trigger_id == "mostrar-matriz-ica":
        return False, None, False, None, True, generar_tabla(df_ica)
    if trigger_id == "cerrar-tabla-ica":
        return False, None, False, None, False, None

    return dash.no_update

server = app.server

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))