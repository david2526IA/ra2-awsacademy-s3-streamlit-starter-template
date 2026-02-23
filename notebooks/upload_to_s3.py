"""Script de ingesta RA2: normaliza JSON IoT y lo sube a S3.

Uso:
    python notebooks/upload_to_s3.py \
      --input iabd01_sensores.json \
      --bucket mi-bucket \
      --region eu-west-1 \
      --key data/sensores/iabd01_sensores.json
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import boto3


STATE_MAP = {
    "ACTIVO": "OK",
    "ACTIVE": "OK",
    "INACTIVO": "FAIL",
    "INACTIVE": "FAIL",
    "ALERTA": "WARN",
    "WARNING": "WARN",
    "OK": "OK",
    "WARN": "WARN",
    "FAIL": "FAIL",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normaliza JSON IoT y lo sube a S3")
    parser.add_argument("--input", default="iabd01_sensores.json", help="Ruta del JSON de entrada")
    parser.add_argument("--bucket", default=os.getenv("S3_BUCKET", ""), help="Nombre del bucket S3")
    parser.add_argument(
        "--key",
        default=os.getenv("S3_KEY", "data/sensores/iabd01_sensores.json"),
        help="Key destino en S3",
    )
    parser.add_argument("--region", default=os.getenv("AWS_REGION", ""), help="Region AWS")
    parser.add_argument(
        "--output",
        default="notebooks/iabd01_sensores_normalizado.json",
        help="Ruta local del JSON normalizado",
    )
    return parser.parse_args()


def _to_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_state(value: Any) -> str:
    if value is None:
        return "WARN"
    return STATE_MAP.get(str(value).strip().upper(), "WARN")


def _normalize_timestamp(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()

    raw = str(value).strip()
    if not raw:
        return datetime.now(timezone.utc).isoformat()

    try:
        # Acepta "2025-02-01 00:00:00" y lo convierte a ISO8601 UTC
        dt = datetime.fromisoformat(raw.replace(" ", "T"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except ValueError:
        return datetime.now(timezone.utc).isoformat()


def normalize_record(record: dict[str, Any], idx: int) -> dict[str, Any]:
    sensor_id = record.get("sensor_id") or record.get("id") or f"sensor_{idx:02d}"

    normalized = {
        "timestamp": _normalize_timestamp(record.get("timestamp") or record.get("time")),
        "sensor_id": str(sensor_id),
        "sensor_state": _normalize_state(record.get("sensor_state") or record.get("estado") or record.get("state")),
        "temperature_c": _to_float(record.get("temperature_c") or record.get("temperatura") or record.get("temperature") or record.get("temp")),
        "co2_ppm": _to_float(record.get("co2_ppm") or record.get("co2")),
        "lat": _to_float(record.get("lat") or record.get("latitude")),
        "lon": _to_float(record.get("lon") or record.get("longitude")),
    }
    return normalized


def load_input_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    if isinstance(raw, dict):
        for key in ("data", "records", "items"):
            if isinstance(raw.get(key), list):
                return [r for r in raw[key] if isinstance(r, dict)]
        return [raw]

    raise ValueError("Formato JSON no soportado")


def save_output_json(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def upload_to_s3(bucket: str, key: str, region: str, local_file: Path) -> None:
    if not bucket:
        raise ValueError("Debes indicar --bucket o definir S3_BUCKET")
    if not region:
        raise ValueError("Debes indicar --region o definir AWS_REGION")

    s3_client = boto3.client("s3", region_name=region)
    s3_client.upload_file(str(local_file), bucket, key)


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    source_records = load_input_json(input_path)
    normalized_records = [normalize_record(r, idx + 1) for idx, r in enumerate(source_records)]
    save_output_json(output_path, normalized_records)

    upload_to_s3(args.bucket, args.key, args.region, output_path)

    print(f"Registros origen: {len(source_records)}")
    print(f"Registros normalizados: {len(normalized_records)}")
    print(f"JSON normalizado: {output_path}")
    print(f"Subido a: s3://{args.bucket}/{args.key}")


if __name__ == "__main__":
    main()
