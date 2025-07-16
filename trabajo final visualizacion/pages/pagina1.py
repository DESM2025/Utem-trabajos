import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Inicializar para controlar la visibilidad de los gráficos y la tabla
if 'show_charts' not in st.session_state:
    st.session_state.show_charts = False
if 'show_filtered_data' not in st.session_state:
    st.session_state.show_filtered_data = False

def normalize_column(series):
    """Normalizar una serie de datos entre 0 y 1"""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - min_val) / (max_val - min_val)

# Configuración de la página
st.set_page_config(
    page_title="Analisis top 500 Animes MyanimeList",
    layout="wide"
)

# Codigos de colores similares a arbol de cerezo
# Paleta para gráficos discretos 
SAKURA_DISCRETE_PALETTE = [
    '#FF69B4', # Rosa Caliente 
    '#FF1493', # Rosa Profundo 
    '#FFAEC9', # Rosa intermedio
    '#FFC0CB', # Rosa Sakura claro
    '#FF8FAB', # Cuarzo Rosa
    '#C71585', # Rojo Violeta Medio
    '#8B008B', # Magenta Oscuro
    '#FF6F91'  # Rosa Brillante
]
# Paleta para graficos continuos 
SAKURA_CONTINUOUS_PALETTE = [
    '#FFE5EE',  # Rosa muy claro 
    '#FFB6C1',  # Rosa más claro
    '#FF8FAB',  # Rosa intermedio
    '#FF6F91',  # Rosa fuerte
    '#FF1493'  # Rosa profundo
]

# coonfigurar colores de la pagina
st.markdown(
    """
<style>
    /* Fondo principal Blanco */
    .stApp {
        background-color: #FFFFFF;
        color: black; /* Texto general a negro */
    }

    /* barra lateral rojo */
    /* Apunta a la barra lateral principal */
    .stSidebar {
        background-color: #BC002D !important; /* Color rojo de la bandera */
    }

    /* todos los elementos de texto dentro de la barra lateral  blancos */
    .stSidebar * {
        color: white !important;
    }

    /* Estilos para elementos interactivos en la barra lateral */
    .stSidebar .stButton > button {
        color: white !important;
        border: 1px solid white !important;
        background-color: #BC002D !important; /* fondo del botón en rojo */
    }
    .stSidebar .stButton > button:hover {
        background-color: #A00020 !important; /* Un rojo un poco más oscuro */
    }

    .stSidebar label { /* Etiquetas de los widgets en el sidebar */
        color: white !important;
    }

    /* Asegurar el texto y el color de fondo para selectbox/input dentro del sidebar */
    .stSidebar div[data-baseweb="select"] > div {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.2) !important; 
    }
    .stSidebar div[data-baseweb="input"] > div {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.2) !important; 
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

    /* Asegurar que el texto de las opciones en los selectbox y text_inputs en el área principal se vea */
    div[data-baseweb="select"] > div {
        color: black;
    }
    div[data-baseweb="input"] > div {
        color: black;
    }

    /* st.metric que muestran los números */
    /* Target the main value and label of st.metric to be black */
    .stMetric [data-testid="stMetricValue"], .stMetric [data-testid="stMetricLabel"] {
        color: black !important;
    }


    /* Estilo para la barra superior */
    [data-testid="stHeader"] {
        background-color: #FFB6C1 !important; /* Color sakura más rojizo */
    }

</style>
    """,
    unsafe_allow_html=True
)

# Título principal
st.title("Los 500 animes mejor puntuados en MyAnimeList")

# Cargar datos
@st.cache_data
def load_data():
    # Ruta del archivo 
    file_path = r"F:\U\visualizacion\final\myanimelist_top500.csv" 

    try:
        df = pd.read_csv(file_path)

        # Función para limpiar numeros
        def clean_numeric_improved(series):
            """Limpiar números que pueden tener comas como separadores de miles"""
            return pd.to_numeric(
                series.astype(str).str.replace(',', '').str.replace(' ', ''),
                errors='coerce'
            )

        # Limpiar y convertir columnas numéricas según la estructura 
        df['ranking'] = clean_numeric_improved(df['ranking'])
        df['puntuacion'] = clean_numeric_improved(df['puntuacion'])
        df['episodios'] = clean_numeric_improved(df['episodios'])
        df['miembros'] = clean_numeric_improved(df['miembros'])
        df['favoritos'] = clean_numeric_improved(df['favoritos'])

        # Análisis de Datos (Muestra de datos)
        st.subheader("Análisis de Datos")
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

        # Usar st.columns([1, 2]) para hacer la segunda columna más ancha
        col1, col2 = st.columns([1, 2])

        with col1:
            st.write("**Informacion por columna**")
            for col in df.columns:
                non_null = df[col].notna().sum()
                st.write(f"- **{col}**: {non_null}/{len(df)} válidos ({non_null/len(df)*100:.1f}%)")

        with col2:
            st.write("**Muestra de datos**")
            st.dataframe(df.head(10)) 

        # Solo mantener filas con puntuación válida 
        df_original_len = len(df)
        df = df.dropna(subset=['puntuacion'])

        if len(df) < df_original_len:
            st.info(f"ℹFilas con puntuación válida: {len(df)} de {df_original_len}")

        # Llenar valores faltantes con 0 para columnas numéricas
        numeric_cols = ['ranking', 'episodios', 'miembros', 'favoritos']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)

        return df

    except FileNotFoundError:
        st.error(f"No se encontró el archivo en la ruta: {file_path}")
        return None
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        st.write(f"Detalles del error: {type(e).__name__}")
        return None

df = load_data()

st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

if df is not None and len(df) > 0:
    # Sidebar con filtros
    st.sidebar.header("Filtros aplicables")

    # Multiselect para tipos de anime
    tipos_disponibles = df['tipo'].unique()
    tipos_seleccionados = st.sidebar.multiselect(
        "Tipo de anime",
        options=tipos_disponibles,
        default=tipos_disponibles[:3] if len(tipos_disponibles) >= 3 else tipos_disponibles
    )

    # Slider para rango de puntuación
    min_score, max_score = st.sidebar.slider(
        "Rango de puntuacion",
        min_value=float(df['puntuacion'].min()),
        max_value=float(df['puntuacion'].max()),
        value=(float(df['puntuacion'].min()), float(df['puntuacion'].max())),
        step=0.1
    )

    # Selectbox para demografía
    demografias_disponibles = ['Todas'] + list(df['demografia'].dropna().unique())
    demografia_seleccionada = st.sidebar.selectbox(
        "Demografía",
        options=demografias_disponibles,
        index=0
    )

    # Slider para número mínimo de miembros
    miembros_min_safe = int(df['miembros'].min()) if df['miembros'].notna().any() else 0
    miembros_max_safe = int(df['miembros'].max()) if df['miembros'].notna().any() else 1000000

    min_miembros = st.sidebar.slider(
        "Numero minimo de miembros",
        min_value=miembros_min_safe,
        max_value=miembros_max_safe,
        value=miembros_min_safe,
        step=50000,
        format="%d"
    )

    # Slider para número mínimo de favoritos
    favoritos_min_safe = int(df['favoritos'].min()) if df['favoritos'].notna().any() else 0
    favoritos_max_safe = int(df['favoritos'].max()) if df['favoritos'].notna().any() else 100000

    min_favoritos = st.sidebar.slider(
        "Numero minimo de favoritos:",
        min_value=favoritos_min_safe,
        max_value=favoritos_max_safe,
        value=favoritos_min_safe,
        step=5000,
        format="%d"
    )

    # Aplicar filtros con verificación de datos válidos
    if len(tipos_seleccionados) == 0:
        st.warning("Selecciona al menos un tipo de anime.")
        st.stop()

    df_filtrado = df[
        (df['tipo'].isin(tipos_seleccionados)) &
        (df['puntuacion'] >= min_score) &
        (df['puntuacion'] <= max_score) &
        (df['miembros'] >= min_miembros) &
        (df['favoritos'] >= min_favoritos)
    ]

    if demografia_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['demografia'] == demografia_seleccionada]

    if len(df_filtrado) == 0:
        st.warning("No hay datos que coincidan con los filtros seleccionados. Ajusta los filtros.")
        st.stop()

    # Métricas principales con datos reales 
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Animes", len(df_filtrado))
    with col2:
        avg_score = df_filtrado['puntuacion'].mean()
        st.metric("Puntuación Promedio", f"{avg_score:.2f}")
    with col3:
        avg_miembros = df_filtrado['miembros'].mean()
        st.metric("Miembros Promedio", f"{avg_miembros:,.0f}")
    with col4:
        avg_favoritos = df_filtrado['favoritos'].mean()
        st.metric("Favoritos Promedio", f"{avg_favoritos:,.0f}")

    # Sección de gráficos activada por botón
    st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

    # Botón para mostrar/ocultar gráficos
    if st.button("Mostrar Gráficos de Análisis"):
        st.session_state.show_charts = not st.session_state.show_charts
    
    # Mostrar gráficos si es True
    if st.session_state.show_charts:
        
        # Definir un color de texto negro para fondo claro  para los gráficos,
        PLOT_TEXT_COLOR = 'black'
        PLOT_GRID_COLOR = '#E0E0E0' 

        # Definir colores para los tooltip
        HOVERLABEL_BG_COLOR = '#F08080' 
        HOVERLABEL_FONT_COLOR = 'white' 

        # Layout en dos columnas para los primeros 4 gráficos
        col1, col2 = st.columns(2)

        with col1:
            # Scatter Plot Relación entre Puntuación y Popularidad
            st.subheader("Relacion entre Puntuacion y Popularidad")

            fig_scatter = px.scatter(
                df_filtrado,
                x='miembros',
                y='puntuacion',
                size='favoritos', # tamaño basado en favoritos
                color='tipo', # color por tipo
                hover_data=['nombre', 'episodios', 'demografia', 'ranking'],
                title="Puntuacion vs Cantidad de Miembros individual",
                labels={'miembros': 'Número de Miembros', 'puntuacion': 'Puntuación'},
                size_max=50,
                # usar paleta de colores cerezo
                color_discrete_sequence=SAKURA_DISCRETE_PALETTE
            )
            fig_scatter.update_layout(
                height=500,
                title_font_color=PLOT_TEXT_COLOR,
                xaxis_title="Numero de Miembros",
                yaxis_title="Puntuacion",
                plot_bgcolor='rgba(0,0,0,0)', # Fondo transparente
                paper_bgcolor='rgba(0,0,0,0)', # Fondo del papel transparente
                font_color=PLOT_TEXT_COLOR, # Color general del texto del gráfico 
                xaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR), # Números del eje X
                    title_font=dict(color=PLOT_TEXT_COLOR), # Titulo del eje X
                    gridcolor=PLOT_GRID_COLOR # Color de la cuadrícula
                ),
                yaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR), # Números del eje Y
                    title_font=dict(color=PLOT_TEXT_COLOR), # Titulo del eje Y
                    gridcolor=PLOT_GRID_COLOR
                ),
                legend=dict(
                    font=dict(color=PLOT_TEXT_COLOR) 
                ),
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR, 
                    font_color=HOVERLABEL_FONT_COLOR 
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            # Histograma de Puntuaciones
            st.subheader("Distribucion de Clasificacion de edad")
            fig_hist = px.histogram(
                df_filtrado,
                x='rating_edad',
                color='tipo', #color
                title="Distribucion de clasificacion de edad por Tipo de anime",
                labels={'rating_edad': 'rating_edad', 'count': 'Frecuencia'},
                nbins=20,
                # usar paleta de colores cerezo
                color_discrete_sequence=SAKURA_DISCRETE_PALETTE
            )
            fig_hist.update_layout(
                height=400,
                title_font_color=PLOT_TEXT_COLOR,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=PLOT_TEXT_COLOR, # Color general del texto 
                xaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR),
                    title_font=dict(color=PLOT_TEXT_COLOR),
                    gridcolor=PLOT_GRID_COLOR
                ),
                yaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR),
                    title_font=dict(color=PLOT_TEXT_COLOR),
                    gridcolor=PLOT_GRID_COLOR
                ),
                legend=dict(
                    font=dict(color=PLOT_TEXT_COLOR)
                ),
                # Configuración del hoverlabel
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR,
                    font_color=HOVERLABEL_FONT_COLOR
                )
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col2:
            # Bar Chart Top 10 por Puntuacion
            st.subheader("Primeros 10 Animes mejor puntuados")
            if len(df_filtrado) > 0:
                top_animes = df_filtrado.nlargest(10, 'puntuacion')

                fig_bar = px.bar(
                    top_animes,
                    x='puntuacion',
                    y='nombre',
                    color='favoritos', # color basado en favoritos
                    orientation='h', # orientación horizontal
                    title="Top 10 Animes Mejor Puntuados y cantidad de favoritos",
                    labels={'puntuacion': 'Puntuación', 'nombre': 'Anime', 'favoritos': 'Favoritos'},
                    text='puntuacion',
                    # usar paleta de colores cerezo
                    color_continuous_scale=SAKURA_CONTINUOUS_PALETTE
                )
                fig_bar.update_layout(
                    height=500,
                    title_font_color=PLOT_TEXT_COLOR,
                    yaxis={'categoryorder': 'total ascending',
                           'tickfont':dict(color=PLOT_TEXT_COLOR),
                           'title_font':dict(color=PLOT_TEXT_COLOR),
                           'gridcolor':PLOT_GRID_COLOR
                          },
                    xaxis_title="Puntuacion",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color=PLOT_TEXT_COLOR, # Color general del texto 
                    xaxis=dict(
                        tickfont=dict(color=PLOT_TEXT_COLOR),
                        title_font=dict(color=PLOT_TEXT_COLOR),
                        gridcolor=PLOT_GRID_COLOR
                    ),
                    coloraxis_colorbar=dict( 
                        tickfont=dict(color=PLOT_TEXT_COLOR),
                        title_font=dict(color=PLOT_TEXT_COLOR)
                    ),
                    # Configuración del hoverlabel
                    hoverlabel=dict(
                        bgcolor=HOVERLABEL_BG_COLOR,
                        font_color=HOVERLABEL_FONT_COLOR
                    )
                )
                # Asegurar que el texto dentro de las barras también sea negro
                fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside',
                                       textfont=dict(color=PLOT_TEXT_COLOR))
                st.plotly_chart(fig_bar, use_container_width=True)

            # Box Plot Puntuaciones por Tipo
            st.subheader("Distribucion de Puntuaciones por Tipo de anime")
            fig_box = px.box(
                df_filtrado,
                x='tipo',
                y='puntuacion',
                color='tipo', 
                title="Box Plot de Puntuaciones por Tipo de Anime",
                labels={'tipo': 'Tipo de Anime', 'puntuacion': 'Puntuacion'},
                # usar paleta de colores cerezo
                color_discrete_sequence=SAKURA_DISCRETE_PALETTE
            )
            fig_box.update_layout(
                height=400,
                title_font_color=PLOT_TEXT_COLOR,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=PLOT_TEXT_COLOR, # Color general del texto 
                xaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR),
                    title_font=dict(color=PLOT_TEXT_COLOR),
                    gridcolor=PLOT_GRID_COLOR
                ),
                yaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR),
                    title_font=dict(color=PLOT_TEXT_COLOR),
                    gridcolor=PLOT_GRID_COLOR
                ),
                legend=dict(
                    font=dict(color=PLOT_TEXT_COLOR)
                ),
                # Configuración del hoverlabel
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR,
                    font_color=HOVERLABEL_FONT_COLOR
                )
            )
            st.plotly_chart(fig_box, use_container_width=True)

        # Fila completa para visualización adicional
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)
        # Heatmap de Correlacion
        st.subheader("Análisis de Correlación entre Variables")

        # Incluir todas las columnas numericas disponibles
        variables_numericas = ['ranking', 'puntuacion', 'episodios', 'miembros', 'favoritos']
        df_correlacion = df_filtrado[variables_numericas].corr(numeric_only=True) 

        fig_heatmap = px.imshow(
            df_correlacion,
            text_auto=True,
            aspect="auto",
            title="Matriz de Correlacion entre Variables Numericas",
            labels=dict(x="Variables", y="Variables", color="Correlación"),
            # usar paleta de colores cerezo
            color_continuous_scale=SAKURA_CONTINUOUS_PALETTE
        )
        fig_heatmap.update_layout(
            height=500,
            title_font_color=PLOT_TEXT_COLOR,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=PLOT_TEXT_COLOR, # Color general del texto 
            xaxis=dict(
                tickfont=dict(color=PLOT_TEXT_COLOR),
                title_font=dict(color=PLOT_TEXT_COLOR)
            ),
            yaxis=dict(
                tickfont=dict(color=PLOT_TEXT_COLOR),
                title_font=dict(color=PLOT_TEXT_COLOR)
            ),
            coloraxis_colorbar=dict( 
                tickfont=dict(color=PLOT_TEXT_COLOR),
                title_font=dict(color=PLOT_TEXT_COLOR)
            ),
            # Configuración del hoverlabel
            hoverlabel=dict(
                bgcolor=HOVERLABEL_BG_COLOR,
                font_color=HOVERLABEL_FONT_COLOR
            )
        )
        # configurar el color del texto de las anotaciones del heatmap
        fig_heatmap.update_traces(textfont=dict(color=PLOT_TEXT_COLOR))
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Analisis por fuente
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            # Pie Chart Distribución por Fuente
            st.subheader("Distribucion por Fuente de Origen")
            source_counts = df_filtrado['source'].value_counts().head(8)
            fig_pie = px.pie(
                values=source_counts.values,
                names=source_counts.index,
                title="Distribucion por Fuente de origen del anime",
                # usar paleta de colores cerezo
                color_discrete_sequence=SAKURA_DISCRETE_PALETTE
            )
            fig_pie.update_layout(
                height=400,
                title_font_color=PLOT_TEXT_COLOR,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=PLOT_TEXT_COLOR, # Color general del texto 
                legend=dict(
                    font=dict(color=PLOT_TEXT_COLOR)
                ),
                # Configuración del hoverlabel
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR,
                    font_color=HOVERLABEL_FONT_COLOR
                )
            )
            # Para el texto dentro del pie chart
            fig_pie.update_traces(textfont=dict(color=PLOT_TEXT_COLOR))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Sunburst Chart Distribución jerárquica
            st.subheader("Distribucion por Demografia y Tipo de anime")

            df_sunburst = df_filtrado.groupby(['demografia', 'tipo']).size().reset_index(name='count')
            df_sunburst = df_sunburst.query('count > 0')

            if not df_sunburst.empty:
                fig_sunburst = px.sunburst(
                    df_sunburst,
                    path=['demografia', 'tipo'], 
                    values='count',
                    title="Distribución Jerarquica",
                    color='count',
                    # usar paleta de colores cerezo
                    color_continuous_scale=SAKURA_CONTINUOUS_PALETTE
                )
                fig_sunburst.update_layout(
                    height=400,
                    title_font_color=PLOT_TEXT_COLOR,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color=PLOT_TEXT_COLOR, # Color general del texto 
                    coloraxis_colorbar=dict( 
                        tickfont=dict(color=PLOT_TEXT_COLOR),
                        title_font=dict(color=PLOT_TEXT_COLOR)
                    ),
                    # Configuración del hoverlabel
                    hoverlabel=dict(
                        bgcolor=HOVERLABEL_BG_COLOR,
                        font_color=HOVERLABEL_FONT_COLOR
                    )
                )
                # Para el texto dentro del sunburst
                fig_sunburst.update_traces(textfont=dict(color=PLOT_TEXT_COLOR))
                st.plotly_chart(fig_sunburst, use_container_width=True)
            else:
                st.info("No hay suficientes datos para mostrar distribución jerárquica")

    # Tabla de datos filtrados 
    st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)
    
    # Título 
    st.subheader("Datos Filtrados listos para descargar")
    
    # Botón 
    if st.button("Mostrar Tabla de Datos Filtrados"):
        st.session_state.show_filtered_data = not st.session_state.show_filtered_data

    # Mostrar la tabla de datos si el estado es True
    if st.session_state.show_filtered_data:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"Mostrando {len(df_filtrado)} animes de {len(df)} totales")
        with col2:
            mostrar_todas = st.checkbox("Mostrar todas las columnas", value=False)

        if mostrar_todas:
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            columnas_principales = ['ranking', 'nombre', 'puntuacion', 'tipo', 'episodios', 'demografia', 'miembros', 'favoritos']
            columnas_existentes = [col for col in columnas_principales if col in df_filtrado.columns]
            st.dataframe(df_filtrado.loc[:, columnas_existentes], use_container_width=True) 

else: 
    st.error("No se pudieron cargar los datos o el archivo está vacío. Verifica que el archivo CSV esté disponible y contenga datos válidos.")
    st.info("Asegúrate de que el archivo 'myanimelist_top500.csv' esté en el directorio correcto y tenga el formato esperado.")