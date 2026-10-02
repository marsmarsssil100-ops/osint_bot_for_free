import aiohttp

async def check_email(email: str) -> str:
    results = []
    
    import hashlib
    email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(gravatar_url) as resp:
                if resp.status == 200:
                    results.append("✅ Gravatar: Профиль найден!")
                else:
                    results.append("❌ Gravatar: Профиль не найден")
        except Exception:
            results.append("⚠️ Gravatar: Ошибка проверки")

    res_text = f"📧 Email Lookup ({email}):\n\n" + "\n".join(results)
    return res_text