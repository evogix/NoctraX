from termcolor import colored

BANNER = r"""
███╗   ██╗  ██████╗   ██████╗ ████████╗██████╗  █████╗ ██╗  ██╗
████╗  ██║ ██═══██╗ ██╔════╝ ╚══██╔══╝██╔══██╗██╔══██╗╚██╗██╔╝
██╔██╗ ██║ ██║   ██║ ██║         ██║   ██████╔╝███████║ ╚███╔╝ 
██║╚██╗██║ ██║   ██║ ██║         ██║   ██╔══██╗██╔══██║ ██╔██╗ 
██║ ╚████║ ╚██████╔╝ ╚██████╗    ██║   ██║  ██║██║  ██║██╔╝ ██╗
╚═╝  ╚═══╝  ╚═════╝   ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

TAGLINE = "Specter in the Void  \u2022  by @faizalx1337  \u2022  v2.0-dark"
SUBTAG  = "WE SEE WHAT YOU TRY TO HIDE"

def show_banner(silent=False):
    if silent:
        return
    print(colored(BANNER, "red", attrs=["bold"]))
    print(colored(f"  {TAGLINE}", "white", attrs=["bold"]))
    print(colored(f"  {SUBTAG}", "red", attrs=["bold"]))
    print(colored("  \u2500"*25, "dark_grey"))
    print(colored("  IG: @faizalx1337  |  GitHub: github.com/evogix/NoctraX", "cyan"))
    print()
