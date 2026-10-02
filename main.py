import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
import config
from modules.username import check_username

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


def get_reg_date(user_id: int) -> str:
    if user_id < 10000000:
        return "2013 - 2014"
    elif user_id < 100000000:
        return "2015 - 2016"
    elif user_id < 500000000:
        return "2017 - 2018"
    elif user_id < 1000000000:
        return "2019 - 2020"
    elif user_id < 2000000000:
        return "2021 - 2022"
    elif user_id < 6000000000:
        return "2023 - 2024"
    else:
        return "2025 - 2026"


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "OSINT Intelligence Bot\n\n"
        "Send username or use /search <username>.\n"
        "Forward message from target to parse ID and metadata.",
        parse_mode="Markdown"
    )


@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Usage: /search <username>")
        return

    username = args[1].replace("@", "").strip()
    await process_username_search(message, username)


@dp.message(F.forward_from)
async def process_forwarded_user(message: types.Message):
    user = message.forward_from
    user_id = user.id
    username_str = user.username if user.username else "N/A"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    reg_date = get_reg_date(user_id)

    sangmata_link = f"https://t.me/SangMataInfo_bot?start={user_id}"
    direct_link = f"https://t.me/{user.username}" if user.username else f"tg://user?id={user_id}"

    text = (
        f"Forwarded User Intel:\n\n"
        f"ID: {user_id}\n"
        f"Name: {full_name}\n"
        f"Username: @{username_str}\n"
        f"Estimated Reg Date: {reg_date}\n\n"
        f"SangMata History: {sangmata_link}\n"
        f"Direct Link: {direct_link}"
    )
    await message.answer(text, disable_web_page_preview=True)


@dp.message(F.forward_sender_name)
async def process_hidden_forward(message: types.Message):
    await message.answer("Privacy Restriction: User hidden account link in forwarded messages.")


@dp.message(F.text)
async def handle_text_search(message: types.Message):
    username = message.text.replace("@", "").strip()
    await process_username_search(message, username)


async def process_username_search(message: types.Message, username: str):
    status_msg = await message.answer(f"Searching OSINT sources for {username}...")
    
    results = await check_username(username)
    
    if not results:
        await status_msg.edit_text(f"No public accounts found for {username}.")
        return

    links = "\n".join([f"{site}: {url}" for site, url in results.items()])
    text = f"OSINT Search Results for {username}:\n\n{links}"
    
    await status_msg.edit_text(text, disable_web_page_preview=True)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))