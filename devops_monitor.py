import subprocess
import argparse
import shlex
import re

print("DevOps Server Health Monitor")
print("----------------------------")
def run_wsl(command):
    
    if isinstance(command, list):
        command = shlex.join(command)

    result = subprocess.run(
        ["wsl", "-d", "Ubuntu", "bash", "-c", command], 
        capture_output=True, 
        text=True,
        check=False
    )

    if result.returncode != 0:
        print("Error:")
        print(result.stderr)
        return 

    return result.stdout

def get_memory_usage():
    output = run_wsl("free -b")

    if output is None:
        return 

    memory = []
    lines = output.splitlines()

    for line in lines[1:]:
        data = line.split()
        
        name = data[0]
        total = int(data[1])
        used = int(data[2])

        percentage = (used / total) * 100
        memory.append((name, percentage))

    return memory

def show_memory_usage():
    print("====== MEMORY USAGE ======")

    result = get_memory_usage()

    if result is None:
        print("Could not retrive memory usage")

    for name, percentage in result:
        print(f"{name} Usage: {percentage:.2f}%")


def disk_usage():
    # run_wsl("df -h")
    output = run_wsl("df -h")

    if output is None:
            return 

    disks = []
    lines = output.splitlines()
    
    for line in lines[1:]:
        data = line.split()
        if data[0] != "none":
        
            name = data[5]
            used = data[4]

            disks.append((name, used))
    return disks

def show_disk_usage():
    print("====== DISK USAGE ======")
    result = disk_usage()

    if result is None:
        print("Could not retrive disk usage.")
        return 

    for name, used in result:
        print(f"{name}: {used}")



def cpu_load():
    output = run_wsl("uptime")

    if output is None:
        return None 

    return output.strip()


def show_cpu_load():
    print("====== CPU/LOAD ======")
    result = cpu_load()

    if result is None:
        print("Could not retrieve CPU load.")
        return 

    print(result)


def cpu_usage():
    output = run_wsl("top -bn1")
    if output is None:
        return

    for line in output.splitlines():
        if "%Cpu(s)" in line:
            data = line.split(",")

            for item in data:
                if "id" in item:
                    idle = float(item.strip().split()[0])
                    usage = 100 - idle

                    return usage 
    return None

def show_cpu_usage():
    print("====== CPU USAGE ======")
    result = cpu_usage()
    if result is not None:
        print(f"Total CPU Usage: {result:.2f}%")
    else:
        print("Could not retrieve CPU usage.")



def log_checker():
    run_wsl("journalctl -n 100 --no-pager")
    output = run_wsl(["journalctl", "-n", "100", "--no-pager"])

    if output is None:
        return None 

    counts = {
        "EMERGENCY": 0,
        "ALERT": 0,
        "CRITICAL": 0,
        "ERROR": 0,
        "WARNING": 0,
        "NOTICE": 0,
        "INFO": 0,
        "DEBUG": 0
    }

    for line in output.splitlines():
        match = re.search(r'\b(EMERGENCY|ALERT|CRITICAL|ERROR|WARNING|NOTICE|INFO|DEBUG)\b', line, re.IGNORECASE)
        if match:
            level = match.group(1).upper()
            counts[level] += 1
    return counts

def show_log_checker():
    print("====== LOG SUMMARY ======")

    result = log_checker()

    if result is None:
        print("Could not retrieve logs.")
        return

    for level, count in result.items():
        print(f"{level}: {count}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["memory_usage", "disk_usage", "cpu_load", "cpu_usage", "check_logs", "all"], default="all")

    # parser.add_argument("--check_logs", action="store_true")

    args = parser.parse_args()

    if args.action == "memory_usage":
        show_memory_usage()

    elif args.action == "disk_usage":
        show_disk_usage()

    elif args.action == "cpu_load":
        show_cpu_load()

    elif args.action == "cpu_usage":
        show_cpu_usage()

    elif args.action == "check_logs":
        show_log_checker()

    else:
        show_memory_usage()
        show_disk_usage()
        show_cpu_load()
        show_cpu_usage()
        show_log_checker()

if __name__ == "__main__":
    main()

## cpu usage = (100 - Idle Percentage)
## memory usage = (total - free) / total * 100
## Disk usage = 
## Sytem Uptime =


## Log Summary
## ERROR: 
## WARNING:
## INFO: 

## Alerts:
