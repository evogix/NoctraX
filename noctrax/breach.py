import httpx

async def check_breach(email, client):
    """Check breach via xposedornot + haveibeenpwned free alternative"""
    results = {"breached": False, "sources": [], "details": None}
    try:
        r = await client.get(f"https://api.xposedornot.com/v1/check-email/{email}", timeout=8)
        if r.status_code == 200:
            j = r.json()
            breaches = j.get("breaches", [])
            if breaches and breaches[0] is not None:
                flat = []
                for b in breaches:
                    if isinstance(b, list):
                        flat.extend(b)
                    elif isinstance(b, str):
                        flat.append(b)
                if flat:
                    results["breached"] = True
                    results["sources"] = flat
                    results["details"] = j
    except Exception:
        pass
    return results

async def check_gravatar(email, client):
    import hashlib
    h = hashlib.md5(email.strip().lower().encode()).hexdigest()
    try:
        r = await client.get(f"https://en.gravatar.com/{h}.json", timeout=6, follow_redirects=True)
        if r.status_code == 200:
            j = r.json()
            entry = j.get("entry", [{}])[0]
            return {"found": True, "profile": entry.get("profileUrl"), "name": entry.get("displayName"), "raw": entry}
    except Exception:
        pass
    return {"found": False}
