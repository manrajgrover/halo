import platform
from colorama import init, Fore
from termcolor import colored

init(autoreset=True)

def is_supported():
    """Check whether operating system supports main symbols or not.

    Returns
    -------
    boolean
        Whether operating system supports main symbols or not
    """

    os_arch = platform.system() + str(platform.architecture()[0])

    if os_arch != 'Windows32bit':
        return True

    return False

def colored_frame(frame, color):
    return colored(frame, color, attrs=['bold'])
