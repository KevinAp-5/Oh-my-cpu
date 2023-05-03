import os
import json
from contextlib import suppress
from time import sleep

try:
    from reprint import output
except ModuleNotFoundError:
    from subprocess import check_call
    from sys import executable
    check_call([executable, '-m', 'pip', 'install', 'reprint'])
    os.system('clear')
finally:
    from reprint import output


def cpu_clock():
    return json.load(os.popen('lscpu -e --json'))
