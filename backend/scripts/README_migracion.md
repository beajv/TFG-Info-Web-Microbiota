# Scripts de Migración de Base de Datos

Este documento explica los pasos necesarios para dejar la base de datos actualizada con los nuevos datos clínicos y microbiológicos del sistema.

---

## Requisitos previos

- Tener PostgreSQL en funcionamiento.
- Haber configurado correctamente el archivo `.env` si se ejecuta dentro de Docker o entorno local.
- Disponer del archivo Excel con los datos actualizados (`ENDORE_relab_0.01%_def_160525.xlsx`) y del diccionario (`microorganismos_detectados_con_ids.xlsx`).

---

## Scripts a ejecutar (en orden)

### 1. `mother_nuevo_db.py`

Crea la tabla `mother`, que contiene el diccionario de microorganismos usados en el sistema, con sus nombres originales, nombres agrupados, identificadores y códigos simplificados (`x1`, `x2`, …).

```bash
python3 mother_nuevo_db.py
```

### 2. `tablas_nuevas.py`
Genera las tablas clínicas para los distintos sitios anatómicos (cervix, vagina, uterus, rectum, orine) a partir de los Excels de microbiota.

```bash
python3 tablas_nuevas.py
```