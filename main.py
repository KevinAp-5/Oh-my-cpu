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


def cleans_cpu_clock_dict(lscpu_dict):
    cpu_clock = dict()
    core_count = 0

    def clean_content(content):
        content = float(float(content)/1000)
        return '{:.2f}'.format(content)

    for dicts in list(lscpu_dict.values())[0]:
        for title, content in dicts.items():
            if title == 'mhz':
                cpu_clock[f"Core {core_count}"] = clean_content(content)
        core_count += 1
    return cpu_clock


def extract_only_clock(cpu_temp):
    new_cpu_temp = dict()
    for core, temps_dict in cpu_temp.items():
        for title, temp in temps_dict.items():
            if "input" in title:
                new_cpu_temp[core] = temp
    return new_cpu_temp
