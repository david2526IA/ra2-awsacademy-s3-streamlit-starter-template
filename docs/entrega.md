# Entrega (GitHub) - RA2 SBD

## Que entregar
1. URL de tu fork en GitHub.
2. Tag `v1.0-entrega` apuntando al commit final.
3. `docs/evidencias.md` completo con capturas.
4. URL final del dashboard en evidencias: `http://IP_PUBLICA_EC2:8501`.

## Orden recomendado de entrega
1. Verifica que el dashboard funciona en EC2.
2. Completa `README.md`.
3. Completa `docs/evidencias.md`.
4. Sube capturas ordenadas a `docs/capturas/`.
5. Haz commit final y push.
6. Crea y publica el tag `v1.0-entrega`.

## Comandos de entrega
```bash
git add .
git commit -m "Entrega RA2 completa"
git push origin main
git tag v1.0-entrega
git push origin v1.0-entrega
```

## Verificaciones antes de etiquetar
```bash
git status
git log --oneline -n 5
git tag --list
```

## Que se corrige
Se corregira exclusivamente la version marcada por el tag `v1.0-entrega`.

## Normas de seguridad
No se aceptan entregas con secretos en el repositorio.

No subir:
- claves AWS
- tokens
- archivos `.pem`
- `.env` con datos sensibles

Si subiste algo sensible por error:
1. Elimina el archivo.
2. Rota credenciales en AWS.
3. Reescribe historial (si procede) o crea repo nuevo y avisa al profesor.
