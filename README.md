## Estructura del Proyecto

```
practico-4-2026/
├── docs/                        # Documentos relevantes para el proyecto
├── src/                         # Código fuente
│   ├── api/                     # Endpoints de la API
│   │   ├── routers/             # Definición de rutas
│   │   └── app.py               # Aplicación FastAPI
│   ├── core/                    # Lógica principal 
│   │   ├── classification          # Implementación del clasificador
│   │   └── preprocessing.py        # Lógica de preprocesamiento
|   ├── data_model               # Modelo de datos
│   ├── settings/                # Configuración
│   └── utils/                   # Utilidades
├── tests/                       # Tests unitarios
├── Dockerfile                   # Configuración de Docker
└── requirements.txt             # Dependencias del proyecto
```

### Manejo de Docker Compose

1. Construir ambos servicios

```bash
docker compose build
```

2. Levantar ambos servicios

```bash
docker compose up
```

3. Levantart reconstruyendo previamente:

```bash
docker compose up --build
```

4. Detener todos los servicios

```bash
docker compose down
```

5. URLs

Backend:

```
http://localhost:8080
```

Swagger:

```
http://localhost:8080/docs
```

Frontend (Gradio):

```
http://localhost:8081
```

### Ejemplos de llamados

1. Prueba de salud del server

```bash
 curl http://localhost:8080/health 
``` 
2. Pruebas en postman
   En la carpeta doc se encuentra el archivo properties_classification_api.postman.json que contiene ejemplos de llamados al api.
   Para utilizarlo instalar postman e inmportar el archivo como una colección.
