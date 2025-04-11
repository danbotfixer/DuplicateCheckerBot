import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import F
import logging

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

posted_tags = set()
posted_teams = set()

def extract_tags_and_teams(text):
    lines = text.strip().split("\n")
    current_team = None
    tags = []
    teams = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("@"):
            tags.append(line)
            if current_team:
                teams.append(current_team)
        else:
            current_team = line
    return tags, teams

@dp.message(F.chat.type == "channel")
async def check_duplicates(message: Message):
    tags, teams = extract_tags_and_teams(message.text or "")
    duplicates = []

    for tag in tags:
        if tag in posted_tags:
            duplicates.append(tag)
        else:
            posted_tags.add(tag)

    for team in teams:
        if team in posted_teams:
            duplicates.append(team)
        else:
            posted_teams.add(team)

    if duplicates:
        duplicate_text = "\n".join(f"⚠️ Повтор: {item}" for item in duplicates)
        await bot.send_message(chat_id=message.chat.id, text=f"<b>Обнаружены дубликаты:</b>\n{duplicate_text}", reply_to_message_id=message.message_id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
