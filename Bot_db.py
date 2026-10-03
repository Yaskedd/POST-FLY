import aiosqlite

db_name = 'bot_db.sqliteU'

async def init_db():
    async with aiosqlite.connect(db_name) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chat_id(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER NOT NULL,
                         channel_id INTEGER UNIQUE NOT NULL,
                         name_chanel TEXT)                    
                        """)
        await db.commit()

async def add_id(user_id, id, name_chanel):
    async with aiosqlite.connect(db_name) as db:
        await db.execute(
            "INSERT OR IGNORE INTO chat_id (user_id,channel_id, name_chanel) VALUES(?, ?, ?)", (user_id,id, name_chanel)) # OR IGNORE - если число уже есть,то ничего не добавится и ошибки не будет
        await db.commit()

async def delete_id(channel_id,name_chanel):
    async with aiosqlite.connect(db_name) as db:
        await db.execute(
            "DELETE FROM chat_id WHERE channel_id = ? AND name_chanel = ?",
            (channel_id,name_chanel)
        )
        await db.commit()

async def get_user_id(channel_id):
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(
            "SELECT user_id FROM chat_id WHERE channel_id = ?",
            (channel_id,)
        )
        result = await cursor.fetchone()
        if result is None:
            return None

        return result[0]
async def get_chat_id(user_id):
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(
            "SELECT channel_id FROM chat_id WHERE user_id = ?",
            (user_id,)
        )
        result = await cursor.fetchall()

        # условие ниже для проверки на привязку бота
        if result is None:
            return None
        return result
    # как я понял функция не будет возвращать нам список всех channel_id из таблицы,а только тот,чей айди мы указали в параметре

async def name_id(user_id):
    async with aiosqlite.connect(db_name) as db: 
        cursor = await db.execute(
            "SELECT name_chanel,channel_id FROM chat_id WHERE user_id = ?", (user_id,))
        result = await cursor.fetchall()
        return result

