import GPUtil
from tabulate import tabulate
import psutil
import platform
from datetime import datetime


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# let's print CPU information
print("="*40, "CPU Info", "="*40)
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# Memory Information
print("="*40, "Memory Information", "="*40)

# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")

# GPU information
print("="*40, "GPU Details", "="*40)
gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    gpu_name = str(gpu.name)
    gpu_load = f"{gpu.load*100}%"
    gpu_free_memory = f"{gpu.memoryFree}MB"
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    gpu_temperature = f"{gpu.temperature} °C"
    list_gpus.append((
        gpu_name, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature
    ))

print(tabulate(list_gpus, headers=("name", "free memory", "used memory", "total memory", "temperature")))
