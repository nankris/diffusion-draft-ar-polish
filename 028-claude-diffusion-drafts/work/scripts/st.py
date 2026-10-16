import subprocess
print(subprocess.getoutput('cat /content/r027/status; tail -c 300 /content/r027/build.log; ls /content/m/*; tail -3 /content/r028/progress.txt; date'))
