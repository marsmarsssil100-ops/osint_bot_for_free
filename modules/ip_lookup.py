import aiohttp

async def check_ip(ip_address: str) -> str:
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "success":
                        return (
                            f"IP Lookup Results ({ip_address}):\n\n"
                            f"Country: {data.get('country')}\n"
                            f"Region: {data.get('regionName')}\n"
                            f"City: {data.get('city')}\n"
                            f"ISP: {data.get('isp')}\n"
                            f"Org: {data.get('org')}\n"
                            f"ASN: {data.get('as')}"
                        )
                    else:
                        return f"IP Lookup Failed: {data.get('message', 'Invalid IP')}"
    except Exception:
        pass
    return "Error querying IP database."