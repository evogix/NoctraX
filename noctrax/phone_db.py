"""NoctraX Phone DB - Dark Carrier Intel"""
import re

# Try phonenumbers lib, fallback to regex
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    HAS_PHONENUMBERS = True
except ImportError:
    HAS_PHONENUMBERS = False

async def phone_intel(phone, client, out):
    """Carrier + region + validity + WhatsApp/Telegram surface"""
    clean = re.sub(r"[^\d+]", "", phone)
    info = {"raw": phone, "clean": clean, "valid": False, "possible": False, "country": None, "carrier": None, "region": None, "timezone": None, "type": None}
    if HAS_PHONENUMBERS:
        try:
            parsed = phonenumbers.parse(clean, None if clean.startswith("+") else "IN")
            info["valid"] = phonenumbers.is_valid_number(parsed)
            info["possible"] = phonenumbers.is_possible_number(parsed)
            info["country"] = geocoder.description_for_number(parsed, "en")
            info["carrier"] = carrier.name_for_number(parsed, "en")
            info["region"] = geocoder._country_code_for_number(parsed) if hasattr(geocoder, '_country_code_for_number') else str(parsed.country_code)
            info["type"] = str(phonenumbers.number_type(parsed))
            try:
                tz = timezone.time_zones_for_number(parsed)
                info["timezone"] = list(tz)[:2]
            except:
                pass
            info["e164"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            info["national"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        except Exception as e:
            info["error"] = str(e)
    else:
        # regex fallback
        info["valid"] = bool(re.match(r"^\+?\d{10,15}$", clean))
        info["country"] = "Unknown (install phonenumbers for details)"

    # Surface checks (best effort, no API key)
    surface = []
    # WhatsApp check via wa.me - if wa.me/<num> returns 200 with "WhatsApp" it's valid format
    try:
        # Use e164 without +
        num = info.get("e164", clean).lstrip("+")
        r = await client.get(f"https://wa.me/{num}", headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=False, timeout=6)
        # wa.me redirects to whatsapp if valid (302), 404 or 400 if invalid
        if r.status_code in [200, 302]:
            surface.append({"platform": "whatsapp", "url": f"https://wa.me/{num}", "exists": True})
        else:
            surface.append({"platform": "whatsapp", "url": f"https://wa.me/{num}", "exists": False})
    except Exception:
        surface.append({"platform": "whatsapp", "url": f"https://wa.me/{clean}", "exists": False, "rateLimit": True})

    # Telegram - t.me/+number not reliable, but check
    try:
        # Telegram usernames are not phone numbers, so we just note
        surface.append({"platform": "telegram", "note": "Phone -> Telegram requires app check (manual)", "exists": None})
    except:
        pass

    # Truecaller-like hint (needs API, skip but note)
    surface.append({"platform": "truecaller", "note": "Use Truecaller app for name lookup", "exists": None})

    out.append({"type": "phone_intel", "info": info, "surface": surface})
    return info, surface

def format_phone_info(info):
    lines = []
    lines.append(f"  Number: {info.get('e164', info.get('clean'))} ({info.get('national','')})")
    lines.append(f"  Valid: {info.get('valid')} | Possible: {info.get('possible')}")
    if info.get("country"):
        lines.append(f"  Country/Region: {info.get('country')} (+{info.get('region','')})")
    if info.get("carrier"):
        lines.append(f"  Carrier: {info.get('carrier')}")
    if info.get("type"):
        lines.append(f"  Type: {info.get('type')}")
    if info.get("timezone"):
        lines.append(f"  Timezone: {', '.join(info.get('timezone'))}")
    return "\n".join(lines)
