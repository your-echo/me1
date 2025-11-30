import aiosqlite

# Отдельная база для WebApp
KNOWLEDGE_DB = "knowledge.db"


# ==========================
#   ИНИЦИАЛИЗАЦИЯ БАЗЫ
# ==========================
async def init_knowledge_db():
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:

        # Таблица разделов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                position INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        """)

        # Таблица материалов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                type TEXT NOT NULL,        -- file, link, text
                payload TEXT NOT NULL,     -- file_id, URL или текст
                position INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (section_id) REFERENCES knowledge_sections(id)
            )
        """)

        await db.commit()


# ==========================
#   РАЗДЕЛЫ (SECTIONS)
# ==========================
async def add_section(title: str, description: str | None = None, position: int = 0):
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        await db.execute(
            """
            INSERT INTO knowledge_sections (title, description, position)
            VALUES (?, ?, ?)
            """,
            (title, description, position)
        )
        await db.commit()


async def get_sections():
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        cursor = await db.execute("""
            SELECT id, title, description, position
            FROM knowledge_sections
            WHERE is_active = 1
            ORDER BY position, id
        """)
        return await cursor.fetchall()


async def get_section(section_id: int):
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        cursor = await db.execute("""
            SELECT id, title, description, position, is_active
            FROM knowledge_sections
            WHERE id = ?
        """, (section_id,))
        return await cursor.fetchone()


async def deactivate_section(section_id: int):
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        await db.execute(
            "UPDATE knowledge_sections SET is_active = 0 WHERE id = ?",
            (section_id,)
        )
        await db.commit()


# ==========================
#   МАТЕРИАЛЫ (MATERIALS)
# ==========================
async def add_material(section_id: int, title: str, type_: str, payload: str, position: int = 0):
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        await db.execute(
            """
            INSERT INTO knowledge_materials
                (section_id, title, type, payload, position)
            VALUES (?, ?, ?, ?, ?)
            """,
            (section_id, title, type_, payload, position)
        )
        await db.commit()


async def get_materials(section_id: int):
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        cursor = await db.execute("""
            SELECT id, title, type, payload, position
            FROM knowledge_materials
            WHERE section_id = ? AND is_active = 1
            ORDER BY position, id
        """, (section_id,))
        return await cursor.fetchall()


async def get_material(material_id: int):
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        cursor = await db.execute("""
            SELECT id, section_id, title, type, payload, position, is_active
            FROM knowledge_materials
            WHERE id = ?
        """, (material_id,))
        return await cursor.fetchone()


async def deactivate_material(material_id: int):
    async with aiosqlite.connect(KNOWLEDGE_DB) as db:
        await db.execute(
            "UPDATE knowledge_materials SET is_active = 0 WHERE id = ?",
            (material_id,)
        )
        await db.commit()
