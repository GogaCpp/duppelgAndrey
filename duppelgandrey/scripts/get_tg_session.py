from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio

from duppelgandrey.settings import settings


async def create_string_session():
    api_id = settings.api_id
    api_hash = settings.api_hash

    client = TelegramClient(StringSession(), api_id, api_hash)

    await client.start()

    session_string = client.session.save()
    print("Ваша строка сессии:")
    print(session_string)

    await client.disconnect()
    return session_string


if __name__ == "__main__":
    session_str = asyncio.run(create_string_session())
