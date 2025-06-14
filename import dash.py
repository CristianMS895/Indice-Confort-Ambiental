import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, Input, Output, State

# Inicializar la aplicación Dash con Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "GEOVISOR ICAM BOGOTÁ"

# Cargar datos de Excel
archivo_excel = 'Matriz General de Indicadores.xlsx'
sheets_to_load = ['ICA-BD', 'IRA-BD', 'ICT-BD', 'ICAM-BD', 'DE_ICA', 'DE_ICT', 'DE_IRA']
data_dict = pd.read_excel(archivo_excel, sheet_name=sheets_to_load, engine='openpyxl')

# Extraer datos específicos de la hoja IRA-BD
data_de_ira = data_dict['IRA-BD']
estrategias_unicas = data_de_ira["numero_estrategia_ira"].dropna().unique()

# 📌 Layout de la aplicación
app.layout = html.Div([
    html.H1("Estrategias de Mejora del Ruido Ambiental", style={'textAlign': 'center'}),

    # 🔹 Botón fijo en la pantalla
    html.Div(
        style={
            'position': 'fixed',  # 🔹 Fijo en la pantalla
            'bottom': '3vh',  # 🔹 Ubicación desde la parte inferior
            'right': '5vw',  # 🔹 Ubicación desde la derecha
            'zIndex': '1000',  # 🔹 Asegura que esté sobre otros elementos
            'textAlign': 'center'
        },
        children=[
            # 📌 Botón para abrir el modal
            html.Button(
                "Ver Estrategias",
                id="abrir-modal-estrategias",
                n_clicks=0,
                style={
                    "fontSize": "1vw",
                    "padding": "0.8vh 1.5vw",
                    "cursor": "pointer",
                    "borderRadius": "8px",
                    "backgroundColor": "#007BFF",
                    "color": "white",
                    "border": "none",
                    "width": "12vw",
                    "height": "5vh",
                    "boxShadow": "2px 2px 5px rgba(0,0,0,0.3)"  # 🔹 Sombra para visibilidad
                }
            ),

            # 📌 Modal con las estrategias
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        dbc.ModalTitle("Estrategias de Mejora del Ruido Ambiental"),
                        close_button=True
                    ),
                    dbc.ModalBody(
                        html.Div(id="modal-contenido-estrategias", style={"textAlign": "justify"})
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Cerrar", id="cerrar-modal-estrategias", className="ml-auto", color="secondary")
                    ),
                ],
                id="modal-estrategias",
                is_open=False,
                centered=True,
                size="lg"
            )
        ]
    )
])

# 📌 Callback para abrir y cerrar el modal de estrategias
@app.callback(
    Output("modal-estrategias", "is_open"),
    [Input("abrir-modal-estrategias", "n_clicks"),
     Input("cerrar-modal-estrategias", "n_clicks")],
    [State("modal-estrategias", "is_open")]
)
def toggle_modal(n_abrir, n_cerrar, is_open):
    if n_abrir or n_cerrar:
        return not is_open
    return is_open

# 📌 Callback para abrir y mostrar la información de una estrategia
@app.callback(
    [Output("modal", "is_open"), Output("modal-content", "children")],
    [Input({"type": "btn-estrategia", "index": estrategia}, "n_clicks") for estrategia in estrategias_unicas] +
    [Input("close-modal", "n_clicks")],
    [State("modal", "is_open")]
)
def mostrar_estrategia(*args):
    ctx = dash.callback_context

    # Si no hay interacción, no abrir el modal
    if not ctx.triggered:
        return False, ""

    # Obtener el ID del botón presionado
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Si se presionó el botón de cerrar
    if button_id == "close-modal":
        return False, ""

    # Extraer la estrategia seleccionada
    estrategia_seleccionada = eval(button_id)["index"]

    # Filtrar información de la estrategia
    estrategia_info = data_de_ira[data_de_ira["numero_estrategia_ira"] == estrategia_seleccionada]

    if estrategia_info.empty:
        return True, "No se encontró información para esta estrategia."

    # Crear contenido del modal
    contenido = html.Div([
        html.H4(f"Nombre: {estrategia_info['nombre_estrategia_ira'].values[0]}"),
        html.P(f"Descripción: {estrategia_info['descripcion_estrategia_ira'].values[0]}")
    ])

    return True, contenido

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)