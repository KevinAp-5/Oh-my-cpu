import os
import json


def cpu_clock():
    return json.load(os.popen('lscpu -e --json'))


def cleans_cpu_clock_dict(lscpu_dict):
    def clean_content(content):
        content = float(float(content)/1000)
        return '{:.2f}'.format(content)

    cpu_clock = dict()
    for core_count, dicts in enumerate(list(lscpu_dict.values())[0]):
        for title, content in dicts.items():
            if title == 'mhz':
                cpu_clock[f"Core {core_count}"] = clean_content(content)
    return cpu_clock


def update_clock():
    return cleans_cpu_clock_dict(cpu_clock())


def cpu_temp():
    sensors_dict = json.load(os.popen('sensors -j'))
    sensors_dict.pop(next(iter(sensors_dict)))
    return sensors_dict


def cleans_cpu_temp_dict(sensors_dict):
    new_sensors = dict()
    for title, content in list(sensors_dict.values())[0].items():
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
    return extract_only_temp(cleans_cpu_temp_dict(cpu_temp()))


def join_core(cpu_dict):
    return ' '.join([str(x) for x in cpu_dict.values()])


if __name__ == '__main__':
    clean = cleans_cpu_temp_dict(cpu_temp())
    temp = extract_only_temp(clean)
    clock = cleans_cpu_clock_dict(cpu_clock())

    print(f'  CPU TEMP\n  {join_core(update_temp())}\n')
    print(f'  CPU CLOCK\n  {join_core(update_clock())}\n')

