import psutil
import platform

def get_cpu_info():
    cpu_info = {}

    cpu_info["processor"] = platform.processor()
    cpu_info["physical_cores"] = psutil.cpu_count(logical=False)
    cpu_info["logical_cores"] = psutil.cpu_count(logical=True)

    cpu_info["cpu_usage_percent"] = psutil.cpu_percent(interval=1)
    cpu_info["cpu_per_core"] = psutil.cpu_percent(interval=1, percpu=True)

    freq = psutil.cpu_freq()
    cpu_info["current_frequency_mhz"] = freq.current
    cpu_info["max_frequency_mhz"] = freq.max

    return cpu_info

cpu = get_cpu_info()

print("\n=== CPU INFORMATION ===")
for key, value in cpu.items():
    print(f"{key}: {value}")

print ("\n========================\n")

def get_ram_info():
    ram_info = {}

    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    ram_info["total_ram_gb"] = round(vm.total / (1024 ** 3), 2)
    ram_info["used_ram_gb"] = round(vm.used / (1024 ** 3), 2)
    ram_info["available_ram_gb"] = round(vm.available / (1024 ** 3), 2)
    ram_info["ram_usage_percent"] = vm.percent

    ram_info["swap_total_gb"] = round(swap.total / (1024 ** 3), 2)
    ram_info["swap_used_gb"] = round(swap.used / (1024 ** 3), 2)
    ram_info["swap_usage_percent"] = swap.percent

    return ram_info

ram = get_ram_info()

print("\n=== RAM INFORMATION ===")
for key, value in ram.items():
    print(f"{key}: {value}")

