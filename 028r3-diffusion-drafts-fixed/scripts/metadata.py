import subprocess,json,pathlib
obj={}
for name,cmd in {'gpu':'nvidia-smi','commit':'git -C /content/llama.cpp log -1 --format=fuller','models':'ls -l /content/m/dg/*.gguf /content/m/g4/*.gguf','runlog':'tail -20 /content/run.log','build':'tail -10 /content/r027/build.log','status':'cat /content/r027/status'}.items():obj[name]=subprocess.getoutput(cmd)
print(json.dumps(obj,indent=2))
