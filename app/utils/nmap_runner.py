import subprocess


def run_nmap(target: str, options: str = "") -> str:
    cmd = ["nmap"]
    if options:
        cmd.extend(options.split())
    cmd.append(target)
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout
