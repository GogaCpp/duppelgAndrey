import asyncio
import logging

from duppelgandrey.services.tg_exporter import TgMessageExporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def export_tg_chat_history():
    tg_exporter = TgMessageExporter(target_person_ids=[1043597669])
    await tg_exporter.export_chat_history()


def main():
    asyncio.run(export_tg_chat_history())


if __name__ == '__main__':
    main()
