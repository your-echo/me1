import aiosqlite
from config import ADMINS

DB_FILE = "bot_data.db"
DEFAULT_ROLE = "interested"  # внутренняя роль "Любопытный"


# ================== ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ ==================
async def add_user_if_not_exists(user_id: int, name: str, username: str):
    async with aiosqlite.connect(DB_FILE) as db:
        # есть ли уже пользователь
        async with db.execute(
            "SELECT role FROM users WHERE id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()

        # если нет — создаём
        if not row:
            role = "admin" if user_id in ADMINS else DEFAULT_ROLE
            await db.execute(
                "INSERT INTO users (id, name, username, role) VALUES (?, ?, ?, ?)",
                (user_id, name, username, role),
            )
            await db.commit()
        else:
            # если есть, но должен быть админом — повышаем
            current_role = row[0]
            if user_id in ADMINS and current_role != "admin":
                await db.execute(
                    "UPDATE users SET role = 'admin' WHERE id = ?",
                    (user_id,),
                )
                await db.commit()


# ================== ПОЛУЧИТЬ РОЛЬ ПОЛЬЗОВАТЕЛЯ ==================
async def get_user_role(user_id: int) -> str:
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute(
            "SELECT role FROM users WHERE id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else DEFAULT_ROLE


# ================== ПОЛУЧИТЬ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ ==================
async def get_all_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute(
            "SELECT id, name, username, role FROM users ORDER BY id"
        ) as cursor:
            return await cursor.fetchall()


# ================== ОБНОВИТЬ РОЛЬ ПОЛЬЗОВАТЕЛЯ ==================
async def update_user_role(user_id: int, new_role: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (new_role, user_id),
        )
        await db.commit()
