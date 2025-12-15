from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import os

from session_manager import SessionManager, Message
from assistant import MultimodalAssistant

app = FastAPI(title="Asistente Generativo Multimodal")

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_manager = SessionManager()
assistant = MultimodalAssistant()


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    config: Optional[Dict] = None


class ConfigUpdate(BaseModel):
    style: Optional[str] = None
    default_mode: Optional[str] = None
    max_steps: Optional[int] = None
    guidance_scale: Optional[float] = None


class ChatResponse(BaseModel):
    session_id: str
    response_type: str
    text_content: Optional[str] = None
    image_url: Optional[str] = None
    metadata: Dict


@app.get("/", response_class=HTMLResponse)
def read_root():
    frontend_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(frontend_path):
        with open(frontend_path, "r") as f:
            return f.read()
    return {
        "service": "Asistente Generativo Multimodal",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "service": "Asistente Generativo Multimodal",
        "version": "1.0.0",
        "status": "running",
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id

    if not session_id:
        session_id = session_manager.create_session()

    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if request.config:
        session.update_config(request.config)

    user_message = Message(role="user", content=request.message, message_type="text")
    session.add_message(user_message)

    response = assistant.process_request(request.message, session.config)

    response_type = response.get("type", "text")
    text_content = response.get("text_content")
    image_path = response.get("image_path")

    image_url = None
    if image_path:
        image_url = f"/api/images/{os.path.basename(image_path)}"

    assistant_content = text_content or f"Imagen generada: {image_url}"
    assistant_message = Message(
        role="assistant",
        content=assistant_content,
        message_type=response_type,
        metadata=response.get("metadata", {}),
    )
    session.add_message(assistant_message)

    return ChatResponse(
        session_id=session_id,
        response_type=response_type,
        text_content=text_content,
        image_url=image_url,
        metadata=response.get("metadata", {}),
    )


@app.patch("/api/config/{session_id}")
def update_config(session_id: str, config: ConfigUpdate):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    updates = config.dict(exclude_unset=True)
    session.update_config(updates)

    return {"session_id": session_id, "config": session.config}


@app.get("/api/history/{session_id}")
def get_history(session_id: str, limit: Optional[int] = None):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    history = session.get_history(limit=limit)

    return {
        "session_id": session_id,
        "message_count": len(history),
        "messages": history,
    }


@app.get("/api/sessions")
def get_sessions():
    sessions = session_manager.get_all_sessions()
    return {"count": len(sessions), "sessions": sessions}


@app.post("/api/sessions")
def create_session():
    session_id = session_manager.create_session()
    return {"session_id": session_id, "created": True}


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    session_manager.delete_session(session_id)
    return {"session_id": session_id, "deleted": True}


@app.get("/api/options")
def get_options():
    return assistant.get_available_options()


@app.get("/api/images/{filename}")
def get_image(filename: str):
    image_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "outputs/renders", filename
    )

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
