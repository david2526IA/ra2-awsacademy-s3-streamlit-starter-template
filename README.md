# RA2 SBD - Dashboard IoT en Streamlit con datos en S3

Proyecto de la tarea evaluable RA2 (Sistemas de Big Data) en AWS Academy.

## Objetivo
Implementar un flujo completo:
1. Ingesta de datos IoT JSON y subida a S3 privado.
2. Lectura desde EC2 Ubuntu 22.04 con Streamlit.
3. Visualizacion con filtros, tabla, graficas Plotly y mapa.
4. Despliegue final accesible por URL publica.

## Arquitectura
S3 (bucket privado) -> EC2 Ubuntu 22.04 -> Streamlit (`app/dashboard.py`) -> navegador (`http://IP_PUBLICA_EC2:8501`).

## Estructura del repositorio
- `app/`: dashboard Streamlit y servicios (S3 + preprocesado).
- `notebooks/`: script de ingesta/subida a S3.
- `scripts/`: instalacion en EC2 y arranque en segundo plano.
- `docs/`: enunciado, evidencias, entrega, rubric y decisiones.
- `docs/capturas/`: capturas ordenadas para evidencias.

## Requisitos
- Python 3.10+
- Cuenta/lab AWS Academy
- Bucket S3 privado
- EC2 Ubuntu 22.04
- Security Group con puertos:
  - `22` (SSH) desde tu IP
  - `8501` (Streamlit) desde tu IP o segun lab

Instalacion local:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Variables de entorno
La app usa:
- `AWS_REGION`
- `S3_BUCKET`
- `S3_KEY`

Ejemplo:

```bash
export AWS_REGION=eu-west-1
export S3_BUCKET=mi-bucket-privado
export S3_KEY=data/sensores/iabd01_sensores.json
```

## Parte 1 y 2 - Ingesta y subida a S3
Script incluido: `notebooks/upload_to_s3.py`.

Ejemplo:

```bash
python notebooks/upload_to_s3.py \
  --input iabd01_sensores.json \
  --bucket <TU_BUCKET> \
  --region <TU_REGION> \
  --key data/sensores/iabd01_sensores.json
```

Salida esperada:
- JSON normalizado en `notebooks/iabd01_sensores_normalizado.json`
- Objeto subido a `s3://<TU_BUCKET>/data/sensores/iabd01_sensores.json`

## Parte 3 y 5 - EC2 y despliegue
En la instancia EC2:

```bash
sudo apt update
sudo apt install -y git
git clone <URL_DE_TU_FORK>
cd ra2-awsacademy-s3-streamlit-starter-template
bash scripts/ec2_setup.sh
```

Exporta variables y arranca en segundo plano:

```bash
export AWS_REGION=<TU_REGION>
export S3_BUCKET=<TU_BUCKET>
export S3_KEY=data/sensores/iabd01_sensores.json
bash scripts/run_streamlit_nohup.sh
```

Comprobaciones:

```bash
aws sts get-caller-identity
aws s3 ls s3://<TU_BUCKET>/data/sensores/
tail -n 50 streamlit.log
```

URL final:
- `http://IP_PUBLICA_EC2:8501`

## Parte 4 - Funcionalidad del dashboard
Implementado en `app/dashboard.py`:
- Lectura de JSON desde S3 usando variables de entorno.
- Filtro por `sensor_state`.
- Slider de rango de temperatura.
- Tabla filtrada ordenada por `timestamp`.
- Grafica de linea: temperatura vs tiempo.
- Grafica de barras: CO2 medio por sensor.
- Mapa con `lat/lon` usando `st.map()`.

## Evidencias y capturas
- Evidencias completas: `docs/evidencias.md`
- Capturas ordenadas: `docs/capturas/`

## Rúbrica (resumen)
Referencia oficial: `docs/rubric.md`.

Cobertura en este repo:
1. S3 privado + datos: subida y esquema JSON documentado.
2. Ingesta: script reproducible en `notebooks/upload_to_s3.py`.
3. EC2 + despliegue: scripts de setup/arranque y comprobaciones.
4. Dashboard: lectura S3, filtros, tabla, graficas y mapa.
5. GitHub: README claro, evidencias y tag de entrega.

## Seguridad
No subir nunca al repositorio:
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- archivos `.pem`
- `.env` con secretos

Variantes validas de acceso a S3 en EC2:
- Variante A (recomendada): IAM Role/Instance Profile.
- Variante B: `aws configure` en EC2.

## Entrega en GitHub
Segun `docs/entrega.md`, debes entregar:
1. Enlace al fork.
2. Tag `v1.0-entrega`.
3. `docs/evidencias.md` completo.
4. URL final del dashboard en evidencias.

Comandos:

```bash
git add .
git commit -m "Entrega RA2 completa"
git push origin main
git tag v1.0-entrega
git push origin v1.0-entrega
```

Verificar tag:

```bash
git tag --list
```
