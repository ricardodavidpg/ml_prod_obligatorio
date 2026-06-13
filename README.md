# Property Valuation — ML en Producción 2026

Predicción del precio de propiedades inmobiliarias en Montevideo mediante un modelo de Machine Learning, expuesto como API REST y consumido por una interfaz web interactiva.

**Autores:** Rodrigo Mendez, Leonell Tambasco, David Pereira

---

## Arquitectura general

```
                    Usuario
                       │
                Navegador Web
                       │
              http://<host>:8081
                       │
          ┌────────────────────────┐
          │     Frontend UI        │
          │       Gradio           │  Docker Container
          └────────────────────────┘
                       │
            HTTP REST (JSON)
                       │
              http://api:8080
                       │
          ┌────────────────────────┐
          │     Backend API        │
          │       FastAPI          │  Docker Container
          │                        │
          │  Inference Pipeline    │
          │  Modelo ML (.pkl)      │
          └────────────────────────┘
```

---

## Estructura del proyecto

```
ml_prod_obligatorio/
├── docker-compose.yaml
├── setup.py
└── src/
    ├── backend/                        # Servicio de inferencia (API REST)
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── api/
    │   │   ├── app.py                  # Entrypoint FastAPI + carga del modelo al inicio
    │   │   └── routers/
    │   │       ├── __init__.py         # Registro de routers
    │   │       ├── health.py           # GET /health
    │   │       └── poperty_value.py    # POST /properties-valuation/houses
    │   ├── core/
    │   │   └── inference/
    │   │       ├── inference_pipeline.py   # Orquesta la predicción
    │   │       ├── model_loader.py         # Carga el modelo desde disco (joblib)
    │   │       └── entity_mapper.py        # Convierte entidades Pydantic a DataFrame
    │   ├── entities/
    │   │   ├── properties.py           # Property, ClassifiedProperty, PropertyType
    │   │   └── payload.py              # PropertyPayload, ResponsePropertyPayload
    │   ├── settings/
    │   │   ├── __init__.py
    │   │   ├── logger.py               # Configuración del logger
    │   │   └── settings_manager.py     # Carga configuración desde YAML
    │   ├── utils/
    │   │   └── file_loading.py
    │   └── artifacts/
    │       └── model.pkl               # Modelo entrenado (debe existir antes de buildear)
    └── frontend/                       # Interfaz de usuario (Gradio)
        ├── Dockerfile
        ├── requirements.txt
        └── ui/
            └── ui_app.py               # App Gradio, consume la API via HTTP
```

---

## Descripción de los paquetes

### `src/backend` — Servicio de inferencia

Aplicación **FastAPI** que expone el modelo de ML como API REST. Puerto: `8080`.

| Paquete | Responsabilidad |
|---|---|
| `api/app.py` | Inicializa la app FastAPI. Al arrancar carga el modelo en memoria via `lifespan` y lo deja disponible en `request.state` para todos los handlers |
| `api/routers/health.py` | Endpoint `GET /health` — responde `{"status": "ok"}` para verificar que el servicio está activo |
| `api/routers/poperty_value.py` | Endpoint `POST /properties-valuation/houses` — recibe una lista de propiedades, invoca el pipeline de inferencia y devuelve los precios estimados |
| `core/inference/model_loader.py` | Carga el modelo serializado desde `src/artifacts/` usando `joblib`. El nombre del archivo se controla con la variable de entorno `ACTIVE_MODEL` |
| `core/inference/entity_mapper.py` | Convierte una lista de entidades `Property` en un `DataFrame` de pandas con las columnas esperadas por el modelo |
| `core/inference/inference_pipeline.py` | Orquesta la predicción: llama al mapper y ejecuta `model.predict()` |
| `entities/properties.py` | Modelos Pydantic: `PropertyType` (enum House/Apartment), `Property` (entrada), `ClassifiedProperty` (salida con precio) |
| `entities/payload.py` | Modelos Pydantic para request (`PropertyPayload`) y response (`ResponsePropertyPayload`) del endpoint |
| `settings/` | Logger personalizado y carga de configuración desde YAML |
| `artifacts/` | Directorio donde se almacena el modelo serializado |

**Variables de entorno:**

| Variable | Descripción | Default |
|---|---|---|
| `ACTIVE_MODEL` | Nombre del archivo del modelo en `src/artifacts/` | `model.pkl` |

**Endpoints:**

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Verifica que el servicio esté activo |
| `POST` | `/properties-valuation/houses` | Predice el precio de una lista de propiedades |
| `GET` | `/docs` | Documentación interactiva Swagger (solo desarrollo) |

Ejemplo de request:

```json
POST /properties-valuation/houses

{
  "properties": [
    {
      "area": 120,
      "bedrooms": 3,
      "bathrooms": 2,
      "neighborhood": "Pocitos"
    }
  ]
}
```

Ejemplo de response:

```json
{
  "properties": [
    {
      "property": {
        "area": 120,
        "bedrooms": 3,
        "bathrooms": 2,
        "neighborhood": "Pocitos"
      },
      "predicted_price": 185000.0
    }
  ]
}
```

---

### `src/frontend` — Interfaz de usuario

Aplicación **Gradio** que permite ingresar las características de una o más propiedades de forma interactiva y solicitar la predicción al servicio de inferencia. Puerto: `8081`.

No contiene lógica de negocio ni realiza inferencias localmente.

| Módulo | Responsabilidad |
|---|---|
| `ui/ui_app.py` | Renderiza la interfaz Gradio, gestiona el estado de la lista de propiedades y realiza las llamadas HTTP al backend mediante `requests` |

**Variables de entorno:**

| Variable | Descripción | Default |
|---|---|---|
| `API_URL` | URL base del servicio de inferencia | `http://localhost:8080` |

---

## Requisitos previos

- [Docker](https://www.docker.com/) instalado y corriendo
- El archivo `src/backend/artifacts/model.pkl` debe existir antes de buildear (generado por el pipeline de entrenamiento)

---

## Comandos Docker

Buildear y levantar ambos servicios:

```bash
docker compose up --build
```

Levantar sin rebuildar (imágenes ya existentes):

```bash
docker compose up
```

Levantar en segundo plano:

```bash
docker compose up --build -d
```

Ver logs:

```bash
docker compose logs -f
```

Detener los servicios:

```bash
docker compose down
```

Una vez levantado:

| Servicio | URL |
|---|---|
| Interfaz web | http://localhost:8081 |
| API REST | http://localhost:8080 |
| Docs Swagger | http://localhost:8080/docs |

---

## Ejecución local (sin Docker)

**Backend:**

```bash
pip install -r src/backend/requirements.txt
python -m src.backend.api.app
```

**Frontend** (en otra terminal):

```bash
pip install -r src/frontend/requirements.txt
API_URL=http://localhost:8080 python -m src.frontend.ui.ui_app
```

---

## Despliegue en AWS

Ambos contenedores son desplegados en la misma **ECS Task** sobre **AWS Fargate**, compartiendo la misma interfaz de red. En ese escenario la variable `API_URL` del frontend se configura como `http://localhost:8080`, ya que ambos contenedores corren en el mismo host de red dentro de la tarea.

Las imágenes se almacenan en **Amazon ECR** y son referenciadas desde la definición de la tarea ECS.
