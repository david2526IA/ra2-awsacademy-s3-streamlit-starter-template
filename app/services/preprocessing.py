from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = [
    "timestamp",
    "sensor_id",
    "sensor_state",
    "temperature_c",
    "co2_ppm",
    "lat",
    "lon",
]


def to_dataframe(raw: object) -> pd.DataFrame:
    """Convierte JSON (lista/dict) a DataFrame."""
    if isinstance(raw, list):
        return pd.DataFrame(raw)
    if isinstance(raw, dict):
        for key in ("data", "records", "items"):
            if key in raw and isinstance(raw[key], list):
                return pd.DataFrame(raw[key])
        return pd.DataFrame([raw])
    raise ValueError("Formato JSON no soportado")


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Asegura columnas minimas y normaliza nombres comunes."""
    rename_map = {
        "temp": "temperature_c",
        "temperature": "temperature_c",
        "temperatura": "temperature_c",
        "co2": "co2_ppm",
        "state": "sensor_state",
        "estado": "sensor_state",
        "id": "sensor_id",
        "longitude": "lon",
        "latitude": "lat",
        "time": "timestamp",
    }

    for old_col, new_col in rename_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df = df.rename(columns={old_col: new_col})
        elif old_col in df.columns and new_col in df.columns and df[new_col].isna().all():
            df[new_col] = df[old_col]

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    # Normalizacion de estado para la rubrica: OK/WARN/FAIL
    if "sensor_state" in df.columns:
        normalized_state = df["sensor_state"].astype(str).str.strip().str.upper().replace(
            {
                "ACTIVO": "OK",
                "ACTIVE": "OK",
                "INACTIVO": "FAIL",
                "INACTIVE": "FAIL",
                "ALERTA": "WARN",
                "WARNING": "WARN",
            }
        )
        df["sensor_state"] = normalized_state

    for num_col in ("temperature_c", "co2_ppm", "lat", "lon"):
        df[num_col] = pd.to_numeric(df[num_col], errors="coerce")

    return df


def parse_time(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte timestamp a datetime UTC."""
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)

    if df["timestamp"].isna().all():
        # Fallback para no romper la app en datasets sin timestamp valido.
        df["timestamp"] = pd.Timestamp.utcnow()

    return df
