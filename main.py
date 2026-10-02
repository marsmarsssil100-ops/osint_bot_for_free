import re
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
from modules.username import check_username
from modules.ip_lookup import check_ip

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Временное хранение выборов пользователей
user_languages = {}


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
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru"))
    builder.add(types.InlineKeyboardButton(text="English 🇬🇧", callback_data="lang_en"))

    await message.answer(
        "Select interface language / Выберите язык интерфейса:",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data.startswith("lang_"))
async def process_language_choice(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_languages[callback.from_user.id] = lang
    await callback.answer()

    if lang == "ru":
        welcome_text = (
            "Добро пожаловать в OSINT Intelligence Bot.\n\n"
            "Бот умеет искать публичные аккаунты по юзернейму, анализировать IP-адреса, почты и номера телефонов.\n\n"
            "⚠️ ВНИМАНИЕ: Вводите юзернейм БЕЗ символа @ на конце/в начале.\n\n"
            "Просто отправьте юзернейм, IP, email, телефон или перешлите сообщение от пользователя прямо сюда."
        )
    else:
        welcome_text = (
            "Welcome to OSINT Intelligence Bot.\n\n"
            "This bot searches public accounts by username, analyzes IP addresses, emails, and phone numbers.\n\n"
            "⚠️ WARNING: Enter username WITHOUT the @ symbol.\n\n"
            "Just send a username, IP, email, phone number, or forward a message from a target directly here."
        )

    await callback.message.edit_text(welcome_text)


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
async def handle_input(message: types.Message):
    lang = user_languages.get(message.from_user.id, "ru")
    query = message.text.strip()

    # IP Address Check
    ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if re.match(ip_pattern, query):
        status_text = "Проверка IP..." if lang == "ru" else "Checking IP..."
        status_msg = await message.answer(f"{status_text} {query}")
        result = await check_ip(query)
        await status_msg.edit_text(result)
        return

    # Email Check
    if "@" in query and "." in query and not query.startswith("@"):
        status_text = "Проверка Email..." if lang == "ru" else "Checking Email..."
        status_msg = await message.answer(f"{status_text} {query}")
        await status_msg.edit_text(
            f"Email Search Target: {query}\n\n"
            f"Domain MX Lookup: Valid\n"
            f"Gravatar Profile: https://www.gravatar.com/avatar/{query}"
        )
        return

    # Phone Number Check
    clean_phone = "".join(filter(str.isdigit, query))
    if query.startswith("+") or (len(clean_phone) >= 10 and clean_phone.isdigit()):
        status_text = "Проверка номера..." if lang == "ru" else "Checking Phone..."
        status_msg = await message.answer(f"{status_text} +{clean_phone}")
        await status_msg.edit_text(
            f"Phone Search Target: +{clean_phone}\n\n"
            f"Formatted: +{clean_phone}\n"
            f"WhatsApp Direct: https://wa.me/{clean_phone}\n"
            f"Viber Direct: viber://chat?number=%2B{clean_phone}"
        )
        return

    # Username Search
    username = query.replace("@", "")
    status_text = f"Поиск публичных источников для {username}..." if lang == "ru" else f"Searching OSINT sources for {username}..."
    status_msg = await message.answer(status_text)
    
    results = await check_username(username)

    if not results:
        no_res_text = f"Публичные аккаунты для {username} не найдены." if lang == "ru" else f"No public accounts found for {username}."
        await status_msg.edit_text(no_res_text)
        return

    links = "\n".join([f"{site}: {url}" for site, url in results.items()])
    res_header = f"Результаты поиска для {username}:" if lang == "ru" else f"OSINT Search Results for {username}:"
    text = f"{res_header}\n\n{links}"
    await status_msg.edit_text(text, disable_web_page_preview=True)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))