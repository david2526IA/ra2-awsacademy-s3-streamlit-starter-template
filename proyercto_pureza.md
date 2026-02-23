# PROYERCTO_PUREZA - Guia de entrega RA2 SBD

Este documento es tu plan unico para dejar el proyecto listo para GitHub y cumplir el enunciado, la entrega y la rubrica.

## 1) Que tienes que entregar (obligatorio)

1. Repositorio fork en GitHub con todo el trabajo.
2. Tag `v1.0-entrega` apuntando al commit final.
3. `docs/evidencias.md` completo.
4. URL final funcionando: `http://IP_PUBLICA_EC2:8501`.
5. Sin secretos en el repo.

## 2) Antes de documentar: deja el proyecto funcional

Segun tu plantilla actual, todavia hay partes por implementar:

1. `app/dashboard.py` tiene funciones con `NotImplementedError`.
2. `notebooks/upload_to_s3.py` esta vacio.

Si eso no esta terminado, no vas a poder demostrar toda la rubrica.

## 3) Estructura recomendada para capturas

Crea esta carpeta y guarda evidencias numeradas:

`docs/capturas/`

Nombres recomendados:

1. `01_s3_bucket_region.png`
2. `02_s3_privado_block_public_access.png`
3. `03_s3_objeto_json_data_sensores.png`
4. `04_notebook_script_upload_ok.png`
5. `05_ec2_instancia_ubuntu.png`
6. `06_ec2_security_group_8501.png`
7. `07_ssh_conexion.png`
8. `08_sts_get_caller_identity.png`
9. `09_s3_ls_desde_ec2.png`
10. `10_streamlit_hello_o_import_ok.png`
11. `11_pip_install_requirements.png`
12. `12_dashboard_filtro_sensor_state.png`
13. `13_dashboard_slider_temperatura.png`
14. `14_dashboard_tabla_filtrada.png`
15. `15_dashboard_grafica_linea_temperatura.png`
16. `16_dashboard_grafica_barras_co2.png`
17. `17_dashboard_mapa.png`
18. `18_arranque_segundo_plano_nohup.png`
19. `19_log_streamlit_tail.png`
20. `20_dashboard_url_publica.png`

## 4) Que debes escribir en README.md

Asegurate de incluir estos apartados:

1. Objetivo del proyecto.
2. Arquitectura resumida (S3 -> EC2 -> Streamlit).
3. Requisitos.
4. Variables de entorno (`AWS_REGION`, `S3_BUCKET`, `S3_KEY`).
5. Pasos para ejecutar en EC2.
6. URL final de acceso.
7. Estructura de carpetas del repo.
8. Seguridad: confirmacion de que no hay claves ni `.pem` en Git.

Texto breve recomendado para seccion "Evidencias" del README:

```md
## Evidencias
Las evidencias completas estan en `docs/evidencias.md` y las capturas en `docs/capturas/`.
```

## 5) Como rellenar docs/evidencias.md (orden exacto)

Completa cada bloque con:

1. Dato real (nombre alumno, region, bucket, URL).
2. Mini explicacion de 1-2 lineas.
3. Captura enlazada por ruta relativa.

Ejemplo de formato:

```md
- Captura: `docs/capturas/08_sts_get_caller_identity.png`
- Resultado: identidad AWS validada desde EC2.
```

Checklist por seccion:

1. `0) Identificacion`: alumno, grupo, variante A/B, region, bucket.
2. `1) S3 privado`: bucket, privacidad, objeto JSON.
3. `2) Notebook/Script`: ejecucion y ruta real en repo.
4. `3) EC2 y red`: instancia, SG 8501, SSH.
5. `4) Acceso S3 desde EC2`: `aws sts get-caller-identity` y `aws s3 ls`.
6. `5) Streamlit en EC2`: prueba streamlit + dependencias.
7. `6) Dashboard`: filtros, tabla, linea, barras, mapa.
8. `7) Despliegue final`: comando segundo plano, log, URL y navegador.
9. `8) Observaciones`: problemas reales y solucion.

## 6) Mapeo directo con rubrica (para asegurar nota)

1. S3 privado + datos (2.0): secciones 1 y 2 de evidencias.
2. Ingesta script (1.5): seccion 2.
3. EC2 + despliegue (2.0): secciones 3, 5 y 7.
4. Dashboard Streamlit (3.5): seccion 6 completa.
5. Buenas practicas GitHub (1.0): README claro + evidencias completas + tag.
6. Bonus IAM Role (+1.0): explicar Variante A y probarla en evidencias.

## 7) Comandos finales de entrega

Revisa estado y sube:

```bash
git add .
git commit -m "Entrega RA2 completa: dashboard, evidencias y README"
git push origin main
```

Crea el tag pedido:

```bash
git tag v1.0-entrega
git push origin v1.0-entrega
```

Verifica:

```bash
git tag --list
```

## 8) Control final (ultima revision)

Marca todo antes de entregar:

1. [ ] Dashboard abre en `http://IP_PUBLICA_EC2:8501`
2. [ ] `docs/evidencias.md` completo con capturas reales
3. [ ] README claro y actualizado
4. [ ] Sin secretos en git (`.pem`, claves AWS, `.env` sensible)
5. [ ] Tag `v1.0-entrega` publicado en GitHub

