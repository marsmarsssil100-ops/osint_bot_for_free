import aiohttp

async def check_username(username: str) -> dict:
    results = {}
    
    # Список сайтов для проверки
    sites = {
        "GitHub": {
            "url": f"https://github.com/{username}",
            "error_text": ["404 Not Found", "Not Found"]
        },
        "Telegram": {
            "url": f"https://t.me/{username}",
            "error_text": []  # Логика Telegram обрабатывается отдельно ниже
        },
        "FunStat": {
            "url": f"https://funstat.bot/{username}",
            "error_text": ["Not found", "404", "Канал не найден"]
        },
        "Steam": {
            "url": f"https://steamcommunity.com/id/{username}",
            "error_text": ["The specified profile could not be found", "Specified profile could not be found"]
        },
        "Reddit": {
            "url": f"https://www.reddit.com/user/{username}",
            "error_text": ["page not found", "nobody on Reddit goes by that name"]
        },
        "Pinterest": {
            "url": f"https://www.pinterest.com/{username}",
            "error_text": ["User not found", "404"]
        },
        "Twitch": {
            "url": f"https://www.twitch.tv/{username}",
            "error_text": ["content is unavailable", "404"]
        },
        "SoundCloud": {
            "url": f"https://soundcloud.com/{username}",
            "error_text": ["We can't find that user", "404"]
        },
        "VK": {
            "url": f"https://vk.com/{username}",
            "error_text": ["404 Not Found", "Страница удалена", "Заблокирована"]
        },
        "Habr": {
            "url": f"https://habr.com/ru/users/{username}",
            "error_text": ["Страница не найдена", "Пользователь не найден"]
        },
        "Pikabu": {
            "url": f"https://pikabu.ru/@{username}",
            "error_text": ["Пользователь не найден", "404"]
        }
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        for site, data in sites.items():
            url = data["url"]
            errors = data["error_text"]
            
            try:
                async with session.get(url, timeout=4, allow_redirects=True) as response:
                    if response.status == 200:
                        text = await response.text()
                        
                        # Проверка на наличие текста ошибки на странице
                        has_error = any(error.lower() in text.lower() for error in errors)
                        if has_error:
                            continue
                            
                        # Специфичная проверка для Telegram
                        if site == "Telegram":
                            if "If you have Telegram, you can contact" in text or "you can contact @" in text:
                                if "extra" not in text and "tgme_page_title" not in text:
                                    continue
                                if "tgme_page_extra" not in text and "Preview channel" not in text:
                                    continue

                        results[site] = url
            except Exception:
                continue
                
    return results