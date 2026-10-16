import subprocess
print(subprocess.getoutput('cd /content/r028; ls | head -30; echo ==C; head -c 1500 n02_C.out; echo; echo ==B; head -c 1500 n02_B.out; echo ==Bwall; grep -c . walls.txt; ps aux|grep -c "pipeline.sh"'))
