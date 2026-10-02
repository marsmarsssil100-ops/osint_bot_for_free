import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


def get_reg_date(user_id: int) -> str:
    if user_id < 10000000:
        return "2013 - 2014"
    elif user_id < 100000000:
        return "~2015 - 2016"
    elif user_id < 500000000:
        return "~2017 - 2018"
    elif user_id < 1000000000:
        return "~2019 - 2020"
    elif user_id < 2000000000:
        return "~2021 - 2022"
    elif user_id < 6000000000:
        return "~2023 - 2024"
    else:
        return "~2025 - 2026"


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "⚡ **OSINT Intelligence Bot**\n\n"
        "Send me a Telegram User ID, phone number, or email to perform a lookup.\n"
        "You can also **forward any message** from a user to extract their ID and metadata.",
        parse_mode="Markdown"
    )


@dp.message(F.forward_from)
async def process_forwarded_user(message: types.Message):
    user = message.forward_from
    user_id = user.id
    username = f"@{user.username}" if user.username else "N/A"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    reg_date = get_reg_date(user_id)

    sangmata_link = f"https://t.me/SangMataInfo_bot?start={user_id}"

    text = (
        f"👤 **Forwarded User Intel:**\n\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"📛 **Name:** {full_name}\n"
        f"🔗 **Username:** {username}\n"
        f"📅 **Estimated Reg Date:** {reg_date}\n\n"
        f"🛠 **External OSINT Tools:**\n"
        f"• Username History (SangMata): [Check Bot]({sangmata_link})\n"
        f"• Direct Profile: [Open Link](https://t.me/{user.username if user.username else ''})"
    )
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)


@dp.message(F.forward_sender_name)
async def process_hidden_forward(message: types.Message):
    await message.answer(
        "⚠️ **Privacy Restriction:**\n"
        "This user has hidden their account link in forwarded messages.",
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))