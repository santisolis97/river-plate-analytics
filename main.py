import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import datetime

from scripts.extract import extract_river_scraping
from scripts.transform import transform_data
from scripts.load import load_to_sql
from config import get_db_url


# --------------------------------------------------
# PAGE CONFIG (must be first Streamlit command)
# --------------------------------------------------
st.set_page_config(
    page_title="River Plate Analytics",
    page_icon="⚪🔴",
    layout="wide"
)

st.info("🚀 App started correctly")


# --------------------------------------------------
# DB HELPERS (LAZY + CACHED)
# --------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_engine():
    try:
        db_url = get_db_url()
        if not db_url:
            return None
        return create_engine(db_url, pool_pre_ping=True)
    except Exception:
        return None


@st.cache_data(ttl=300, show_spinner="Cargando datos desde la base…")
def load_data():
    engine = get_engine()
    if engine is None:
        return None

    query = "SELECT * FROM partidos_river"
    df = pd.read_sql(query, engine)
    return df


# --------------------------------------------------
# CUSTOM CSS (River identity)
# --------------------------------------------------
st.markdown(
    """
    <style>
    h1 { 
        color: #ffffff !important; 
        padding: 20px; 
        border-radius: 12px; 
        text-align: center;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    h2, h3 { color: #FFFFFF !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: #ffffff; 
        color: #ED1C24; 
        border: 2px solid #ED1C24;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 25px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ED1C24 !important; 
        color: #ffffff !important; 
        border: 2px solid #ED1C24 !important;
    }

    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #ED1C24;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    [data-testid="stMetric"] > * {
        color: rgb(14, 17, 23);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("⚪🔴 RIVER PLATE - TEMPORADA 2026")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.image(
        "https://cdn.resfu.com/img_data/equipos/593.png?size=120x",
        width=150
    )
    st.markdown("---")

    if st.button("🚀 Actualizar Datos (ETL)"):
        with st.spinner("Procesando datos..."):
            extract_river_scraping()
            transform_data()
            load_to_sql()
            st.cache_data.clear()
            st.success("¡Datos actualizados!")


# --------------------------------------------------
# MAIN LOGIC
# --------------------------------------------------
df = load_data()

if df is None:
    st.warning(
        "⚠️ No se pudo conectar a la base de datos.\n\n"
        "Verificá que las variables de entorno estén configuradas en Streamlit Cloud."
    )
    st.stop()

if df.empty:
    st.info("La base de datos está vacía. Ejecuta el ETL desde la barra lateral.")
    st.stop()


# --------------------------------------------------
# DATA PREP
# --------------------------------------------------
df["fecha"] = pd.to_datetime(df["fecha"])

tab1, tab2 = st.tabs(
    ["📅 AGENDA POR COMPETICIÓN", "📊 ANÁLISIS ESTADÍSTICO"]
)


# --------------------------------------------------
# TAB 1 – CALENDAR
# --------------------------------------------------
with tab1:
    st.header("Calendario River Plate 2026")

    for comp in df["competicion"].unique():
        with st.expander(f"🏆 {comp.upper()}", expanded=True):
            df_comp = df[df["competicion"] == comp].sort_values("fecha").copy()

            df_view = df_comp.rename(
                columns={
                    "fecha": "FECHA",
                    "local": "LOCAL",
                    "visitante": "VISITANTE",
                    "g_river": "GOLES DE RIVER",
                    "g_rival": "GOLES DEL RIVAL",
                    "resultado_final": "RESULTADO",
                }
            )

            df_view["FECHA"] = df_view["FECHA"].dt.strftime("%d/%m/%Y %H:%M")

            def semaforo(val):
                return {
                    "Ganó": "background-color:#d4edda;font-weight:bold;",
                    "Empató": "background-color:#fff3cd;font-weight:bold;",
                    "Perdió": "background-color:#f8d7da;font-weight:bold;",
                }.get(val, "")

            st.dataframe(
                df_view[
                    [
                        "FECHA",
                        "LOCAL",
                        "VISITANTE",
                        "GOLES DE RIVER",
                        "GOLES DEL RIVAL",
                        "RESULTADO",
                    ]
                ].style.applymap(semaforo, subset=["RESULTADO"]),
                use_container_width=True,
                hide_index=True,
            )


# --------------------------------------------------
# TAB 2 – ANALYTICS
# --------------------------------------------------
with tab2:
    st.header("Análisis de Rendimiento")

    df_jugados = df[df["resultado_final"] != "Pendiente"].copy()

    if df_jugados.empty:
        st.warning("No hay partidos jugados aún.")
        st.stop()

    df_jugados["Puntos"] = df_jugados["resultado_final"].map(
        {"Ganó": 3, "Empató": 1, "Perdió": 0}
    )

    puntos = (
        df_jugados.groupby("competicion")["Puntos"]
        .sum()
        .reset_index()
    )

    cols = st.columns(len(puntos))
    for i, row in puntos.iterrows():
        cols[i].metric(row["competicion"], f"{row['Puntos']} pts")

    st.divider()

    barras = (
        df_jugados.groupby(["competicion", "resultado_final"])
        .size()
        .reset_index(name="Cantidad")
    )

    fig_bar = px.bar(
        barras,
        x="competicion",
        y="Cantidad",
        color="resultado_final",
        barmode="group",
        text_auto=True,
        color_discrete_map={
            "Ganó": "#b0d3b4",
            "Empató": "#e6d89f",
            "Perdió": "#e0bfc2",
        },
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        fig_pie = px.pie(
            df_jugados,
            names="resultado_final",
            hole=0.4,
            color_discrete_map={
                "Ganó": "#b0d3b4",
                "Empató": "#e6d89f",
                "Perdió": "#e0bfc2",
            },
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        df_jugados["g_river"] = pd.to_numeric(
            df_jugados["g_river"], errors="coerce"
        )
        st.metric(
            "Promedio goles de River",
            f"{df_jugados['g_river'].mean():.2f}",
        )
        st.metric(
            "Vallas invictas",
            (df_jugados["g_rival"].astype(str) == "0").sum(),
        )
