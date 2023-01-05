import subprocess


def run_command(command, path=None):
    return subprocess.run(
        command,
        shell=True,
        cwd=path,
        text=True,
        capture_output=True,
    )


def run_command_continuously(command, path=None):
    proc = subprocess.Popen(
        command,
        shell=True,
        cwd=path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    while True:
        line = proc.stdout.readline().strip()
        if line:
            yield line
        if proc.poll() is not None:
            break
