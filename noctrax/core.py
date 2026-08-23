"""NoctraX Core - 100% Native, Native Dark"""
import time, re, json, sys
import httpx
import trio
from termcolor import colored
from .banner import show_banner
from .breach import check_breach, check_gravatar
from .sites_db import get_all_native_checkers, get_site_count

__version__ = "2.0"

EMAIL_RE = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def is_email(s):
    return bool(re.fullmatch(EMAIL_RE, s))

def print_noctrax(data, email, start_time, total_checked, args, breach_info=None, gravatar_info=None):
    def c(text, color):
        if args.no_color:
            return text
        return colored(text, color)

    if not args.silent and not args.no_clear:
        print("\033[H\033[J", end="")

    if not args.silent:
        print(c("═" * 60, "red"))
        pad = " " * ((60 - len(email) - 6)//2)
        print(c(f"{pad}▶ {email} ◀", "white"))
        if breach_info:
            if breach_info.get("breached"):
                src = ", ".join(breach_info["sources"][:5])
                print(c(f"  ☠️  BREACHED: {src} (+{len(breach_info['sources'])})", "red"))
            else:
                print(c("  ✅ No public breach (xposedornot)", "green"))
        if gravatar_info and gravatar_info.get("found"):
            print(c(f"  👤 Gravatar: {gravatar_info.get('profile')}", "cyan"))
        print(c("═" * 60, "red"))

    found = [d for d in data if d.get("exists")]
    rate = [d for d in data if d.get("rateLimit")]
    notfound = len(data) - len(found) - len(rate)
    show_all = not args.only_used

    for r in data:
        dom = r["domain"]
        if r.get("rateLimit") and show_all and not args.silent:
            print(c(f"[x] {dom:<25}  rate-limited", "yellow"))
        elif r.get("exists"):
            extra = ""
            if r.get("emailrecovery"):
                extra += f" {r['emailrecovery']}"
            print(c(f"[+] {dom:<25}  FOUND{extra}", "green"))
        elif show_all and not args.silent:
            print(c(f"[-] {dom:<25}  not found", "magenta"))

    if not args.json_out and not args.csv_out and not args.silent:
        print()
        print(c(f"  ✔ {len(found)} FOUND  ", "green") + c(f"• {notfound} not found • {len(rate)} rate-limit", "dark_grey") + c(f" • {total_checked} checked in {round(time.time()-start_time,2)}s", "white"))
        print(c("  ──────────────────────────────────────────────", "red"))
        print(c("  NoctraX v2.0  •  IG: @faizalx1337  •  github.com/evogix/NoctraX", "cyan"))

    if args.csv_out:
        import csv, datetime
        ts = int(datetime.datetime.now().timestamp())
        fname = f"noctrax_{ts}_{email.replace('@','_')}.csv"
        with open(fname, 'w', newline='', encoding='utf8') as f:
            if data:
                w = csv.DictWriter(f, fieldnames=data[0].keys())
                w.writeheader()
                w.writerows(data)
        print(c(f"\n[→] CSV: {fname}", "cyan"))
    if args.json_out:
        import datetime
        ts = int(datetime.datetime.now().timestamp())
        fname = f"noctrax_{ts}_{email.replace('@','_')}.json"
        payload = {"email": email, "breach": breach_info, "gravatar": gravatar_info, "elapsed": round(time.time()-start_time,2), "found": found, "all": data}
        with open(fname, 'w', encoding='utf8') as f:
            json.dump(payload, f, indent=2)
        print(c(f"[→] JSON: {fname}", "cyan"))
        if args.silent:
            print(json.dumps(payload, indent=2))

async def run_noctrax(email, args):
    start = time.time()
    if not is_email(email):
        print(colored("[-] Invalid email: ", "red") + email)
        sys.exit(1)

    show_banner(silent=args.silent)

    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
    timeout = httpx.Timeout(args.timeout)
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36"}

    out = []
    breach_info = None
    gravatar_info = None

    checkers = get_all_native_checkers()
    total = get_site_count()

    async with httpx.AsyncClient(limits=limits, timeout=timeout, headers=headers, follow_redirects=True) as client:
        if not args.no_breach:
            try:
                breach_info = await check_breach(email, client)
                gravatar_info = await check_gravatar(email, client)
            except Exception:
                breach_info = {"breached": False, "sources": []}
                gravatar_info = {"found": False}

        async with trio.open_nursery() as nursery:
            for fn in checkers:
                async def launch(f, e, c, o):
                    try:
                        await f(e, c, o)
                    except Exception:
                        o.append({"name": f.__name__, "domain": f.__name__+".com", "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
                nursery.start_soon(launch, fn, email, client, out)

    print_noctrax(out, email, start, total, args, breach_info, gravatar_info)
    return out
