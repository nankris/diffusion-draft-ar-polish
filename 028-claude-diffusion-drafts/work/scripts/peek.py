import subprocess
print(subprocess.getoutput('cd /content/r028; cat progress.txt walls.txt; for f in n01_C.txt n01_A.txt n01_B.txt n01_J.out; do echo == $f; head -c 700 $f; done; tail -c 300 n01_A.err; cat /content/pipe.out|tail -3'))
