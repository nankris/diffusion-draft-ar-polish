import subprocess
p=subprocess.Popen(["flock","-n","/content/r3028_setup.lock","bash","/content/setup.sh"],stdout=open("/content/setup.log","a"),stderr=subprocess.STDOUT,start_new_session=True)
print(p.pid)
