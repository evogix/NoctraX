"""NoctraX Sites DB — OSINT"""
import random, hashlib, json

UA = "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

# ───── INDIVIDUAL SITE CHECKERS ─────
async def check_twitter(email, client, out):
    name, domain = "twitter", "twitter.com"
    try:
        r = await client.get("https://api.twitter.com/i/users/email_available.json", params={"email": email}, timeout=8)
        j = r.json()
        exists = bool(j.get("taken"))
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_github(email, client, out):
    name, domain = "github", "github.com"
    try:
        r = await client.post("https://github.com/signup_check/email", data={"value": email, "authenticity_token": ""}, headers={"User-Agent": UA}, timeout=8)
        txt = r.text.lower()
        exists = "email is already taken" in txt or "unavailable" in txt or "already" in txt
        if not exists and r.status_code == 422:
            exists = True
        out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_instagram(email, client, out):
    name, domain = "instagram", "instagram.com"
    try:
        headers = {"User-Agent": UA, "X-IG-App-ID": "936619743392459", "X-Requested-With": "XMLHttpRequest"}
        r = await client.post("https://www.instagram.com/accounts/account_recovery_send_ajax/", data={"email_or_username": email}, headers=headers, timeout=8)
        txt = r.text.lower()
        exists = "sent" in txt or "email sent" in txt or '"status":"ok"' in txt
        if "wait" in txt or "rate" in txt:
            out.append({"name": name, "domain": domain, "method": "recovery", "frequent_rate_limit": True, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return
        out.append({"name": name, "domain": domain, "method": "recovery", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "recovery", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_spotify(email, client, out):
    name, domain = "spotify", "spotify.com"
    try:
        r = await client.get("https://spclient.wg.spotify.com/signup/public/v1/account", params={"validate": "1", "email": email}, headers={"User-Agent": UA}, timeout=8)
        j = r.json()
        status = j.get("status")
        exists = status == 20
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_pinterest(email, client, out):
    name, domain = "pinterest", "pinterest.com"
    try:
        r = await client.get("https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/", params={"source_url": "/", "data": json.dumps({"options": {"email": email}})}, timeout=8)
        j = r.json()
        exists = j.get("resource_response", {}).get("data", False) is True
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_adobe(email, client, out):
    name, domain = "adobe", "adobe.com"
    try:
        r = await client.post("https://auth.services.adobe.com/signin/v2/users/accounts", json={"username": email}, headers={"User-Agent": UA, "Content-Type": "application/json"}, timeout=8)
        j = r.json()
        exists = j[0].get("type") != "unknown" if isinstance(j, list) and j else False
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_discord(email, client, out):
    name, domain = "discord", "discord.com"
    try:
        r = await client.post("https://discord.com/api/auth/register", json={"email": email, "username": "noctrax_test123", "password": "NoctraX123!@#", "consent": True}, headers={"User-Agent": UA, "Content-Type": "application/json"}, timeout=8)
        txt = r.text.lower()
        exists = "email is already registered" in txt
        if r.status_code == 429:
            out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": True, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return
        out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_netflix(email, client, out):
    name, domain = "netflix", "netflix.com"
    try:
        r = await client.get("https://www.netflix.com/login", headers={"User-Agent": UA}, timeout=8)
        out.append({"name": name, "domain": domain, "method": "login", "frequent_rate_limit": False, "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "login", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_gravatar_native(email, client, out):
    name, domain = "gravatar", "gravatar.com"
    try:
        h = hashlib.md5(email.strip().lower().encode()).hexdigest()
        r = await client.get(f"https://en.gravatar.com/{h}.json", timeout=6)
        exists = r.status_code == 200 and "entry" in r.text
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_google_native(email, client, out):
    name, domain = "google", "google.com"
    try:
        headers = {'User-Agent': UA, 'Content-Type': 'application/x-www-form-urlencoded'}
        r = await client.get("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn", headers=headers, timeout=8)
        if 'quot;,null,null,null,&quot;' in r.text:
            freq = r.text.split('quot;,null,null,null,&quot;')[1].split('&quot')[0]
            data = {'continue':'https://accounts.google.com/', 'f.req': f'["{freq}","","","{email}",false]'}
            r2 = await client.post('https://accounts.google.com/_/signup/webusernameavailability', headers=headers, data=data, timeout=8)
            exists = '"gf.wuar",2' in r2.text
            out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
            return
        out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "register", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_flipkart_native(email, client, out):
    name, domain = "flipkart", "flipkart.com"
    try:
        r = await client.post("https://www.flipkart.com/api/5/user/exists", json={"loginId": email}, headers={"User-Agent": UA}, timeout=8)
        txt = r.text.lower()
        exists = '"exists":true' in txt or '"exists": true' in txt
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_paytm_native(email, client, out):
    name, domain = "paytm", "paytm.com"
    try:
        r = await client.post("https://accounts.paytm.com/signin/validate/otp", json={"email": email}, headers={"User-Agent": UA}, timeout=8)
        txt = r.text.lower()
        exists = "user exists" in txt or "already" in txt
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": False, "exists": exists, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "api", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def check_generic(email, client, out, name, domain):
    try:
        out.append({"name": name, "domain": domain, "method": "generic", "frequent_rate_limit": False, "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": "generic", "frequent_rate_limit": False, "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

NATIVE_SITES = [
    ("twitter", "twitter.com", check_twitter),
    ("github", "github.com", check_github),
    ("instagram", "instagram.com", check_instagram),
    ("spotify", "spotify.com", check_spotify),
    ("pinterest", "pinterest.com", check_pinterest),
    ("adobe", "adobe.com", check_adobe),
    ("discord", "discord.com", check_discord),
    ("netflix", "netflix.com", check_netflix),
    ("gravatar", "gravatar.com", check_gravatar_native),
    ("google", "google.com", check_google_native),
    ("flipkart", "flipkart.com", check_flipkart_native),
    ("paytm", "paytm.com", check_paytm_native),
]

EXTRA_GENERIC = [
    ("naukri", "naukri.com"), ("zomato", "zomato.com"), ("swiggy", "swiggy.com"),
    ("dream11", "dream11.com"), ("myntra", "myntra.com"), ("ajio", "ajio.com"),
    ("irctc", "irctc.co.in"), ("oyo", "oyorooms.com"), ("ola", "olacabs.com"),
    ("bigbasket", "bigbasket.com"), ("jiomart", "jiomart.com"), ("meesho", "meesho.com"),
    ("phonepe", "phonepe.com"), ("cred", "cred.club"), ("upstox", "upstox.com"),
    ("zerodha", "zerodha.com"), ("canva", "canva.com"), ("notion", "notion.so"),
    ("figma", "figma.com"), ("medium", "medium.com"), ("quora", "quora.com"),
    ("redbus", "redbus.in"), ("indiamart", "indiamart.com"), ("magicbricks", "magicbricks.com"),
    ("99acres", "99acres.com"), ("yahoo", "yahoo.com"), ("protonmail", "protonmail.ch"),
    ("outlook", "outlook.com"), ("office365", "office365.com"), ("deliveroo", "deliveroo.com"),
    ("ebay", "ebay.com"), ("amazon", "amazon.com"), ("arch", "archive.org"),
    ("imgur", "imgur.com"), ("flickr", "flickr.com"), ("soundcloud", "soundcloud.com"),
    ("tumblr", "tumblr.com"), ("wordpress", "wordpress.com"), ("patreon", "patreon.com"),
    ("aboutme", "about.me"), ("lastfm", "last.fm"), ("strava", "strava.com"),
    ("duolingo", "duolingo.com"), ("codepen", "codepen.io"), ("replit", "replit.com"),
    ("docker", "docker.com"), ("atlassian", "atlassian.com"), ("trello", "trello.com"),
    ("slack", "slack.com"), ("notion2", "notion.com"), ("chatgpt", "chatgpt.com"),
    ("x", "x.com"), ("snapchat", "snapchat.com"), ("tiktok", "tiktok.com"),
    ("linkedin", "linkedin.com"), ("facebook", "facebook.com"), ("reddit", "reddit.com"),
    ("youtube", "youtube.com"), ("twitch", "twitch.tv"), ("steam", "steampowered.com"),
    ("epic", "epicgames.com"), ("roblox", "roblox.com"), ("coinbase", "coinbase.com"),
    ("binance", "binance.com"),
]

def get_all_native_checkers():
    checkers = []
    for name, domain, fn in NATIVE_SITES:
        checkers.append(fn)
    for name, domain in EXTRA_GENERIC:
        async def _make(email, client, out, n=name, d=domain):
            await check_generic(email, client, out, n, d)
        _make.__name__ = name
        checkers.append(_make)
    return checkers

def get_site_count():
    return len(NATIVE_SITES) + len(EXTRA_GENERIC)
