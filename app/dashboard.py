import os

import pandas as pd
import plotly.express as px
import streamlit as st

from app.services.preprocessing import ensure_columns, parse_time, to_dataframe
from app.services.s3_loader import load_json_from_s3

st.set_page_config(page_title="RA2 - IoT Dashboard", layout="wide")

st.title("RA2 - Dashboard IoT (S3 privado + Streamlit)")
st.caption("Carga desde S3, filtros, tabla, graficas y mapa.")

# --- Config ---
AWS_REGION = os.getenv("AWS_REGION", "")
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_KEY = os.getenv("S3_KEY", "")

with st.sidebar:
    st.header("Configuracion")
    st.write("Usa variables de entorno o escribe aqui para pruebas.")
    aws_region = st.text_input("AWS_REGION", value=AWS_REGION, placeholder="eu-west-1")
    s3_bucket = st.text_input("S3_BUCKET", value=S3_BUCKET, placeholder="mi-bucket-privado")
    s3_key = st.text_input("S3_KEY", value=S3_KEY, placeholder="data/sensores/iabdXX_sensores.json")

    st.divider()
    st.header("Filtros")
    sensor_state = st.selectbox("Estado del sensor", ["(todos)", "OK", "WARN", "FAIL"])
    temp_min, temp_max = st.slider("Rango temperatura (C)", -20.0, 80.0, (0.0, 40.0), 0.5)

    st.divider()
    reload_btn = st.button("Recargar datos", type="primary")


@st.cache_data(show_spinner=False)
def load_data(bucket: str, key: str, region: str) -> pd.DataFrame:
    """Carga datos desde S3 y devuelve un DataFrame listo para usar."""
    raw = load_json_from_s3(bucket, key, region)
    df = to_dataframe(raw)
    df = ensure_columns(df)
    df = parse_time(df)
    return df


def apply_filters(df: pd.DataFrame, sensor_state: str, temp_min: float, temp_max: float) -> pd.DataFrame:
    """Aplica filtros de estado y rango de temperatura."""
    filtered = df.copy()

    if sensor_state.strip().lower() != "(todos)":
        filtered = filtered[
            filtered["sensor_state"].astype(str).str.upper() == sensor_state.strip().upper()
        ]

    filtered = filtered[
        filtered["temperature_c"].between(temp_min, temp_max, inclusive="both")
    ]
    return filtered


def plot_temperature(df: pd.DataFrame):
    """Figura Plotly de linea: temperatura vs tiempo."""
    chart_df = df.dropna(subset=["timestamp", "temperature_c", "sensor_id"]).copy()
    chart_df = chart_df.sort_values("timestamp", ascending=True)

    fig = px.line(
        chart_df,
        x="timestamp",
        y="temperature_c",
        color="sensor_id",
        markers=True,
        title="Temperatura (C) por tiempo y sensor",
        labels={"timestamp": "Fecha/hora", "temperature_c": "Temperatura (C)", "sensor_id": "Sensor"},
    )
    fig.update_layout(legend_title_text="Sensor")
    return fig


def plot_co2(df: pd.DataFrame):
    """Figura Plotly de barras: CO2 medio por sensor."""
    agg_df = (
        df.dropna(subset=["sensor_id", "co2_ppm"])
        .groupby("sensor_id", as_index=False)["co2_ppm"]
        .mean()
        .sort_values("co2_ppm", ascending=False)
    )

    fig = px.bar(
        agg_df,
        x="sensor_id",
        y="co2_ppm",
        color="sensor_id",
        title="CO2 medio (ppm) por sensor",
        labels={"sensor_id": "Sensor", "co2_ppm": "CO2 medio (ppm)"},
    )
    fig.update_layout(showlegend=False)
    return fig


def render_map(df: pd.DataFrame):
    """Muestra mapa con st.map() usando lat/lon."""
    map_df = df.dropna(subset=["lat", "lon"])[["lat", "lon"]].copy()
    if map_df.empty:
        st.info("No hay coordenadas validas para el filtro actual.")
        return
    st.map(map_df, latitude="lat", longitude="lon")


# --- Control recarga cache ---
if reload_btn:
    load_data.clear()

# --- Carga ---
if not s3_bucket or not s3_key or not aws_region:
    st.warning("Define AWS_REGION, S3_BUCKET y S3_KEY (variables o barra lateral).")
    st.stop()

try:
    with st.spinner("Cargando JSON desde S3..."):
        df = load_data(s3_bucket, s3_key, aws_region)
except Exception as e:
    st.error("No se pudo cargar desde S3. Revisa permisos, region y ruta del objeto.")
    st.exception(e)
    st.stop()

# --- Filtrado ---
fdf = apply_filters(df, sensor_state, temp_min, temp_max)

# --- Metricas ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros (total)", len(df))
c2.metric("Registros (filtrado)", len(fdf))
c3.metric("Sensores unicos", fdf["sensor_id"].nunique() if len(fdf) else 0)
c4.metric("Ultima lectura", fdf["timestamp"].max().isoformat() if len(fdf) else "-")

# --- Tabla ---
st.subheader("Tabla (filtrada)")
st.dataframe(
    fdf.sort_values("timestamp", ascending=False) if "timestamp" in fdf.columns else fdf,
    use_container_width=True,
    height=320,
)

left, right = st.columns(2)

with left:
    st.subheader("Temperatura en el tiempo")
    if len(fdf):
        fig = plot_temperature(fdf)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin datos con el filtro actual.")

with right:
    st.subheader("CO2 por sensor (agregado)")
    if len(fdf):
        fig2 = plot_co2(fdf)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sin datos con el filtro actual.")

st.subheader("Mapa de sensores")
if len(fdf):
    render_map(fdf)
else:
    st.info("Sin datos con el filtro actual.")
