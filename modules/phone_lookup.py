import phonenumbers
from phonenumbers import geocoder, carrier, timezone

async def check_phone(phone_number: str) -> str:
    try:
        parsed_num = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_num):
            return "Invalid or non-existent phone number."

        country = geocoder.country_name_for_number(parsed_num, "ru")
        region = geocoder.description_for_number(parsed_num, "ru")
        op_carrier = carrier.name_for_number(parsed_num, "ru")
        time_zones = timezone.time_zones_for_number(parsed_num)

        return (
            f"Phone Search Target: {phone_number}\n\n"
            f"Country: {country or 'N/A'}\n"
            f"Region: {region or 'N/A'}\n"
            f"Carrier: {op_carrier or 'N/A'}\n"
            f"Timezone: {', '.join(time_zones)}"
        )
    except Exception as e:
        return f"Phone lookup error: {e}"