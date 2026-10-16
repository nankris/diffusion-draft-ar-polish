import subprocess,pathlib
print(subprocess.getoutput('tail -4 /content/setup.out; tail -4 /content/setup_logs/build.log; ps -eo pid,comm | tail -6'))
