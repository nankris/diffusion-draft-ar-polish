import subprocess,pathlib
print(subprocess.getoutput('nvidia-smi --query-gpu=name --format=csv,noheader'))
for f in ['/content/r027/status','/content/r027/build.log','/content/r027/dl_dg.log','/content/r027/dl_g4.log','/content/setup.log']:
 p=pathlib.Path(f);print(f, p.read_text(errors='replace')[-1800:] if p.exists() else 'missing')
print(subprocess.getoutput('ps -eo pid,ppid,args | grep -E "setup.sh|cmake --build|hf download" | head -15'))
