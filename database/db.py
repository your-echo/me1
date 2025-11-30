import aiosqlite

DB_FILE = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                role TEXT DEFAULT 'interested',
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_all_users():
    query = "SELECT id, name, username, role FROM users ORDER BY id"
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute(query) as cursor:
            return await cursor.fetchall()



