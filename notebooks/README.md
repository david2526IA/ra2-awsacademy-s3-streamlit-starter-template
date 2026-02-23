# Notebooks / Scripts de carga a S3

Este directorio contiene la parte de ingesta del RA2.

## Archivo principal
- `upload_to_s3.py`: normaliza datos IoT y sube el JSON a S3.

## Uso recomendado

```bash
python notebooks/upload_to_s3.py \
  --input iabd01_sensores.json \
  --bucket <TU_BUCKET> \
  --region <TU_REGION> \
  --key data/sensores/iabd01_sensores.json
```

Si el JSON viene en un enlace, usa:

```bash
python notebooks/upload_to_s3.py \
  --input-url "https://.../sensores.json" \
  --bucket <TU_BUCKET> \
  --region <TU_REGION> \
  --key data/sensores/iabd01_sensores.json
```

## Resultado
- Archivo local normalizado: `notebooks/iabd01_sensores_normalizado.json`
- Objeto subido a: `s3://<TU_BUCKET>/data/sensores/iabd01_sensores.json`

Importante: no subir credenciales ni tokens al repositorio.
