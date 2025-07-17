import streamlit as st

# Configuración de la pagina
st.set_page_config(
    page_title="Aplicación de Análisis de Animes",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* Fondo principal: Blanco */
    .stApp {
        background-color: #FFFFFF;
        color: black; /* Texto general en el área principal a negro */
    }

    /* Fondo de la barra lateral: Rojo (Bandera de Japón) */
    .stSidebar {
        background-color: #BC002D;
    }
    /* Asegurarse de que el texto en la barra lateral sea blanco */
    .stSidebar * {
        color: white !important;
    }

    /* Estilos específicos para elementos interactivos en la barra lateral */
    .stSidebar .stButton > button {
        color: white !important;
        border: 1px solid white !important;
    }
    .stSidebar .stSelectbox > label,
    .stSidebar .stTextInput > label,
    .stSidebar .stSlider > label,
    .stSidebar .stMultiSelect > label {
        color: white !important;
    }
    /* Asegurar el texto en selectbox/input dentro del sidebar */
    .stSidebar div[data-baseweb="select"] > div,
    .stSidebar div[data-baseweb="input"] > div {
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

    /* Asegurar que el texto de las opciones en los selectbox y text_inputs en el área principal se vea */
    div[data-baseweb="select"] > div {
        color: black;
    }
    div[data-baseweb="input"] > div {
        color: black;
    }

    /* Estilo para la barra superior usando data-testid, ahora color sakura más rojizo */
    [data-testid="stHeader"] {
        background-color: #FFB6C1 !important; /* Color sakura más rojizo */
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.title("Popularidad y datos estadísticos del mundo del Anime y Manga")

st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    st.image("arbol2.jpg", caption="", width=700) # 

st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

st.write("Diego Silva;Pablo ibañez")
