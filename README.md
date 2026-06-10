# Arquitectura de la solución

La solución se diseñó siguiendo una arquitectura basada en dos servicios independientes: un **Backend** encargado de exponer la API de clasificación y un **Frontend** que proporciona una interfaz gráfica desarrollada con Gradio.

Ambos componentes se encuentran en un mismo repositorio (monorepo), pero son construidos y desplegados de forma independiente mediante imágenes Docker diferentes.

```
                    Usuario
                       │
                Navegador Web
                       │
              http://<ip>:8081
                       │
               ┌─────────────────┐
               │   Frontend UI   │
               │     Gradio      │
               └─────────────────┘
                       │
            HTTP REST (JSON)
                       │
               http://localhost:8080
                       │
               ┌─────────────────┐
               │   Backend API   │
               │     FastAPI     │
               └─────────────────┘
                       │
             Modelo de Machine Learning
```

---

# Organización del proyecto

El proyecto se encuentra organizado como un monorepo, separando claramente las responsabilidades de cada componente.

```
src/
├── backend/
│   ├── api/
│   ├── core/
│   ├── entities/
│   ├── settings/
│   ├── utils/
│   ├── Dockerfile
│   └── requirements.txt
│
└── frontend/
    ├── ui/
    ├── Dockerfile
    └── requirements.txt
```

Cada componente posee:

* Dockerfile propio
* Dependencias independientes
* Imagen Docker independiente

---

# Backend

El Backend implementa una API REST utilizando **FastAPI**.

Sus responsabilidades son:

* recibir solicitudes de clasificación;
* validar el payload mediante Pydantic;
* ejecutar el pipeline de inferencia;
* devolver la clasificación en formato JSON.

Este servicio expone, entre otros, los siguientes endpoints:

```
GET  /health

POST /properties-valuation/houses
```

Durante el desarrollo también se dispone automáticamente de la documentación Swagger:

```
/docs
```

---

# Frontend

El Frontend implementa una interfaz gráfica utilizando **Gradio**.

Su única responsabilidad consiste en:

* solicitar los datos al usuario;
* construir el payload JSON;
* consumir la API REST del Backend;
* mostrar los resultados de la clasificación.

La UI no contiene ninguna lógica de negocio ni realiza inferencias localmente.

---

# Comunicación entre servicios

La comunicación entre ambos componentes se realiza mediante HTTP REST.

Durante el desarrollo local, Docker Compose crea automáticamente una red privada donde ambos servicios pueden comunicarse utilizando el nombre del servicio.

```
Frontend
      │
      │ HTTP POST
      ▼
http://api:8080
```

En producción, ambos contenedores se ejecutan dentro de la misma **ECS Task**, compartiendo la misma interfaz de red. En este escenario el Frontend consume la API mediante:

```
http://localhost:8080
```

La dirección utilizada se configura mediante la variable de entorno:

```
API_URL
```

---

# Contenedores Docker

Cada componente posee una imagen Docker independiente.

```
Imagen Backend
──────────────
Python
FastAPI
Modelo ML

Imagen Frontend
───────────────
Python
Gradio
Requests
```

Esta separación permite actualizar cualquiera de los dos componentes sin necesidad de reconstruir el otro.

---

# Docker Compose

Durante el desarrollo se utiliza Docker Compose para levantar ambos servicios de forma conjunta.

```
docker compose up --build
```

Compose se encarga de:

* construir ambas imágenes;
* crear una red privada;
* iniciar ambos contenedores;
* configurar la comunicación entre ellos.

---

# Despliegue en AWS

El despliegue se realiza utilizando **Amazon ECS sobre AWS Fargate**.

La arquitectura desplegada es la siguiente:

```
Internet
     │
Public IP
     │
┌──────────────────────────┐
│ ECS Service              │
│                          │
│  ECS Task                │
│  ┌────────────────────┐  │
│  │ Backend Container  │  │
│  │ FastAPI            │  │
│  └────────────────────┘  │
│                          │
│  ┌────────────────────┐  │
│  │ Frontend Container │  │
│  │ Gradio             │  │
│  └────────────────────┘  │
└──────────────────────────┘
```

Cada contenedor utiliza una imagen almacenada en **Amazon Elastic Container Registry (ECR)**.

La UI es el componente expuesto al usuario final, mientras que el Backend procesa las solicitudes de clasificación realizadas desde la interfaz.

