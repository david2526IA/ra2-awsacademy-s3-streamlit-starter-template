# Decisiones de diseno - RA2 SBD

Este documento justifica decisiones tecnicas aplicadas en la entrega.

## 1) Modelo de datos IoT
Esquema utilizado en el dashboard y en la ingesta:
- `timestamp`
- `sensor_id`
- `sensor_state` (`OK`, `WARN`, `FAIL`)
- `temperature_c`
- `co2_ppm`
- `lat`, `lon`

Razon:
- Coincide con el esquema recomendado en el enunciado.
- Permite filtrar, agregar y mapear sin transformaciones complejas en la vista.

## 2) Normalizacion aplicada
En `app/services/preprocessing.py` y `notebooks/upload_to_s3.py` se normalizan nombres comunes:
- `temperatura` -> `temperature_c`
- `co2` -> `co2_ppm`
- `estado` -> `sensor_state`
- `latitude/longitude` -> `lat/lon`

Se normalizan estados a `OK/WARN/FAIL`:
- `Activo` -> `OK`
- `Inactivo` -> `FAIL`
- `Alerta` -> `WARN`

Razon:
- Garantiza compatibilidad con datasets de origen heterogeneo.
- Mantiene el filtro de estado alineado con la rubrica.

## 3) Agregaciones para graficas
- Temperatura: grafica de linea por `timestamp`, color por `sensor_id`.
- CO2: grafica de barras por `sensor_id` usando media de `co2_ppm`.

Razon:
- La serie temporal facilita detectar tendencias.
- La media de CO2 por sensor compara comportamiento general por dispositivo.

## 4) Supuestos tecnicos
- `timestamp` se parsea a UTC.
- Si el timestamp no es valido en todos los registros, se usa fallback para evitar que la app falle.
- El mapa ignora registros sin coordenadas validas.

## 5) Variante AWS usada
Variante seleccionada: `<A o B>`

- Si A: IAM Role en EC2 con permisos minimos de lectura a `s3://<bucket>/data/sensores/*`.
- Si B: `aws configure` en EC2 y credenciales locales del lab.

Justificacion:
- `<explica por que elegiste la variante en tu lab>`

## 6) Seguridad
Se verifica que no se suben secretos:
- No `.pem` en el repo.
- No claves AWS en codigo o capturas.
- Variables por entorno (`AWS_REGION`, `S3_BUCKET`, `S3_KEY`).
