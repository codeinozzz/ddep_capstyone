# Asistente Generativo Multimodal

Proyecto final CSAI-353: Aprendizaje Profundo e IA Generativa

## Descripcion

Asistente generativo multimodal que combina generacion de texto y generacion de imagenes para diseno arquitectonico. El sistema utiliza una arquitectura basada en API RESTful con capa de asistente que previene acceso directo a los modelos.

## Caracteristicas

- API RESTful con FastAPI
- Generacion de texto (especificaciones tecnicas)
- Generacion de imagenes (renders fotorrealistas con Stable Diffusion)
- Sistema de sesiones y gestion de conversaciones
- Frontend web intuitivo
- Arquitectura SOLID, KISS, DRY
- Containerizacion con Docker
- Pipeline CI/CD con GitHub Actions

## Arquitectura

```
src/
├── api/
│   ├── main.py                  # API principal con endpoints
│   ├── assistant.py             # Capa de asistente multimodal
│   └── session_manager.py       # Gestion de sesiones
├── models/
│   ├── design_generator.py      # Generacion de especificaciones
│   └── render_generator.py      # Generacion de imagenes
├── frontend/
│   ├── index.html              # Interfaz de usuario
│   ├── styles.css              # Estilos
│   └── app.js                  # Logica frontend
├── data/
│   └── materials_catalog.json  # Catalogo de materiales
├── Dockerfile                   # Configuracion Docker
└── docker-compose.yml           # Orquestacion de contenedores
```

## Endpoints API

### POST /api/chat
Interaccion con el asistente multimodal

Request:
```json
{
  "session_id": "uuid-optional",
  "message": "genera una cocina minimalista",
  "config": {
    "style": "minimalist",
    "default_mode": "auto",
    "max_steps": 50,
    "guidance_scale": 7.5
  }
}
```

Response:
```json
{
  "session_id": "uuid",
  "response_type": "multimodal",
  "text_content": "especificacion tecnica...",
  "image_url": "/api/images/filename.png",
  "metadata": {}
}
```

### PATCH /api/config/{session_id}
Actualizar configuracion del sistema

Request:
```json
{
  "style": "modern",
  "max_steps": 75,
  "guidance_scale": 8.0
}
```

### GET /api/history/{session_id}
Obtener historial de conversacion

Query params:
- limit (optional): numero de mensajes a retornar

Response:
```json
{
  "session_id": "uuid",
  "message_count": 10,
  "messages": [...]
}
```

## Instalacion y Uso

### Con Docker (Recomendado)

```bash
cd src
docker compose up --build
```

La aplicacion estara disponible en http://localhost:8000

### Instalacion Manual

```bash
cd src
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Uso del Frontend

1. Abrir http://localhost:8000 en el navegador
2. Se crea automaticamente una nueva sesion
3. Configurar estilo, modo y parametros en el panel superior
4. Escribir solicitud en el campo de texto
5. El asistente determina automaticamente si generar texto, imagen o ambos

Ejemplos de solicitudes:
- "genera una cocina minimalista"
- "mostrar render de fachada rustica"
- "especificacion tecnica de sala moderna grande"

## Sistema de Prompts

El asistente analiza la intencion del usuario mediante keywords:

- Palabras clave para imagenes: render, imagen, foto, visualizar, mostrar
- Palabras clave para especificaciones: especificacion, detalles, materiales, presupuesto, tecnico
- Modo auto: genera ambos si no se especifica

## Estilos Disponibles

- rustic
- brutalism
- minimalist
- industrial
- modern
- mediterranean
- scandinavian
- contemporary_luxury

## Espacios Disponibles

- facade (fachada)
- living_room (sala)
- kitchen (cocina)
- bathroom (bano)
- bedroom (dormitorio)
- office (oficina)
- restaurant (restaurante)
- store (tienda)

## CI/CD Pipeline

El proyecto incluye GitHub Actions para:
- Verificacion de estilo de codigo
- Build de imagen Docker
- Test de contenedor

## Principios de Diseno

- SOLID: Separacion de responsabilidades en capas (API, Asistente, Modelos)
- KISS: Codigo simple y directo, sin abstracciones innecesarias
- DRY: Reutilizacion de componentes (SessionManager, MultimodalAssistant)

## Requisitos del Sistema

- Python 3.12+
- Docker y Docker Compose
- GPU NVIDIA con CUDA (opcional, mejora rendimiento)
- 8GB RAM minimo, 16GB recomendado
- 10GB espacio en disco para modelos

## Consideraciones de Produccion

- El sistema usa modelos grandes (Stable Diffusion ~5GB)
- Primera ejecucion descarga modelos de HuggingFace
- GPU acelera generacion de imagenes significativamente
- Sesiones se mantienen en memoria (usar Redis para produccion)

## Licencia

Proyecto academico CSAI-353
