import os
import json
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


def update_clock():
    return cleans_cpu_clock_dict(cpu_clock())


def cpu_temp():
    sensors_dict = json.load(os.popen('sensors -j'))
    sensors_dict.pop(next(iter(sensors_dict)))
    return sensors_dict


def cleans_cpu_temp_dict(sensors_dict):
    new_sensors = dict()
    for useless, honeypot in sensors_dict.items():
        for title, content in honeypot.items():
            if 'Core' in title:
                new_sensors[title] = content
    return new_sensors


def extract_only_temp(cpu_temp):
    new_cpu_temp = dict()
    for core, temps_dict in cpu_temp.items():
        for title, temp in temps_dict.items():
            if "input" in title:
                new_cpu_temp[core] = temp
    return new_cpu_temp


def update_temp():
    return extract_only_clock(cleans_cpu_temp_dict(cpu_temp()))


def go_through(cpu_dict):
    text = ''
    for x in range(len(cpu_dict)):
        text += str(cpu_dict.get(f"Core {x}")) + ' '
    print(text+'\r', flush=True, end='\n') 


def runs(function, cpu_dict):
    while True:
        try:
            function(cpu_dict)
            sleep(0.3)
        except KeyboardInterrupt:
            break




