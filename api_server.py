import asyncio
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from config import ADMINS
from database.knowledge_db import (
    init_knowledge_db,
    get_sections,
    get_materials,
    add_section,
    add_material,
    deactivate_section,
    deactivate_material,
)

# ------------------------------------
#  ПРАВИЛЬНО СОЗДАЁМ FastAPI
# ------------------------------------
app = FastAPI(title="Луч света API")

# ------------------------------------
#  ПРАВИЛЬНО ДОБАВЛЯЕМ CORS (теперь работает)
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # можно ограничить позже
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
#   МОДЕЛИ
# ----------------------
class SectionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    position: int = 0


class MaterialCreate(BaseModel):
    section_id: int
    title: str
    type: str
    payload: str
    position: int = 0


# ----------------------
#   ПРОВЕРКА АДМИНА
# ----------------------
def check_admin(user_id: int):
    if user_id not in ADMINS:
        raise HTTPException(status_code=403, detail="Forbidden: not admin")


# ----------------------
#   СТАРТ API
# ----------------------
@app.on_event("startup")
async def on_startup():
    await init_knowledge_db()
    print("✅ knowledge.db initialized")


# ----------------------
#   PING
# ----------------------
@app.get("/api/ping")
async def ping():
    return {"status": "ok", "message": "Луч света API online"}


# ----------------------
#   СПИСОК РАЗДЕЛОВ
# ----------------------
@app.get("/api/sections")
async def api_get_sections():
    rows = await get_sections()
    return [
        {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "position": r[3],
        }
        for r in rows
    ]


# ----------------------
#   СОЗДАТЬ РАЗДЕЛ
# ----------------------
@app.post("/api/sections")
async def api_create_section(
    payload: SectionCreate,
    user_id: int = Query(...),
):
    check_admin(user_id)
    await add_section(payload.title, payload.description, payload.position)
    return {"status": "ok"}


# ----------------------
#   ДЕАКТИВАЦИЯ РАЗДЕЛА
# ----------------------
@app.delete("/api/sections/{section_id}")
async def api_delete_section(
    section_id: int,
    user_id: int = Query(...),
):
    check_admin(user_id)
    await deactivate_section(section_id)
    return {"status": "ok"}


# ----------------------
#   МАТЕРИАЛЫ РАЗДЕЛА
# ----------------------
@app.get("/api/sections/{section_id}/materials")
async def api_get_materials(section_id: int):
    rows = await get_materials(section_id)
    return [
        {
            "id": r[0],
            "title": r[1],
            "type": r[2],
            "payload": r[3],
            "position": r[4],
        }
        for r in rows
    ]


# ----------------------
#   СОЗДАТЬ МАТЕРИАЛ
# ----------------------
@app.post("/api/materials")
async def api_create_material(
    payload: MaterialCreate,
    user_id: int = Query(...),
):
    check_admin(user_id)
    await add_material(
        section_id=payload.section_id,
        title=payload.title,
        type_=payload.type,
        payload=payload.payload,
        position=payload.position,
    )
    return {"status": "ok"}


# ----------------------
#   ДЕАКТИВАЦИЯ МАТЕРИАЛА
# ----------------------
@app.delete("/api/materials/{material_id}")
async def api_delete_material(
    material_id: int,
    user_id: int = Query(...),
):
    check_admin(user_id)
    await deactivate_material(material_id)
    return {"status": "ok"}
