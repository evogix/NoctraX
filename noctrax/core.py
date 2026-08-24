"""NoctraX Core — WE SEE WHAT YOU TRY TO HIDE by Md. Faizal"""
import time, re, json, sys
import httpx
import trio
from termcolor import colored
from colorama import init as colorama_init, Fore, Style
colorama_init(autoreset=True)
from .banner import show_banner
from .breach import check_breach, check_gravatar
from .sites_accurate import get_accurate_checkers, get_accurate_count
from .username_db import run_username_scan, USERNAME_SITES
from .phone_db import phone_intel, format_phone_info

__version__ = "2.3"

EMAIL_RE = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def is_email(s):
    return bool(re.fullmatch(EMAIL_RE, s))

def cprint(text, color="white", bright=False, no_color=False):
    if no_color:
        return text
    col = getattr(Fore, color.upper(), Fore.WHITE) if hasattr(Fore, color.upper()) else Fore.WHITE
    style = Style.BRIGHT if bright else ""
    return col + style + text + Style.RESET_ALL

def print_noctrax(data, email, start_time, total_checked, args, breach_info=None, gravatar_info=None):
    no_col = args.no_color
    if not args.silent and not args.no_clear:
        print("\033[H\033[J", end="")
    if not args.silent:
        # Pro header - hacker box
        print(Fore.RED + Style.BRIGHT + "  ╔" + "═"*58 + "╗" + Style.RESET_ALL if not no_col else "  ╔" + "═"*58 + "╗")
        pad = " " * ((58 - len(email) - 4)//2)
        print(cprint(f"  ║{pad} ► {email} ◄{pad}║", "white", True, no_col))
        print(Fore.RED + Style.BRIGHT + "  ╚" + "═"*58 + "╝" + Style.RESET_ALL if not no_col else "  ╚" + "═"*58 + "╝")
        if breach_info:
            if breach_info.get("breached"):
                sources = breach_info["sources"]
                print(Fore.RED + Style.BRIGHT + f"  ☠  BREACHED in {len(sources)} leaks:" + Style.RESET_ALL if not no_col else f"  BREACHED in {len(sources)} leaks:")
                # Show all breach sources with numbering
                for idx, src in enumerate(sources, 1):
                    print(Fore.RED + f"     {idx:2}. {src}" + Style.RESET_ALL if not no_col else f"     {idx}. {src}")
                    if idx >= 30 and len(sources) > 30:
                        remaining = len(sources) - 30
                        print(Fore.YELLOW + f"     ... and {remaining} more (see JSON export)" + Style.RESET_ALL if not no_col else f"     ... and {remaining} more")
                        break
            else:
                print(Fore.GREEN + f"  ✔  No public breach (xposedornot)" + Style.RESET_ALL if not no_col else "  No breach")
        if gravatar_info and gravatar_info.get("found"):
            print(Fore.CYAN + f"  ● Gravatar: {gravatar_info.get('profile')}" + Style.RESET_ALL if not no_col else f"  Gravatar: {gravatar_info.get('profile')}")
        print(Fore.BLACK + Style.BRIGHT + "  ─" * 60 + Style.RESET_ALL if not no_col else "  " + "-"*60)
    found = [d for d in data if d.get("exists")]
    rate = [d for d in data if d.get("rateLimit")]
    notfound = len(data) - len(found) - len(rate)
    show_all = not args.only_used
    for r in data:
        dom = r["domain"]
        if r.get("rateLimit") and show_all and not args.silent:
            print(Fore.YELLOW + f"  [×] {dom:<26}  rate-limited" + Style.RESET_ALL if not no_col else f"  [x] {dom} rate-limited")
        elif r.get("exists"):
            extra = ""
            if r.get("emailrecovery"):
                extra += f" {r['emailrecovery']}"
            print(Fore.GREEN + Style.BRIGHT + f"  [+] {dom:<26}  ● FOUND{extra}" + Style.RESET_ALL if not no_col else f"  [+] {dom} FOUND")
        elif show_all and not args.silent:
            print(Fore.MAGENTA + Style.DIM + f"  [-] {dom:<26}  not found" + Style.RESET_ALL if not no_col else f"  [-] {dom} not found")
    if not args.json_out and not args.csv_out and not args.silent:
        print()
        print(Fore.GREEN + Style.BRIGHT + f"  ✔ {len(found)} FOUND" + Style.RESET_ALL + Fore.WHITE + f"  •  {notfound} not found" + Fore.YELLOW + f" • {len(rate)} rate-limit" + Fore.CYAN + f"  •  {total_checked} checked in {round(time.time()-start_time,2)}s" + Style.RESET_ALL if not no_col else f"  {len(found)} FOUND • {notfound} not found • {len(rate)} rate-limit • {total_checked} checked")
        print(Fore.RED + "  ──────────────────────────────────────────────────────" + Style.RESET_ALL if not no_col else "  " + "-"*54)
        print(Fore.CYAN + Style.BRIGHT + "  ◆ NoctraX v2.3  " + Fore.WHITE + "•  " + Fore.CYAN + "Md. Faizal  " + Fore.WHITE + "•  " + Fore.CYAN + "IG: @faizalx1337  " + Fore.WHITE + "•  " + Fore.CYAN + "github.com/evogix/NoctraX" + Style.RESET_ALL if not no_col else "  NoctraX v2.3 • Md. Faizal • @faizalx1337 • github.com/evogix/NoctraX")
    if args.csv_out:
        import csv, datetime
        ts = int(datetime.datetime.now().timestamp())
        fname = f"noctrax_{ts}_{email.replace('@','_')}.csv"
        with open(fname, 'w', newline='', encoding='utf8') as f:
            if data:
                w = csv.DictWriter(f, fieldnames=data[0].keys())
                w.writeheader()
                w.writerows(data)
        print(Fore.CYAN + f"\n  → CSV: {fname}" + Style.RESET_ALL if not no_col else f" CSV:{fname}")
    if args.json_out:
        import datetime
        ts = int(datetime.datetime.now().timestamp())
        fname = f"noctrax_{ts}_{email.replace('@','_')}.json"
        payload = {"email": email, "breach": breach_info, "gravatar": gravatar_info, "elapsed": round(time.time()-start_time,2), "found": found, "all": data}
        with open(fname, 'w', encoding='utf8') as f:
            json.dump(payload, f, indent=2)
        print(Fore.CYAN + f"  → JSON: {fname}" + Style.RESET_ALL if not no_col else f" JSON:{fname}")
        if args.silent:
            print(json.dumps(payload, indent=2))

def print_username(data, username, start_time, args):
    no_col = args.no_color
    if not args.silent and not args.no_clear:
        print("\033[H\033[J", end="")
    if not args.silent:
        print(Fore.RED + Style.BRIGHT + "  ╔" + "═"*58 + "╗" + Style.RESET_ALL if not no_col else "  ╔" + "═"*58 + "╗")
        pad = " " * ((58 - len(username) - 6)//2)
        print(cprint(f"  ║{pad} ► @{username} ◄{pad}║", "white", True, no_col))
        print(Fore.RED + Style.BRIGHT + "  ║" + " "*18 + "WE SEE WHAT YOU TRY TO HIDE" + " "*15 + "║" + Style.RESET_ALL if not no_col else f"  WE SEE WHAT YOU TRY TO HIDE")
        print(Fore.RED + Style.BRIGHT + "  ╚" + "═"*58 + "╝" + Style.RESET_ALL if not no_col else "  ╚" + "═"*58 + "╝")
    found = [d for d in data if d.get("exists")]
    rate = [d for d in data if d.get("rateLimit")]
    show_all = not args.only_used
    for r in data:
        dom = r["domain"]
        url = r.get("url", "")
        if r.get("rateLimit") and show_all and not args.silent:
            print(Fore.YELLOW + f"  [×] {dom:<22}  rate-limited" + Style.RESET_ALL if not no_col else f"  [x] {dom} rate-limited")
        elif r.get("exists"):
            print(Fore.GREEN + Style.BRIGHT + f"  [+] {dom:<22}  ● FOUND  → " + Fore.CYAN + f"{url}" + Style.RESET_ALL if not no_col else f"  [+] {dom} FOUND -> {url}")
        elif show_all and not args.silent:
            print(Fore.MAGENTA + Style.DIM + f"  [-] {dom:<22}  not found" + Style.RESET_ALL if not no_col else f"  [-] {dom} not found")
    if not args.json_out and not args.csv_out and not args.silent:
        print()
        print(Fore.GREEN + Style.BRIGHT + f"  ✔ {len(found)} FOUND" + Style.RESET_ALL + Fore.WHITE + f"  •  {len(data)-len(found)-len(rate)} not found" + Fore.YELLOW + f" • {len(rate)} rate-limit" + Fore.CYAN + f"  •  {len(data)} checked in {round(time.time()-start_time,2)}s" + Style.RESET_ALL if not no_col else f"  {len(found)} FOUND")
        print(Fore.RED + "  ──────────────────────────────────────────────────────" + Style.RESET_ALL if not no_col else "  " + "-"*54)
        print(Fore.CYAN + Style.BRIGHT + "  ◆ NoctraX v2.3 — Username Hunt  " + Fore.WHITE + "•" + Fore.CYAN + "  Md. Faizal  " + Fore.WHITE + "•" + Fore.CYAN + "  @faizalx1337" + Style.RESET_ALL if not no_col else "  Username Hunt • Md. Faizal")
    if args.csv_out:
        import csv, datetime
        ts = int(datetime.datetime.now().timestamp())
        fname = f"noctrax_user_{ts}_{username}.csv"
        with open(fname, 'w', newline='', encoding='utf8') as f:
            if data:
                w = csv.DictWriter(f, fieldnames=data[0].keys())
                w.writeheader()
                w.writerows(data)
        print(Fore.CYAN + f"\n  → CSV: {fname}" + Style.RESET_ALL if not no_col else f" CSV:{fname}")
    if args.json_out:
        import datetime
        ts = int(datetime.datetime.now().timestamp())
        fname = f"noctrax_user_{ts}_{username}.json"
        payload = {"username": username, "elapsed": round(time.time()-start_time,2), "found": found, "all": data}
        with open(fname, 'w', encoding='utf8') as f:
            json.dump(payload, f, indent=2)
        print(Fore.CYAN + f"  → JSON: {fname}" + Style.RESET_ALL if not no_col else f" JSON:{fname}")
        if args.silent:
            print(json.dumps(payload, indent=2))

def print_phone(info, surface, phone, start_time, args):
    no_col = args.no_color
    if not args.silent and not args.no_clear:
        print("\033[H\033[J", end="")
    if not args.silent:
        print(Fore.RED + Style.BRIGHT + "  ╔" + "═"*58 + "╗" + Style.RESET_ALL if not no_col else "  ╔" + "═"*58 + "╗")
        pad = " " * ((58 - len(phone) - 4)//2)
        print(cprint(f"  ║{pad} ► {phone} ◄{pad}║", "white", True, no_col))
        print(Fore.RED + Style.BRIGHT + "  ║" + " "*18 + "WE SEE WHAT YOU TRY TO HIDE" + " "*15 + "║" + Style.RESET_ALL if not no_col else f"  WE SEE WHAT YOU TRY TO HIDE")
        print(Fore.RED + Style.BRIGHT + "  ╚" + "═"*58 + "╝" + Style.RESET_ALL if not no_col else "  ╚" + "═"*58 + "╝")
        print(Fore.CYAN + Style.BRIGHT + format_phone_info(info) + Style.RESET_ALL if not no_col else format_phone_info(info))
        print(Fore.BLACK + Style.BRIGHT + "  ─" * 60 + Style.RESET_ALL if not no_col else "  " + "-"*60)
        for s in surface:
            plat = s.get("platform", "")
            if s.get("exists") is True:
                print(Fore.GREEN + Style.BRIGHT + f"  [+] {plat:<15}  ● FOUND → " + Fore.CYAN + f"{s.get('url','')}" + Style.RESET_ALL if not no_col else f"  [+] {plat} FOUND")
            elif s.get("exists") is False:
                print(Fore.MAGENTA + Style.DIM + f"  [-] {plat:<15}  not found" + Style.RESET_ALL if not no_col else f"  [-] {plat} not found")
            else:
                print(Fore.YELLOW + f"  [?] {plat:<15}  {s.get('note','')}" + Style.RESET_ALL if not no_col else f"  [?] {plat} {s.get('note','')}")
        print()
        print(Fore.CYAN + f"  ⏱  {round(time.time()-start_time,2)}s  •  NoctraX v2.3 — Phone Intel  •  Md. Faizal • @faizalx1337" + Style.RESET_ALL if not no_col else f"  {round(time.time()-start_time,2)}s • Phone Intel")

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
    checkers = get_accurate_checkers()
    total = get_accurate_count()
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

async def run_username(username, args):
    start = time.time()
    show_banner(silent=args.silent)
    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
    timeout = httpx.Timeout(args.timeout)
    out = []
    async with httpx.AsyncClient(limits=limits, timeout=timeout, follow_redirects=True) as client:
        await run_username_scan(username, client, out)
    print_username(out, username, start, args)
    return out

async def run_phone(phone, args):
    start = time.time()
    show_banner(silent=args.silent)
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=30)
    timeout = httpx.Timeout(args.timeout)
    out = []
    info = {}
    surface = []
    async with httpx.AsyncClient(limits=limits, timeout=timeout, follow_redirects=True) as client:
        info, surface = await phone_intel(phone, client, out)
    if out and out[0].get("type") == "phone_intel":
        info = out[0]["info"]
        surface = out[0]["surface"]
    print_phone(info, surface, phone, start, args)
    return out
