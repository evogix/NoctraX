#!/usr/bin/env python3
import argparse, trio, sys
from termcolor import colored
from .core import run_noctrax, __version__
from .banner import show_banner

def build_parser():
    p = argparse.ArgumentParser(
        prog="noctrax",
        description=f"NoctraX v{__version__} \u2014 VOID SPECTER by @faizalx1337 \u2014 Dark Ghost Trace // Hacker OSINT",
        epilog="IG: @faizalx1337 | Example: noctrax technicalsagar@gmail.com --only-used --silent"
    )
    p.add_argument("email", nargs="?", help="Target email")
    p.add_argument("--only-used", dest="only_used", action="store_true", help="Show only FOUND sites")
    p.add_argument("--silent", action="store_true", help="Clean output \u2014 only FOUND, no banner (output hata ke)")
    p.add_argument("--no-color", dest="no_color", action="store_true", help="No colors")
    p.add_argument("--no-clear", dest="no_clear", action="store_true", help="Do not clear screen")
    p.add_argument("--csv", dest="csv_out", action="store_true", help="Export CSV")
    p.add_argument("--json", dest="json_out", action="store_true", help="Export JSON")
    p.add_argument("--timeout", type=int, default=10, help="Timeout per request (default 10)")
    p.add_argument("--no-breach", dest="no_breach", action="store_true", help="Skip breach/gravatar check")
    p.add_argument("--version", action="store_true", help="Show version")
    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.version:
        print(f"NoctraX v{__version__} by @faizalx1337 \u2014 VOID SPECTER // Dark Protocol")
        sys.exit(0)
    if not args.email:
        show_banner(silent=args.silent)
        parser.print_help()
        print()
        print(colored("  \u2192 noctrax technicalsagar@gmail.com --only-used", "cyan"))
        print(colored("  \u2192 noctrax test@gmail.com --silent --json", "cyan"))
        sys.exit(1)
    try:
        trio.run(run_noctrax, args.email, args)
    except KeyboardInterrupt:
        print(colored("\n[!] Interrupted by user", "red"))
        sys.exit(0)

if __name__ == "__main__":
    main()
