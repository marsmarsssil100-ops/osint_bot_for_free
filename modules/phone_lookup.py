import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type, PhoneNumberType

async def check_phone(phone_number: str) -> str:
    try:
        parsed_num = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_num):
            return "Invalid or non-existent phone number."

        country = geocoder.country_name_for_number(parsed_num, "en")
        region = geocoder.description_for_number(parsed_num, "en")
        op_carrier = carrier.name_for_number(parsed_num, "en")
        time_zones = timezone.time_zones_for_number(parsed_num)
        
        # Определение типа номера (мобильный / городской)
        num_type = number_type(parsed_num)
        type_str = "Mobile" if num_type == PhoneNumberType.MOBILE else "Fixed Line / Other"

        return (
            f"Phone Search Target: {phone_number}\n\n"
            f"Country: {country or 'N/A'}\n"
            f"Region: {region or 'N/A'}\n"
            f"Carrier: {op_carrier or 'N/A'}\n"
            f"Type: {type_str}\n"
            f"Timezone: {', '.join(time_zones)}"
        )
    except Exception as e:
        return f"Phone lookup error: {e}"