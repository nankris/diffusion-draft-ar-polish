import subprocess
print(subprocess.getoutput("pkill -f 'pipelin[e].sh'; pkill llama-; sleep 2; rm -rf /content/r028"))
subprocess.Popen("nohup bash /content/pipeline.sh > /content/pipe.out 2>&1 &", shell=True)
print("launched")
