#!/usr/bin/env python3
import argparse, trio, sys
from termcolor import colored
from .core import run_noctrax, run_username, run_phone, __version__
from .banner import show_banner

def build_parser():
    p = argparse.ArgumentParser(
        prog="noctrax",
        description=f"NoctraX v{__version__} — VOID SPECTER by @faizalx1337 — Dark Ghost Trace // Email + Username + Phone OSINT",
        epilog="IG: @faizalx1337 | GitHub: github.com/evogix/NoctraX | Email: noctrax email@gmail.com | User: noctrax --username faizalx1337 | Phone: noctrax --phone +919876543210"
    )
    p.add_argument("email", nargs="?", help="Target email (or use --username / --phone)")
    p.add_argument("--username", dest="username", help="Target username to hunt (50+ sites)")
    p.add_argument("--phone", dest="phone", help="Target phone number (with country code, e.g. +919876543210)")
    p.add_argument("--only-used", dest="only_used", action="store_true", help="Show only FOUND")
    p.add_argument("--silent", action="store_true", help="Clean output — only FOUND (output hata ke)")
    p.add_argument("--no-color", dest="no_color", action="store_true", help="No colors")
    p.add_argument("--no-clear", dest="no_clear", action="store_true", help="Do not clear screen")
    p.add_argument("--csv", dest="csv_out", action="store_true", help="Export CSV")
    p.add_argument("--json", dest="json_out", action="store_true", help="Export JSON")
    p.add_argument("--timeout", type=int, default=10, help="Timeout per request (default 10)")
    p.add_argument("--no-breach", dest="no_breach", action="store_true", help="Skip breach/gravatar check (email only)")
    p.add_argument("--version", action="store_true", help="Show version")
    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.version:
        print(f"NoctraX v{__version__} by @faizalx1337 — VOID SPECTER // Dark Protocol")
        print("  Email: 76 sites + breach + gravatar")
        print("  Username: 50+ sites (GitHub, Insta, X, TikTok, etc)")
        print("  Phone: carrier + region + WhatsApp surface")
        sys.exit(0)
    # routing
    try:
        if args.username:
            trio.run(run_username, args.username, args)
        elif args.phone:
            trio.run(run_phone, args.phone, args)
        elif args.email:
            trio.run(run_noctrax, args.email, args)
        else:
            show_banner(silent=args.silent)
            parser.print_help()
            print()
            print(colored("  → noctrax technicalsagar@gmail.com --only-used", "cyan"))
            print(colored("  → noctrax --username faizalx1337 --only-used", "cyan"))
            print(colored("  → noctrax --phone +919876543210", "cyan"))
            print(colored("  → noctrax test@gmail.com --silent --json", "cyan"))
            sys.exit(1)
    except KeyboardInterrupt:
        print(colored("\n[!] Interrupted", "red"))
        sys.exit(0)

if __name__ == "__main__":
    main()
