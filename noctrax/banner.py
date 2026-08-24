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

TAGLINE = "Professional OSINT Tool  •  v2.3  •  by Md. Faizal"
SUBTAG  = "Email  •  Username  •  Phone  •  Pipeline"

def show_banner(silent=False):
    if silent:
        return
    print(Fore.CYAN + Style.BRIGHT + BANNER + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + f"  {TAGLINE}" + Style.RESET_ALL)
    print(Fore.WHITE + f"  {SUBTAG}" + Style.RESET_ALL)
    print(Fore.BLACK + Style.BRIGHT + "  " + "─" * 52 + Style.RESET_ALL)
    print(Fore.CYAN + "  IG: " + Fore.WHITE + "@faizalx1337  " + Fore.CYAN + "GitHub: " + Fore.WHITE + "github.com/evogix/NoctraX" + Style.RESET_ALL)
    print()
