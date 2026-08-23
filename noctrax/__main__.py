#!/usr/bin/env python3
import argparse, trio, sys, pathlib
from termcolor import colored
from .core import run_noctrax, run_username, run_phone, __version__
from .banner import show_banner
from .pipeline import extract_targets, detect_stdin, detect_file_arg

def build_parser():
    p = argparse.ArgumentParser(
        prog="noctrax",
        description=f"NoctraX v{__version__} — VOID SPECTER by @faizalx1337 — Dark Ghost Trace // Email + Username + Phone OSINT + PIPELINE",
        epilog="IG: @faizalx1337 | GitHub: github.com/evogix/NoctraX | Pipeline: cat file.txt | noctrax"
    )
    p.add_argument("input", nargs="?", help="Target email OR file path (auto-detect) | or pipe via cat file.txt | noctrax")
    p.add_argument("--username", dest="username", help="Target username to hunt (50+ sites)")
    p.add_argument("--phone", dest="phone", help="Target phone number (with country code, e.g. +91XXXXXXXXXX)")
    p.add_argument("--only-used", dest="only_used", action="store_true", help="Show only FOUND")
    p.add_argument("--silent", action="store_true", help="Clean output — only FOUND, no banner")
    p.add_argument("--no-color", dest="no_color", action="store_true", help="No colors")
    p.add_argument("--no-clear", dest="no_clear", action="store_true", help="Do not clear screen")
    p.add_argument("--csv", dest="csv_out", action="store_true", help="Export CSV")
    p.add_argument("--json", dest="json_out", action="store_true", help="Export JSON")
    p.add_argument("--timeout", type=int, default=10, help="Timeout per request (default 10)")
    p.add_argument("--no-breach", dest="no_breach", action="store_true", help="Skip breach/gravatar check (email only)")
    p.add_argument("--version", action="store_true", help="Show version")
    return p

async def run_pipeline(content, args):
    emails, phones, usernames = extract_targets(content)
    total = len(emails) + len(phones) + len(usernames)
    if total == 0:
        print(colored("[-] No email/phone/username found in input", "red"))
        print(colored("  Hint: file should contain emails like example@gmail.com, phones like +91XXXXXXXXXX, usernames like example_user", "yellow"))
        return
    # summary
    if not args.silent:
        print(colored(f"\n[*] Pipeline detected: {len(emails)} emails, {len(phones)} phones, {len(usernames)} usernames — total {total} targets", "cyan", attrs=["bold"]))
        if emails:
            print(colored(f"  Emails: {', '.join(emails[:5])}", "white"))
        if phones:
            print(colored(f"  Phones: {', '.join(phones[:5])}", "white"))
        if usernames:
            print(colored(f"  Users: {', '.join(usernames[:5])}", "white"))
        print()

    # Run sequentially for each type
    for email in emails:
        print(colored(f"\n{'='*60}", "red"))
        print(colored(f"  [PIPELINE] Email: {email}", "white", attrs=["bold"]))
        print(colored(f"{'='*60}", "red"))
        await run_noctrax(email, args)

    for phone in phones:
        print(colored(f"\n{'='*60}", "red"))
        print(colored(f"  [PIPELINE] Phone: {phone}", "white", attrs=["bold"]))
        print(colored(f"{'='*60}", "red"))
        await run_phone(phone, args)

    for user in usernames:
        print(colored(f"\n{'='*60}", "red"))
        print(colored(f"  [PIPELINE] Username: @{user}", "white", attrs=["bold"]))
        print(colored(f"{'='*60}", "red"))
        await run_username(user, args)

    if not args.silent:
        print(colored(f"\n[✓] Pipeline complete — {total} targets scanned", "green", attrs=["bold"]))
        print(colored(f"  NoctraX v{__version__} • IG: @faizalx1337 • github.com/evogix/NoctraX", "cyan"))

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.version:
        print(f"NoctraX v{__version__} by @faizalx1337 — VOID SPECTER // Dark Protocol")
        print("  Email: 76 sites + breach + gravatar")
        print("  Username: 50+ sites (GitHub, Insta, X, TikTok, etc)")
        print("  Phone: carrier + region + WhatsApp surface")
        print("  Pipeline: cat file.txt | noctrax (auto-detect mixed)")
        sys.exit(0)

    # PIPELINE MODE: stdin piped
    stdin_data = detect_stdin()
    if stdin_data:
        # stdin has content -> pipeline
        try:
            trio.run(run_pipeline, stdin_data, args)
        except KeyboardInterrupt:
            print(colored("\n[!] Interrupted", "red"))
            sys.exit(0)
        return

    # PIPELINE MODE: input is a file path
    if args.input:
        # check if input is file
        file_content = detect_file_arg(args.input)
        if file_content is not None:
            try:
                trio.run(run_pipeline, file_content, args)
            except KeyboardInterrupt:
                print(colored("\n[!] Interrupted", "red"))
                sys.exit(0)
            return
        # not a file, treat as email/username/phone via flags
        if args.username:
            trio.run(run_username, args.username, args)
            return
        if args.phone:
            trio.run(run_phone, args.phone, args)
            return
        # if input looks like email, run email
        # single target mode (backward compat)
        try:
            trio.run(run_noctrax, args.input, args)
        except KeyboardInterrupt:
            print(colored("\n[!] Interrupted", "red"))
            sys.exit(0)
        return

    # Flags alone
    try:
        if args.username:
            trio.run(run_username, args.username, args)
        elif args.phone:
            trio.run(run_phone, args.phone, args)
        else:
            show_banner(silent=args.silent)
            parser.print_help()
            print()
            print(colored("  → noctrax example@gmail.com --only-used", "cyan"))
            print(colored("  → noctrax --username example_user --only-used", "cyan"))
            print(colored("  → noctrax --phone +91XXXXXXXXXX", "cyan"))
            print(colored("  → cat file.txt | noctrax --only-used  (auto pipeline)", "cyan"))
            print(colored("  → noctrax targets.txt --only-used  (file pipeline)", "cyan"))
            sys.exit(1)
    except KeyboardInterrupt:
        print(colored("\n[!] Interrupted", "red"))
        sys.exit(0)

if __name__ == "__main__":
    main()
