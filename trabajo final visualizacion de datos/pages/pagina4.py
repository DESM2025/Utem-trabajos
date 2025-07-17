import streamlit as st
import pandas as pd
import plotly.express as px
from pytrends.request import TrendReq
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

st.markdown(
    """
<style>
    /* Fondo principal: Blanco */
    .stApp {
        background-color: #FFFFFF;
        color: black; /* Texto general en el área principal a negro */
    }

    /* FORZAR LA BARRA LATERAL A ROJO Y SU TEXTO A BLANCO */
    /* Apunta a la barra lateral principal */
    .stSidebar {
        background-color: #BC002D !important; /* Color rojo de la bandera, ¡FORZADO! */
    }

    /* Asegurarse de que TODOS los elementos de texto dentro de la barra lateral sean blancos */
    .stSidebar * {
        color: white !important;
    }

    /* Estilos específicos para elementos interactivos en la barra lateral */
    .stSidebar .stButton > button {
        color: white !important;
        border: 1px solid white !important;
        background-color: #BC002D !important; /* Asegura el fondo del botón en rojo */
    }
    .stSidebar .stButton > button:hover {
        background-color: #A00020 !important; /* Un rojo un poco más oscuro al pasar el ratón */
    }

    .stSidebar label { /* Etiquetas de los widgets en el sidebar */
        color: white !important;
    }

    /* Asegurar el texto y el color de fondo para selectbox/input dentro del sidebar */
    .stSidebar div[data-baseweb="select"] > div {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.2) !important; /* Fondo ligeramente transparente para los selectbox */
    }
    .stSidebar div[data-baseweb="input"] > div {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.2) !important; /* Fondo ligeramente transparente para los inputs */
    }
    .stSidebar div[data-baseweb="input"] input,
    .stSidebar div[data-baseweb="select"] input {
        color: white !important;
    }
    /* Estilos para el slider en la barra lateral */
    .stSidebar .stSlider .st-cq { /* La barra de fondo del slider */
        background-color: rgba(255, 255, 255, 0.3) !important;
    }
    .stSidebar .stSlider .st-cp { /* El relleno de la barra del slider */
        background-color: white !important;
    }
    .stSidebar .stSlider .st-cu { /* El círculo del slider (thumb) */
        background-color: white !important;
        border: 1px solid #BC002D !important; /* Borde rojo para el círculo */
    }
    /* Asegurar los números del slider también en blanco */
    .stSidebar .stSlider [data-testid="stTickValue"],
    .stSidebar .stSlider [data-testid="stRelativeTickValue"] {
        color: white !important;
    }

    /* Estilos para el título principal y subtítulos en el área de contenido (fondo blanco) */
    h1, h2, h3, h4, h5, h6 {
        color: black; /* Títulos a negro */
    }

    /* Líneas divisorias (hr): Establecemos un color rosa para el cerezo */
    hr {
        border-top: 1px solid #FFC0CB; /* Rosa claro, color cerezo japonés */
    }

    /* Ajustes para botones en el área de contenido principal */
    .stButton>button {
        color: black;
        border: 1px solid #BC002D; /* Borde rojo */
        background-color: #F0F0F0;
    }
    .stButton>button:hover {
        background-color: #e0e0e0;
    }

    /* Ajustes para etiquetas de widgets (selectbox, text_input) en el área de contenido principal */
    .stSelectbox>label,
    .stTextInput>label,
    .stSlider>label,
    .stMultiSelect>label {
        color: black;
    }

    /* Ajuste para el texto dentro del spinner */
    .stSpinner > div > span {
        color: black;
    }

    /* Ajuste para el texto de advertencia (st.warning) y otros mensajes informativos */
    .stAlert {
        color: black;
        background-color: #FFFACD;
    }
    .stAlert > div > div > div { /* Para el texto del mensaje dentro de la alerta */
        color: black !important;
    }
    .stInfo, .stSuccess, .stWarning, .stError { /* Otros tipos de alertas */
        color: black;
    }

    /* Asegurar que el texto de las opciones en los selectbox y text_inputs en el área principal se vea y tengan fondo blanco */
    div[data-baseweb="select"] > div {
        color: black !important; /* Asegura el color del texto */
        background-color: white !important; /* Fondo blanco */
        border: 1px solid #FFB7C5 !important; /* Borde rosa sakura */
        border-radius: 5px; /* Bordes ligeramente redondeados */
    }
    /* Estilo para el input interno del selectbox */
    div[data-baseweb="select"] div[data-baseweb="base-input"] {
        background-color: white !important;
    }
    div[data-baseweb="select"] div[data-baseweb="base-input"] input {
        color: black !important; /* Color del texto dentro del selectbox */
    }

    div[data-baseweb="input"] > div {
        color: black !important; /* Asegura el color del texto */
        background-color: white !important; /* Fondo blanco */
        border: 1px solid #FFB7C5 !important; /* Borde rosa sakura */
        border-radius: 5px; /* Bordes ligeramente redondeados */
    }
    /* Estilo para el input interno del text_input */
    div[data-baseweb="input"] input {
        color: black !important; /* Color del texto dentro del text_input */
    }
    
    /* Estilos para las opciones desplegables del selectbox */
    div[data-baseweb="popover"] div[role="listbox"] {
        background-color: white !important; /* Fondo blanco para el desplegable */
        border: 1px solid #FFB7C5 !important; /* Borde rosa sakura para el desplegable */
    }
    div[data-baseweb="popover"] div[role="option"] {
        color: black !important; /* Texto de las opciones en negro */
    }
    div[data-baseweb="popover"] div[role="option"]:hover {
        background-color: #FFF0F5 !important; /* Rosa muy claro al pasar el ratón */
    }

    /* Target the main value and label of st.metric to be black */
    .stMetric [data-testid="stMetricValue"], .stMetric [data-testid="stMetricLabel"] {
        color: black !important;
    }

    /* Estilo para la barra superior usando data-testid, ahora color sakura más rojizo */
    [data-testid="stHeader"] {
        background-color: #FFB6C1 !important; /* Color sakura más rojizo */
    }

</style>
    """,
    unsafe_allow_html=True
)
# Inicialización de pytrends(google trends)
pytrends = TrendReq(hl='en-US', tz=360)

# Configuración de la página
st.set_page_config(
    page_title="Popularidad mundial",
    layout="wide"
)

animes_populares = [
    "Naruto", "One Piece", "Attack on Titan", "Demon Slayer", "Jujutsu Kaisen",
    "Bleach", "Dragon Ball", "My Hero Academia", "Death Note", "Fullmetal Alchemist",
    "Spy x Family", "Chainsaw Man", "Tokyo Ghoul", "Sword Art Online", "Black Clover",
    "Hunter x Hunter", "Fairy Tail", "JoJo's Bizarre Adventure", "Haikyuu!!", "Code Geass"
]

st.title("Popularidad Global de Animes ")

st.markdown("---") 

# mostrar/ocultar secciones
if "mostrar_lista" not in st.session_state:
    st.session_state.mostrar_lista = False
if "mostrar_texto" not in st.session_state:
    st.session_state.mostrar_texto = False

col_buttons, col_spacer, col_image = st.columns([1, 0.5, 1.5]) 

with col_buttons:
    st.write("")
    st.write("")
    if st.button("Mostrar / Ocultar busqueda por lista", use_container_width=True):
        st.session_state.mostrar_lista = not st.session_state.mostrar_lista
    st.write("") 
    if st.button("Mostrar / Ocultar busqueda por texto libre", use_container_width=True):
        st.session_state.mostrar_texto = not st.session_state.mostrar_texto

with col_spacer:
    st.write("") 

with col_image:
     st.image("mangas.jpg", caption="", width=500)

# Widgets en la barra lateral 
st.sidebar.header("Opciones de Visualización")

# Slider para seleccionar el número de países a mostrar 
num_paises_top = st.sidebar.slider(
    "Numero de paises en el Top",
    min_value=5,
    max_value=100,
    value=20,
    step=5,
    key="sidebar_num_paises_top"
)

# Multiselect para seleccionar años 
selected_years = []

def mostrar_resultados(busqueda, num_paises_top_sidebar, selected_years_sidebar):
    if busqueda:
        st.write(f"datos de Google Trends usando pytrends para **{busqueda}**")
        try:
            with st.spinner('Obteniendo datos'):
                pytrends.build_payload([busqueda], cat=0, timeframe='today 5-y', geo='', gprop='')
                df_region = pytrends.interest_by_region(resolution='COUNTRY')
                df_tiempo = pytrends.interest_over_time()

            if df_region.empty and df_tiempo.empty:
                st.warning(f"No hay suficientes datos para '{busqueda}' en el periodo seleccionado.")
                return

            # --- Popularidad por Región (Datos) ---
            if not df_region.empty:
                df_region["País"] = df_region.index
                df_region = df_region.reset_index(drop=True)
                df_region = df_region.rename(columns={busqueda: "Popularidad (%)"})

                actual_num_paises_top = min(num_paises_top_sidebar, len(df_region))
                if actual_num_paises_top != num_paises_top_sidebar:
                    st.sidebar.info(f"Ajustando Top N a {actual_num_paises_top} ya que hay menos países con datos.")

                # --- Gráfico de Mapa Mundial ---
                st.subheader(f"Mapa mundial de interes (Interes para Top {actual_num_paises_top} paises)")
                
                # Codigos de colores similares a arbol de cerezo
                pink_color_scale = [
                    '#FFE5EE',  # Rosa muy claro 
                    '#FFC0CB',  # Rosa Sakura original
                    '#FFB6C1',  # Rosa más claro
                    '#FF69B4',  # Rosa fuerte
                    '#FF1493',  # Rosa profundo
                    '#C71585',  # Rojo violeta medio
                    '#8B008B'   # Magenta oscuro 
                ]

                # Asegurarse de que el dataframe usado para el mapa contiene suficientes filas
                df_map_data = df_region.sort_values("Popularidad (%)", ascending=False).head(actual_num_paises_top)
                
                fig_map = px.choropleth(
                    df_map_data,
                    locations="País",
                    locationmode="country names",
                    color="Popularidad (%)",
                    hover_name="País",
                    color_continuous_scale=pink_color_scale,  # CAMBIADO a la escala de rosas personalizada
                    title=f"Interes mundial de '{busqueda}'"
                )
                fig_map.update_layout(
                    template="simple_white",
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(color="black"),
                    title_font=dict(color="black"),
                    coloraxis_colorbar=dict(title_font=dict(color="black"), tickfont=dict(color="black")),
                    hoverlabel=dict(
                        bgcolor="#F08080",  
                        font=dict(color="white") 
                    )
                )
                st.plotly_chart(fig_map, use_container_width=True)

                # Gráfico de Barras
                st.subheader(f"Grafico de barras (Top {actual_num_paises_top} paises)")
                fig_bar = px.bar(
                    df_map_data, # datos del top N
                    x="País", y="Popularidad (%)",
                    title=f"Top {actual_num_paises_top} paises por popularidad de '{busqueda}'",
                    labels={"Popularidad (%)": "Popularidad (%)", "País": "País"},
                    template="simple_white",  
                    color_discrete_sequence=["#FFB7C5"]  
                )
                fig_bar.update_layout(
                    template="simple_white",
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(color="black"),
                    title_font=dict(color="black"),
                    xaxis=dict(
                        color="black",
                        title_font=dict(color="black"),
                        tickfont=dict(color="black")
                    ),
                    yaxis=dict(
                        color="black",
                        title_font=dict(color="black"),
                        tickfont=dict(color="black")
                    ),
                    hoverlabel=dict(
                        bgcolor="#F08080", 
                        font=dict(color="white") 
                    )
                )
                st.plotly_chart(fig_bar, use_container_width=True)

                # tabla por pais
                st.markdown("---")
                with st.expander("Mostrar Tabla de Popularidad"):
                    st.dataframe(df_region, use_container_width=True)
                
            else:
                st.warning(f"No hay datos de popularidad para '{busqueda}'.")

            # Evolución Temporal
            if not df_tiempo.empty:
                if 'isPartial' in df_tiempo.columns:
                    df_tiempo = df_tiempo.drop(columns=['isPartial'])

                df_tiempo['year'] = df_tiempo.index.year
                all_years = sorted(df_tiempo['year'].unique())

                if f"multi_year_{busqueda}" not in st.session_state or st.session_state[f"multi_year_{busqueda}_options"] != all_years:
                    st.session_state[f"multi_year_{busqueda}_options"] = all_years
                    st.session_state[f"multi_year_{busqueda}_default"] = all_years

                selected_years_sidebar = st.sidebar.multiselect(
                    "Selecciona los años:",
                    options=st.session_state[f"multi_year_{busqueda}_options"],
                    default=st.session_state[f"multi_year_{busqueda}_default"],
                    key=f"multi_year_{busqueda}"
                )

                st.subheader("Evolucion temporal de la popularidad")

                filtered_df_tiempo = pd.DataFrame()
                chart_title_suffix = ""

                if selected_years_sidebar:
                    filtered_df_tiempo = df_tiempo[df_tiempo['year'].isin(selected_years_sidebar)]
                    if len(selected_years_sidebar) == 1:
                        chart_title_suffix = f" en {selected_years_sidebar[0]}"
                    else:
                        chart_title_suffix = f" ({min(selected_years_sidebar)}-{max(selected_years_sidebar)})"
                else:
                    st.info("Por favor, selecciona al menos un año para ver la evolución.")
                    return

                if not filtered_df_tiempo.empty:
                    fig_line_time = px.line(
                        filtered_df_tiempo,
                        y=busqueda,
                        labels={busqueda: "Popularidad (%)", "date": "Fecha"},
                        title=f"Evolución de la popularidad de '{busqueda}'{chart_title_suffix}",
                        template="simple_white",  
                        line_shape="linear",
                        color_discrete_sequence=["#FFB7C5"]  
                    )
                    fig_line_time.update_layout(
                        template="simple_white",
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        font=dict(color="black"),
                        title_font=dict(color="black"),
                        xaxis=dict(
                            color="black",
                            title_font=dict(color="black"),
                            tickfont=dict(color="black")
                        ),
                        yaxis=dict(
                            color="black",
                            title_font=dict(color="black"),
                            tickfont=dict(color="black")
                        ),
                        hoverlabel=dict(
                            bgcolor="#F08080",  
                            font=dict(color="white") 
                        )
                    )
                    st.plotly_chart(fig_line_time, use_container_width=True)
                else:
                    st.warning(f"No hay datos para los años seleccionados de '{busqueda}'.")
            else:
                st.warning(f"No hay datos de evolución temporal para '{busqueda}'.")

        except Exception as e:
            st.error(f"Error al consultar Google Trends para '{busqueda}': {e}")
            st.info("Asegúrate de que el término de búsqueda sea válido y ten paciencia, a veces Google Trends tiene límites de consulta.")

st.markdown("---")
if st.session_state.mostrar_lista:
    st.markdown("---")
    anime = st.selectbox("Selecciona un anime:", sorted(animes_populares), key="select_anime_list")
    mostrar_resultados(anime, num_paises_top, selected_years)

if st.session_state.mostrar_texto:
    st.markdown("---")
    busqueda_libre = st.text_input("Escribe el término a buscar:", key="text_input_free")
    if busqueda_libre:
        mostrar_resultados(busqueda_libre, num_paises_top, selected_years)