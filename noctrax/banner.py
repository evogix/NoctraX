from colorama import init, Fore, Style
init(autoreset=True)

BANNER = r"""
 ███╗   ██╗  ██████╗   ██████╗ ████████╗██████╗  █████╗ ██╗  ██╗
 ████╗  ██║ ██═══██╗ ██╔════╝ ╚══██╔══╝██╔══██╗██╔══██╗╚██╗██╔╝
 ██╔██╗ ██║ ██║   ██║ ██║         ██║   ██████╔╝███████║ ╚███╔╝ 
 ██║╚██╗██║ ██║   ██║ ██║         ██║   ██╔══██╗██╔══██║ ██╔██╗ 
 ██║ ╚████║ ╚██████╔╝ ╚██████╗    ██║   ██║  ██║██║  ██║██╔╝ ██╗
 ╚═╝  ╚═══╝  ╚═════╝   ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

TAGLINE = "OSINT Tool  •  v2.3  •  by Md. Faizal"
SUBTAG  = "WE SEE WHAT YOU TRY TO HIDE"

def show_banner(silent=False):
    if silent:
        return
    print(Fore.RED + Style.BRIGHT + BANNER + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + f"  {TAGLINE}" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + f"  {SUBTAG}" + Style.RESET_ALL)
    print(Fore.BLACK + Style.BRIGHT + "  " + "─" * 52 + Style.RESET_ALL)
    print(Fore.CYAN + "  IG: " + Fore.WHITE + "@faizalx1337  " + Fore.CYAN + "GitHub: " + Fore.WHITE + "github.com/evogix/NoctraX" + Style.RESET_ALL)
    print()
