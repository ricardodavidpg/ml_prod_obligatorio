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

### Manejo de Docker

1. Construir la imagen:

   ```bash
   docker build -t property-classification-api .
   ```
2. Ejecutar el contenedor:

   ```bash
   # Ejecutar en modo detached
   docker run -d -p 8080:8080 text-classification-api

   # Ver logs
   docker logs -f <container_id>
   ```
3. Borrar contenedores e imágenes

   ```bash
   # Borrar todos los contenedores
   docker stop $(docker ps -a -q)
   docker rm $(docker ps -a -q)    

   # Borrar todas las imágenes
   docker rmi -f $(docker images -q)
   ```

### Prueba 

1. Prueba de salud del server

```bash
 curl http://localhost:8080/health 
``` 
2. Pruebas en postman
   En la carpeta doc se encuentra el archivo properties_classification_api.postman.json que contiene ejemplos de llamados al api.
   Para utilizarlo instalar postman e inmportar el archivo como una colección.
