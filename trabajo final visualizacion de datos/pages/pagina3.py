import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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
    page_title="Analisis de subreddits",
    layout="wide"
)

# Título principal
st.title("Analisis subreddits anime-manga")

# Cargar datos
@st.cache_data
def load_data():
    # Ruta del archivo 
    file_path = r"F:\U\visualizacion\final\posts.csv" 
    
    try:
        df = pd.read_csv(file_path) 
        
        # Función para limpiar números
        def clean_numeric_improved(series):
            """Limpiar números que pueden tener comas como separadores de miles"""
            return pd.to_numeric(
                series.astype(str).str.replace(',', '').str.replace(' ', ''), 
                errors='coerce'
            )
        
        # Limpiar y convertir columnas numéricas
        df['numero_comentarios'] = clean_numeric_improved(df['numero_comentarios']) 
        df['puntaje'] = clean_numeric_improved(df['puntaje']) 
        df['upvotes'] = clean_numeric_improved(df['upvotes']) 
        df['downvotes'] = clean_numeric_improved(df['downvotes']) 
        
        # Convertir fecha a datetime
        df['fecha_post'] = pd.to_datetime(df['fecha_post'], errors='coerce') 
        
        # Crear columnas derivadas para análisis
        df['mes'] = df['fecha_post'].dt.to_period('M').astype(str) 
        df['dia_semana'] = df['fecha_post'].dt.day_name() 
        df['hora'] = df['fecha_post'].dt.hour 
        df['longitud_titulo'] = df['titulo_post'].str.len() 
        df['longitud_texto'] = df['texto_post'].fillna('').str.len() 
        
        # Calcular engagement rate
        df['engagement_rate'] = (df['numero_comentarios'] / (df['puntaje'] + 1)) * 100 
        
        # Análisis de datos faltantes
        st.subheader("Análisis de Datos") 
        # Sustitución de st.markdown por el estilo de cerezo
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)
        
        # Ajuste de la relación de columnas para que col2 sea más ancha
        col1, col2 = st.columns([1, 1.5]) 
        
        with col1:
            st.write("**Información por columna:**") 
            for col in df.columns:
                non_null = df[col].notna().sum() 
                st.write(f"- **{col}**: {non_null}/{len(df)} válidos ({non_null/len(df)*100:.1f}%)") 
        
        with col2:
            st.write("**Muestra de datos:**") 
            # Mostrar los primeros 10 y usar use_container_width=True para ajustarlo
            st.dataframe(df[['titulo_post', 'autor_post', 'puntaje', 'numero_comentarios', 'fecha_post']].head(10), use_container_width=True) 
        
        # Llenar valores faltantes
        numeric_cols = ['numero_comentarios', 'puntaje', 'upvotes', 'downvotes', 'longitud_titulo', 'longitud_texto'] 
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0) 
        
        # Se añade la columna 'tiene_texto' aquí ya que se usa en los gráficos (por ejemplo, en el scatter plot)
        df['tiene_texto'] = df['texto_post'].notna() & (df['texto_post'].str.len() > 0)
        
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
    
    # Slider para rango de puntaje
    min_puntaje, max_puntaje = st.sidebar.slider(
        "Rango de puntaje",
        min_value=int(df['puntaje'].min()),
        max_value=int(df['puntaje'].max()),
        value=(int(df['puntaje'].min()), int(df['puntaje'].max())),
        step=50
    ) 
    
    # Multiselect para meses
    meses_disponibles = sorted(df['mes'].dropna().unique()) 
    meses_seleccionados = st.sidebar.multiselect(
        "Meses",
        options=meses_disponibles,
        default=meses_disponibles[-3:] if len(meses_disponibles) >= 3 else meses_disponibles
    ) 
    
    # Slider para número mínimo de comentarios
    min_comentarios = st.sidebar.slider(
        "Numero minimo de comentarios",
        min_value=0,
        max_value=int(df['numero_comentarios'].max()),
        value=0,
        step=10
    ) 
    
    # Slider para engagement rate
    max_engagement = df['engagement_rate'].quantile(0.95) # percentil 95 para evitar outliers
    min_engagement, max_engagement_filter = st.sidebar.slider(
        "Rango de engagement rate",
        min_value=0.0,
        max_value=float(max_engagement),
        value=(0.0, float(max_engagement)),
        step=0.5
    ) 
    
    # Multiselect para autores top
    top_autores = df['autor_post'].value_counts().head(20).index.tolist() 
    autores_seleccionados = st.sidebar.multiselect(
        "Filtrar por top 20 autores",
        options=['Todos'] + top_autores,
        default=['Todos']
    ) 
    
    # Aplicar filtros 
    df_filtrado = df[
        (df['puntaje'] >= min_puntaje) &
        (df['puntaje'] <= max_puntaje) &
        (df['numero_comentarios'] >= min_comentarios) &
        (df['engagement_rate'] >= min_engagement) &
        (df['engagement_rate'] <= max_engagement_filter)
    ] 
    
    if len(meses_seleccionados) > 0:
        df_filtrado = df_filtrado[df_filtrado['mes'].isin(meses_seleccionados)] 
    
    if 'Todos' not in autores_seleccionados and len(autores_seleccionados) > 0:
        df_filtrado = df_filtrado[df_filtrado['autor_post'].isin(autores_seleccionados)] 
    
    if len(df_filtrado) == 0:
        st.warning("No hay datos que coincidan con los filtros seleccionados. Ajusta los filtros.") 
        st.stop() 
    
    # Metricas principales
    col1, col2, col3, col4 = st.columns(4) 
    with col1:
        st.metric("Total de Posts", len(df_filtrado)) 
    with col2:
        avg_puntaje = df_filtrado['puntaje'].mean() 
        st.metric("Puntaje Promedio", f"{avg_puntaje:.0f}") 
    with col3:
        avg_comentarios = df_filtrado['numero_comentarios'].mean() 
        st.metric("Comentarios Promedio", f"{avg_comentarios:.1f}") 
    with col4:
        avg_engagement = df_filtrado['engagement_rate'].mean() 
        st.metric("Engagement Rate Promedio", f"{avg_engagement:.1f}%") 
    
    # Separador visual
    st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True) 

    # Inicializar el estado de sesión
    if 'show_graphs' not in st.session_state:
        st.session_state.show_graphs = False

    # Botón para mostrar/ocultar Gráficos
    if st.button("Mostrar Gráficos de Análisis"):
        st.session_state.show_graphs = not st.session_state.show_graphs

    if st.session_state.show_graphs:
        # Layout en dos columnas
        col1, col2 = st.columns(2) 

        # Definir un color de texto común para los gráficos 
        PLOT_TEXT_COLOR = 'black'
        PLOT_GRID_COLOR = '#E0E0E0' 
        
        # Definir colores para el  tooltip
        HOVERLABEL_BG_COLOR = '#F08080' 
        HOVERLABEL_FONT_COLOR = 'white'
        
        with col1:
            # Scatter Plot Puntaje vs Comentarios
            st.subheader("Relacion entre Puntaje y Comentarios") 
            
            fig_scatter = px.scatter(
                df_filtrado,
                x='puntaje',
                y='numero_comentarios',
                size='engagement_rate', 
                color='tiene_texto', 
                hover_data=['titulo_post', 'autor_post', 'fecha_post'],
                title="Scatter Plot de uuntaje vs Numero de Comentarios",
                labels={'puntaje': 'Puntaje', 'numero_comentarios': 'Número de Comentarios'},
                size_max=50,
                # usar paleta de colores cerezo
                color_discrete_sequence=SAKURA_DISCRETE_PALETTE
            ) 
            fig_scatter.update_layout(
                height=500,
                title_font_color=PLOT_TEXT_COLOR, 
                xaxis_title="Puntaje",
                yaxis_title="Número de Comentarios",
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
            
            # Histograma de Engagement Rate
            st.subheader("Distribucion por Tasa de participacion") 
            fig_hist = px.histogram(
                df_filtrado,
                x='engagement_rate',
                color='tiene_texto', # Canal visual: color
                title="Histograma de distribucion del Engagement Rate por Tipo de Post",
                labels={'engagement_rate': 'Tasa de participacion', 'count': 'Frecuencia'},
                nbins=30,
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
            # Bar Chart Top 10 Posts por Puntaje
            st.subheader("Primeros 10 post con mejor puntaje") 
            if len(df_filtrado) > 0: 
                top_posts = df_filtrado.nlargest(10, 'puntaje') 
                
                # Truncar títulos largos para mejor visualización
                top_posts_display = top_posts.copy() 
                top_posts_display['titulo_corto'] = top_posts_display['titulo_post'].str[:50] + '...' 
                
                fig_bar = px.bar(
                    top_posts_display,
                    x='puntaje',
                    y='titulo_corto',
                    color='numero_comentarios', 
                    orientation='h', 
                    title="Bar Chart Top 10 Posts con Mayor Puntaje",
                    labels={'puntaje': 'Puntaje', 'titulo_corto': 'Título del Post'},
                    # usar paleta de colores cerezo
                    color_continuous_scale=SAKURA_CONTINUOUS_PALETTE,
                    text='puntaje'
                ) 
                fig_bar.update_layout(
                    height=500, 
                    title_font_color=PLOT_TEXT_COLOR,
                    yaxis={'categoryorder': 'total ascending', 
                           'tickfont':dict(color=PLOT_TEXT_COLOR),
                           'title_font':dict(color=PLOT_TEXT_COLOR),
                           'gridcolor':PLOT_GRID_COLOR
                         },
                    xaxis_title="Puntaje",
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
                fig_bar.update_traces(texttemplate='%{text}', textposition='outside',
                                        textfont=dict(color=PLOT_TEXT_COLOR)) 
                st.plotly_chart(fig_bar, use_container_width=True) 
            
            # Box Plot Puntajes por Día de la Semana
            st.subheader("Distribucion de Puntajes por Dia") 
            fig_box = px.box(
                df_filtrado,
                x='dia_semana',
                y='puntaje',
                color='dia_semana', 
                title="Box Plot de distribucion de Puntajes por dias de la semana",
                labels={'dia_semana': 'Dia de la Semana', 'puntaje': 'Puntaje'},
                # usar paleta de colores cerezo
                color_discrete_sequence=SAKURA_DISCRETE_PALETTE
            ) 
            # Ordenar días de la semana
            dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] #
            fig_box.update_xaxes(categoryorder='array', categoryarray=dias_orden) 
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
        # Análisis temporal y de actividad
        # Sustitución de st.markdown por el estilo de cerezo
        st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True) 
        
        st.subheader("Actividad de Posts por Mes") 
        if len(df_filtrado) > 0: 
            actividad_mes = df_filtrado.groupby('mes').agg({
                'puntaje': 'mean',
                'numero_comentarios': 'mean',
                'id_post': 'count'
            }).reset_index() 
            actividad_mes.columns = ['mes', 'puntaje_promedio', 'comentarios_promedio', 'num_posts'] 
            
            fig_line = px.line(
                actividad_mes,
                x='mes',
                y='num_posts',
                title="Número de Posts por Mes",
                labels={'mes': 'Mes', 'num_posts': 'Número de Posts'},
                markers=True,
                # usar paleta de colores cerezo
                color_discrete_sequence=[SAKURA_DISCRETE_PALETTE[1]] 
            ) 
            fig_line.update_layout(
                height=400, 
                xaxis_tickangle=-45,
                title_font_color=PLOT_TEXT_COLOR,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=PLOT_TEXT_COLOR, 
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
                #TOOLTIP
                hoverlabel=dict(
                    bgcolor=HOVERLABEL_BG_COLOR, 
                    font_color=HOVERLABEL_FONT_COLOR 
                )
            ) 
            st.plotly_chart(fig_line, use_container_width=True) 

    # Separador visual
    st.markdown("<hr style='border: 1px solid #FFC0CB;'>", unsafe_allow_html=True)

    # Inicializar el estado de sesión
    if 'show_data' not in st.session_state:
        st.session_state.show_data = False

    st.subheader("Datos Filtrados listos para descargar")
    # Botón para mostrar Datos Filtrados
    if st.button("Mostrar Tabla de Datos Filtrados"):
        st.session_state.show_data = not st.session_state.show_data

    if st.session_state.show_data:
        # Tabla de datos filtrados
        col1, col2 = st.columns([3, 1]) 
        with col1:
            st.write(f"Mostrando {len(df_filtrado)} posts de {len(df)} totales") 
        with col2:
            mostrar_todas = st.checkbox("Mostrar todas las columnas", value=False) 
        
        if mostrar_todas:
            st.dataframe(df_filtrado, use_container_width=True) 
        else:
            columnas_principales = ['titulo_post', 'autor_post', 'fecha_post', 'puntaje', 'numero_comentarios', 
                                    'tiene_texto', 'engagement_rate'] 
            st.dataframe(df_filtrado[columnas_principales], use_container_width=True) 
            

else:
    st.error("No se pudieron cargar los datos o el archivo está vacío. Verifica que el archivo CSV esté disponible y contenga datos válidos.") 
    st.info("Asegúrate de que el archivo 'posts.csv' esté en el directorio correcto y tenga el formato esperado.")