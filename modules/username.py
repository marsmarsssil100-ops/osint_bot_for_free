import aiohttp

async def check_username(username: str) -> dict:
    results = {}
    
    # Расширенный список популярных ресурсов и форумов
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Telegram": f"https://t.me/{username}",
        "VK": f"https://vk.com/{username}",
        "Habr": f"https://habr.com/ru/users/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "D3 (TJ/Mull)": f"https://d3.ru/user/{username}/posts",
        "Pikabu": f"https://pikabu.ru>@{username}" # Базовая проверка
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        for site, url in sites.items():
            try:
                async with session.get(url, timeout=4, allow_redirects=True) as response:
                    if response.status == 200:
                        text = await response.text()
                        
                        # СПЕЦИАЛЬНАЯ ПРОВЕРКА ДЛЯ TELEGRAM
                        if site == "Telegram":
                            # Если на странице есть эта фраза или нет кнопки "Send Message", аккаунта не существует
                            if "If you have Telegram, you can contact" in text or "you can contact @" in text:
                                if "extra" not in text and "tgme_page_title" not in text:
                                    continue
                                # Доп проверка: если телеграм пишет "you can contact @username right away", но нет заголовка профиля
                                if "tgme_page_extra" not in text and "Preview channel" not in text:
                                    continue

                        # ПРОВЕРКА ДЛЯ STEAM (если профиль не найден, Steam возвращает 200, но пишет сообщение)
                        if site == "Steam" and "The specified profile could not be found" in text:
                            continue

                        results[site] = url
            except Exception:
                continue
                
    return results