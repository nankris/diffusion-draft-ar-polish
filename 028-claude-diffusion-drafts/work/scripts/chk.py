import subprocess
print(subprocess.getoutput('date; cd /content/r028 && cat progress.txt; wc -l walls.txt; ps aux | grep -E "pipelin[e]|llama-[a-z]" | head; tail -3 /content/pipe.out; ls | wc -l'))
