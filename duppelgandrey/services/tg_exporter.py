
import json
from typing import AsyncGenerator
from duppelgandrey.settings import settings
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Dialog
import logging


class TgMessageExporter():
    def __init__(self, target_person_ids: set[int]):
        self.target_person_ids = target_person_ids

    async def connect_client(self):
        logging.info("Connecting to Telegram client...")
        self.client = TelegramClient(StringSession(settings.tg_token), settings.api_id, settings.api_hash)
        await self.client.start()

    async def disconnect_client(self):
        logging.info("Disconnecting from Telegram client...")
        await self.client.disconnect()

    async def get_dialogs(self) -> AsyncGenerator[Dialog, None]:
        async for d in self.client.iter_dialogs():
            if d.entity.id in self.target_person_ids:
                yield d

    async def get_messages(self, dialog: Dialog):
        logging.info(f"Getting messages from {dialog.entity.username}...")
        messages_data = []
        async for message in self.client.iter_messages(dialog.entity, limit=100):
            if message.text:
                msg_data = {
                    'id': message.id,
                    'date': message.date.isoformat(),
                    'out': message.out,
                    'text': message.text,
                    'reply_to_msg_id': message.reply_to_msg_id
                }
                messages_data.append(msg_data)
        logging.info(f"Got {len(messages_data)} messages from {dialog.entity.username}")
        return messages_data

    async def save_to_file(self, messages_data: list[dict], target_person: str):
        with open(f'chat_with_{target_person}.json', 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

    async def export_chat_history(self):
        try:
            await self.connect_client()
            async for dialog in self.get_dialogs():
                messages_data = await self.get_messages(dialog)
                await self.save_to_file(messages_data, dialog.entity.username)
            await self.disconnect_client()
        except Exception as e:
            await self.disconnect_client()
            raise Exception(e)
