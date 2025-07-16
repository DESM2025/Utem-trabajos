import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Inicializar el estado de la sesión 
if 'show_charts_manga' not in st.session_state:
    st.session_state.show_charts_manga = False
if 'show_filtered_data_manga' not in st.session_state:
    st.session_state.show_filtered_data_manga = False

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

# Paleta para gráficos continuos 
SAKURA_CONTINUOUS_PALETTE = [
    '#FFE5EE',  # Rosa muy claro 
    '#FFB6C1',  # Rosa más claro
    '#FF8FAB',  # Rosa intermedio
    '#FF6F91',  # Rosa fuerte
    '#FF1493'   # Rosa profundo
]

# # coonfigurar colores de la pagina
st.markdown(
    """
<style>
    /* Fondo principal: Blanco */
    .stApp {
        background-color: #FFFFFF;
        color: black; /* Texto general en el área principal a negro */
    }

    /* barra lateral rojo */
    /* Apunta a la barra lateral principal */
    .stSidebar {
        background-color: #BC002D !important; /* Color rojo de la bandera, ¡FORZADO! */
    }

    /* Asegurarse de que TODOS los elementos de texto dentro de la barra lateral sean blancos */
    .stSidebar * {
        color: white !important;
    }

    /* Estilos para elementos interactivos en la barra lateral */
    .stSidebar .stButton > button {
        color: white !important;
        border: 1px solid white !important;
        background-color: #BC002D !important; /* Asegura el fondo del botón en rojo */
    }
    .stSidebar .stButton > button:hover {
        background-color: #A00020 !important; 
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
    /* Asegurar los números del slider en blanco */
    .stSidebar .stSlider [data-testid="stTickValue"],
    .stSidebar .stSlider [data-testid="stRelativeTickValue"] {
        color: white !important;
    }

    /* Estilos para el título principal y subtítulos en el área de contenido (fondo blanco) */
    h1, h2, h3, h4, h5, h6 {
        color: black; /* Títulos a negro */
    }

    /* Líneas divisorias cerezo */
    hr {
        border-top: 1px solid #FFC0CB; 
    }

    /* Ajustes para botones en el área de contenido principal */
    .stButton>button {
        color: black;
        border: 1px solid #BC002D; 
        background-color: #F0F0F0;
    }
    .stButton>button:hover {
        background-color: #e0e0e0;
    }

    /* Ajustes para etiquetas de widgets en el área de contenido principal */
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

    /* Ajuste para el texto de advertencia (st.warning) y otros mensajes */
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

    /* Asegurar que el texto de las opciones en los selectbox y text_inputs se vea */
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
        background-color: #FFB6C1 !important; 
    }

</style>
    """,
    unsafe_allow_html=True
)

def normalize_column(series):
    """Normalizar una serie de datos entre 0 y 1"""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - min_val) / (max_val - min_val)

# Configuración de la página
st.set_page_config(
    page_title="Analisis top 500 Mangas MyanimeList",
    layout="wide"
)

# Título principal
st.title("Los 500 mangas mejor puntuados en MyAnimeList")

# Cargar datos
@st.cache_data
def load_data():
    # Ruta del archivo 
    file_path = r"F:\U\visualizacion\final\myanimelist_top500_manga.csv"
    
    try:
        df = pd.read_csv(file_path)
        
        # Función para limpiar números 
        def clean_numeric_improved(series):
            """Limpiar números que pueden tener comas como separadores de miles"""
            return pd.to_numeric(
                series.astype(str).str.replace(',', '').str.replace(' ', ''), 
                errors='coerce'
            )
        
        # Limpiar y convertir columnas numéricas según la estructura real
        df['ranking'] = clean_numeric_improved(df['ranking'])
        df['score'] = clean_numeric_improved(df['score'])
        df['ranked'] = clean_numeric_improved(df['ranked'])
        df['popularity'] = clean_numeric_improved(df['popularity'])
        df['members'] = clean_numeric_improved(df['members'])
        df['volumenes'] = clean_numeric_improved(df['volumenes'])
        df['capitulos'] = clean_numeric_improved(df['capitulos'])
        
        # Análisis de datos faltantes
        st.subheader("Análisis de Datos")
        # Sustitución de st.markdown por el estilo de cerezo
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**Información por columna:**")
            for col in df.columns:
                non_null = df[col].notna().sum()
                st.write(f"- **{col}**: {non_null}/{len(df)} válidos ({non_null/len(df)*100:.1f}%)")
        
        with col2:
            st.write("**Muestra de datos**")
            # Mostrar los primeros 10 datos
            st.dataframe(df.head(10))
        
        # Solo mantener filas con score válido 
        df_original_len = len(df)
        df = df.dropna(subset=['score'])
        
        if len(df) < df_original_len:
            st.info(f"Filas con score válido: {len(df)} de {df_original_len}")
        
        # Llenar valores faltantes con 0 para columnas numéricas
        numeric_cols = ['ranking', 'ranked', 'popularity', 'members', 'volumenes', 'capitulos']
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

# Sustitución de st.markdown por el estilo de cerezo
st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

if df is not None and len(df) > 0:
    # Sidebar con filtros
    st.sidebar.header("Filtros Interactivos")
    
    # Multiselect para status del manga
    status_disponibles = df['status'].dropna().unique()
    
    status_disponibles_list = list(status_disponibles)
    if 'Discontinued' in status_disponibles_list:
        status_disponibles_list.remove('Discontinued')
    
    # Ajustar la selección por defecto a los 3 primeros statuses disponibles 
    default_status = status_disponibles_list[:3] if len(status_disponibles_list) >= 3 else status_disponibles_list
    
    status_seleccionados = st.sidebar.multiselect(
        "Status del manga",
        options=status_disponibles_list,
        default=default_status
    )
    
    # Slider para rango de score
    min_score, max_score = st.sidebar.slider(
        "Rango de puntuacion",
        min_value=float(df['score'].min()),
        max_value=float(df['score'].max()),
        value=(float(df['score'].min()), float(df['score'].max())),
        step=0.1
    )
    
    # Selectbox para demografía
    demografias_disponibles = ['Todas'] + list(df['demografia'].dropna().unique())
    demografia_seleccionada = st.sidebar.selectbox(
        "Demografia",
        options=demografias_disponibles,
        index=0
    )
    
    # Slider para número mínimo de miembros
    members_min_safe = int(df['members'].min()) if df['members'].notna().any() else 0
    members_max_safe = int(df['members'].max()) if df['members'].notna().any() else 1000000
    
    min_members = st.sidebar.slider(
        "Numero minimo de miembros",
        min_value=members_min_safe,
        max_value=members_max_safe,
        value=members_min_safe,
        step=10000,
        format="%d"
    )
    
    # Slider para ranking máximo (menor número = mejor ranking)
    ranking_max = st.sidebar.slider(
        "Ranking maximo",
        min_value=1,
        max_value=int(df['ranking'].max()) if df['ranking'].notna().any() else 500,
        value=100,
        step=10,
        help="Mostrar solo los top X mangas por ranking"
    )
    
    # Slider para número mínimo de capítulos
    if df['capitulos'].notna().any() and df['capitulos'].max() > 0:
        capitulos_max_safe = int(df['capitulos'].max())
        min_capitulos = st.sidebar.slider(
            "Numero minimo de capitulos",
            min_value=0,
            max_value=capitulos_max_safe,
            value=0,
            step=10,
            format="%d"
        )
    else:
        min_capitulos = 0
    
    # Aplicar filtros con verificación de datos válidos
    if len(status_seleccionados) == 0:
        st.warning("Selecciona al menos un status de manga.")
        st.stop()
    
    df_filtrado = df[
        (df['status'].isin(status_seleccionados)) &
        (df['score'] >= min_score) &
        (df['score'] <= max_score) &
        (df['members'] >= min_members) &
        (df['ranking'] <= ranking_max) &
        (df['capitulos'] >= min_capitulos)
    ]
    
    if demografia_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['demografia'] == demografia_seleccionada]
    
    if len(df_filtrado) == 0:
        # Se muestra la advertencia si no hay datos que coincidan con los filtros
        st.warning("No hay datos que coincidan con los filtros seleccionados. Ajusta los filtros.")
        st.stop()
    
    # Métricas principales con datos reales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Mangas", len(df_filtrado))
    with col2:
        avg_score = df_filtrado['score'].mean()
        st.metric("Score Promedio", f"{avg_score:.2f}")
    with col3:
        avg_members = df_filtrado['members'].mean()
        st.metric("Miembros Promedio", f"{avg_members:,.0f}")
    with col4:
        avg_capitulos = df_filtrado['capitulos'].mean()
        st.metric("Capítulos Promedio", f"{avg_capitulos:.0f}")
    
    # Sección de gráficos por botón 
    st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

    # Botón para mostrar gráficos
    if st.button("Mostrar Gráficos de Análisis"):
        st.session_state.show_charts_manga = not st.session_state.show_charts_manga

    if st.session_state.show_charts_manga:

        # Definir un color de texto común para los gráficos 
        PLOT_TEXT_COLOR = 'black'
        PLOT_GRID_COLOR = '#E0E0E0' 
        
        # Definir colores para el hoverlabel 
        HOVERLABEL_BG_COLOR = '#F08080' 
        HOVERLABEL_FONT_COLOR = 'white' 
        
        # Layout en dos columnas
        col1, col2 = st.columns(2)

        with col1:
            # Scatter Plot Score vs Popularidad
            st.subheader("Relacion entre puntuacion y Popularidad")
            
            fig_scatter = px.scatter(
                df_filtrado,
                x='members',
                y='score',
                size='capitulos', # tamaño basado en capítulos
                color='status', # color por status
                hover_data=['nombre', 'volumenes', 'demografia', 'ranking'],
                title="Puntuacion vs cantidad de miembros individual",
                labels={'members': 'Número de Miembros', 'score': 'Score'},
                size_max=50,
                # usar paleta de colores cerezo
                color_discrete_sequence=SAKURA_DISCRETE_PALETTE
            )
            fig_scatter.update_layout(
                height=500,
                title_font_color=PLOT_TEXT_COLOR, 
                xaxis_title="Numero de Miembros",
                yaxis_title="Puntuacion",
                plot_bgcolor='rgba(0,0,0,0)', # Fondo del plot transparente
                paper_bgcolor='rgba(0,0,0,0)', # Fondo  transparente
                font_color=PLOT_TEXT_COLOR, # Color general del texto del gráfico 
                xaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR), # Números del eje X
                    title_font=dict(color=PLOT_TEXT_COLOR), # Título del eje X
                    gridcolor=PLOT_GRID_COLOR # Color de la cuadrícula
                ),
                yaxis=dict(
                    tickfont=dict(color=PLOT_TEXT_COLOR), # Números del eje Y
                    title_font=dict(color=PLOT_TEXT_COLOR), # Título del eje Y
                    gridcolor=PLOT_GRID_COLOR
                ),
                legend=dict(
                    font=dict(color=PLOT_TEXT_COLOR) # Texto de la leyenda
                ),
                # TOOLTIP 
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR, 
                    font_color=HOVERLABEL_FONT_COLOR 
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Histograma de Scores
            st.subheader("Distribucion de puntuacion por estado")
            fig_hist = px.histogram(
                df_filtrado,
                x='score',
                color='status', 
                title="Distribucion de puntuacion por Status", #puntuacion
                labels={'score': 'puntuacion', 'count': 'Frecuencia'},
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
                # TOOLTIP 
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR, 
                    font_color=HOVERLABEL_FONT_COLOR 
                )
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Bar Chart Top 10 por Score
            st.subheader("Primeros 10 mangas mejor puntuados")
            if len(df_filtrado) > 0:
                top_mangas = df_filtrado.nlargest(10, 'score')
                
                fig_bar = px.bar(
                    top_mangas,
                    x='score',
                    y='nombre',
                    color='members', # color basado en miembros
                    orientation='h', # orientación horizontal
                    title="Top 10 Mangas Mejor Puntuados", #puntuacion
                    labels={'score': 'Score', 'nombre': 'Manga', 'members': 'Miembros'},
                    text='score',
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
                    xaxis_title="puntuacion",
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
                    # TOOLTIP
                    hoverlabel=dict(
                        bgcolor=HOVERLABEL_BG_COLOR, 
                        font_color=HOVERLABEL_FONT_COLOR 
                    )
                )
                fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside',
                                        textfont=dict(color=PLOT_TEXT_COLOR)) 
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Box Plot Scores por Demografía
            st.subheader("Distribucion de miembros por Demografia")
            if len(df_filtrado['demografia'].dropna()) > 0:
                fig_box = px.box(
                    df_filtrado.dropna(subset=['demografia']),
                    x='demografia',
                    y='members',
                    color='demografia', 
                    title="Box Plot de miembros por Demografia",
                    labels={'demografia': 'Demografia', 'members': 'miembros'},
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
                    # TOOLTIP 
                    hoverlabel=dict(
                        bgcolor=HOVERLABEL_BG_COLOR, 
                        font_color=HOVERLABEL_FONT_COLOR 
                    )
                )
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("No hay datos de demografía suficientes para el box plot")
        
        # Sustitución de st.markdown por el estilo de cerezo
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

        # Heatmap de Correlación
        st.subheader("Analisis de Correlacion entre Variables")
        
        # Incluir todas las columnas numéricas disponibles
        variables_numericas = ['ranking', 'score', 'ranked', 'popularity', 'members', 'volumenes', 'capitulos']
        # Filtrar solo las que tienen datos
        vars_con_datos = [var for var in variables_numericas if var in df_filtrado.columns and df_filtrado[var].notna().any()]
        
        if len(vars_con_datos) >= 2:
            df_correlacion = df_filtrado[vars_con_datos].corr(numeric_only=True) 
            
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
                # TOOLTIP
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR, 
                    font_color=HOVERLABEL_FONT_COLOR 
                )
            )
            # configurar el color del texto de las anotaciones del heatmap
            fig_heatmap.update_traces(textfont=dict(color=PLOT_TEXT_COLOR))
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("No hay suficientes variables numéricas para correlación")
        
        # Sustitución de st.markdown por el estilo de cerezo
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart Distribución por Demografía
            st.subheader("Distribucion por Demografia")
            if len(df_filtrado['demografia'].dropna()) > 0:
                demo_counts = df_filtrado['demografia'].value_counts()
                fig_pie = px.pie(
                    values=demo_counts.values,
                    names=demo_counts.index,
                    title="Distribucion por Demografía",
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
                    # TOOLTIP
                    hoverlabel=dict(
                        bgcolor=HOVERLABEL_BG_COLOR, 
                        font_color=HOVERLABEL_FONT_COLOR 
                    )
                )
                # Para el texto dentro del pie chart
                fig_pie.update_traces(textfont=dict(color=PLOT_TEXT_COLOR))
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No hay datos de demografía suficientes")
        
        with col2:
            # Pie Chart Distribución por Status
            st.subheader("Distribucion por estado del manga")
            
            status_counts = df_filtrado['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            
            if len(status_counts) > 0:
                fig_pie_status = px.pie(
                    status_counts,
                    values='count',
                    names='status',
                    title="Distribucion",
                    # usar paleta de colores cerezo
                    color_discrete_sequence=SAKURA_DISCRETE_PALETTE
                )
                
                # Configuración del layout para el gráfico de pastel
                fig_pie_status.update_layout(
                    height=400,
                    title_font_color=PLOT_TEXT_COLOR,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color=PLOT_TEXT_COLOR,
                    legend=dict(
                        font=dict(color=PLOT_TEXT_COLOR)
                    ),
                    # tooltip
                    hoverlabel=dict(
                        bgcolor=HOVERLABEL_BG_COLOR,
                        font_color=HOVERLABEL_FONT_COLOR
                    )
                )
                
                fig_pie_status.update_traces(
                    textfont=dict(color=PLOT_TEXT_COLOR),
                    textposition='inside',
                    marker=dict(line=dict(color='#ffffff', width=2)),
                    textinfo='value'
                )
                
                st.plotly_chart(fig_pie_status, use_container_width=True)
            else:
                st.info("No hay suficientes datos para el gráfico de pastel de status")
        
    # datos filtrados 
    # Sustitución de st.markdown por el estilo de cerezo
    st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

    st.subheader("Datos Filtrados listos para descargar")

    # Botón para mostrar/ocultar la tabla de datos
    if st.button("Mostrar Tabla de Datos Filtrados"):
        st.session_state.show_filtered_data_manga = not st.session_state.show_filtered_data_manga

    if st.session_state.show_filtered_data_manga:
        
        # Checkbox para mostrar todas las columnas
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"Mostrando {len(df_filtrado)} mangas de {len(df)} totales")
        with col2:
            mostrar_todas = st.checkbox("Mostrar todas las columnas", value=False)
        
        if mostrar_todas:
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            columnas_principales = ['ranking', 'nombre', 'score', 'status', 'demografia', 'members', 'volumenes', 'capitulos']
            # Verificar qué columnas existen realmente
            columnas_existentes = [col for col in columnas_principales if col in df_filtrado.columns]
            st.dataframe(df_filtrado.loc[:, columnas_existentes], use_container_width=True) # Use .loc for safer indexing
else:
    st.error("No se pudieron cargar los datos o el archivo está vacío. Verifica que el archivo CSV esté disponible y contenga datos válidos.")
    st.info("Asegúrate de que el archivo 'myanimelist_top500_manga.csv' esté en el directorio correcto y tenga el formato esperado.")