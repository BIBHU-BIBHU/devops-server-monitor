import subprocess

def run_wsl(command):
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

    print(result.stdout)

print("==== MEMORY USAGE ====")
run_wsl("free -h")

print("==== DISK USAGE ====")
run_wsl("df -h")

print("===== CPU/LOAD ====")
run_wsl("uptime")
      
print("==== CPU USAGE ====")
run_wsl("top")
