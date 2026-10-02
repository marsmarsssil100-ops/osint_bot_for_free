import hashlib
import aiohttp

async def check_email(email: str) -> str:
    results = []
    email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(gravatar_url, timeout=5) as resp:
                if resp.status == 200:
                    results.append("Gravatar: Profile Found")
                else:
                    results.append("Gravatar: Profile Not Found")
    except Exception:
        results.append("Gravatar: Check Failed")

    return f"Email Lookup Results ({email}):\n\n" + "\n".join(results)