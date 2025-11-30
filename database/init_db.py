import aiosqlite

DB_FILE = "bot_data.db"


async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT,
                role TEXT
            )
        """)
        await db.commit()
