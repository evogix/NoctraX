from termcolor import colored
from colorama import init, Fore, Back, Style
init(autoreset=True)

BANNER = r"""
 ███╗   ██╗  ██████╗   ██████╗ ████████╗██████╗  █████╗ ██╗  ██╗
 ████╗  ██║ ██╔═══██╗ ██╔════╝ ╚══██╔══╝██╔══██╗██╔══██╗╚██╗██╔╝
 ██╔██╗ ██║ ██║   ██║ ██║         ██║   ██████╔╝███████║ ╚███╔╝ 
 ██║╚██╗██║ ██║   ██║ ██║         ██║   ██╔══██╗██╔══██║ ██╔██╗ 
 ██║ ╚████║ ╚██████╔╝ ╚██████╗    ██║   ██║  ██║██║  ██║██╔╝ ██╗
 ╚═╝  ╚═══╝  ╚═════╝   ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

TAGLINE = "Specter in the Void  •  by Md. Faizal (@faizalx1337)  •  v2.3"
SUBTAG  = "WE SEE WHAT YOU TRY TO HIDE"

def show_banner(silent=False):
    if silent:
        return
    # Professional hacker gradient: red banner + neon accents
    print(Fore.RED + Style.BRIGHT + BANNER + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + f"  {TAGLINE}" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + f"  {SUBTAG}" + Style.RESET_ALL)
    print(Fore.BLACK + Style.BRIGHT + "  " + "─" * 52 + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "  ◆ IG: " + Fore.WHITE + "@faizalx1337  " + Fore.CYAN + "◆ GitHub: " + Fore.WHITE + "github.com/evogix/NoctraX  " + Fore.CYAN + "◆ v2.3" + Style.RESET_ALL)
    print(Fore.BLACK + Style.BRIGHT + "  " + "─" * 52 + Style.RESET_ALL)
    print()
