import aiosqlite
from config import DB_FILE


# ================== СОЗДАТЬ ТАБЛИЦУ ==================
async def init_teachers_table():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                name TEXT,
                bio TEXT,
                telegram TEXT,
                whatsapp TEXT,
                email TEXT,
                photo_file_id TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)
        await db.commit()


# ================== ДОБАВИТЬ УЧИТЕЛЯ ==================
async def add_teacher(user_id: int):
    async with aiosqlite.connect(DB_FILE) as db:

        async with db.execute(
            "SELECT id FROM teachers WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            exists = await cursor.fetchone()

        if exists:
            await db.execute(
                "UPDATE teachers SET is_active = 1 WHERE user_id = ?",
                (user_id,),
            )
            await db.commit()
            return

        async with db.execute(
            "SELECT name FROM users WHERE id = ?",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()

        name = row[0] if row else "Без имени"

        await db.execute(
            "INSERT INTO teachers (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        await db.commit()


# ================== ПОЛУЧИТЬ СПИСОК АКТИВНЫХ ==================
async def get_active_teachers():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute(
            "SELECT id, name FROM teachers WHERE is_active = 1"
        ) as cursor:
            return await cursor.fetchall()


# ================== ПОЛУЧИТЬ ОДНОГО УЧИТЕЛЯ ==================
async def get_teacher_by_id(teacher_id: int):
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute(
            "SELECT * FROM teachers WHERE id = ? AND is_active = 1",
            (teacher_id,)
        ) as cursor:
            return await cursor.fetchone()


# ================== ОБНОВИТЬ ПОЛЕ УЧИТЕЛЯ ==================
async def update_teacher_field(teacher_id: int, field: str, value: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            f"UPDATE teachers SET {field} = ? WHERE id = ?",
            (value, teacher_id)
        )
        await db.commit()
