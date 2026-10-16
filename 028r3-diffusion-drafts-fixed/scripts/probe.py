import pathlib,subprocess
for f in ['build_repair.log','status','dl_dg.log','dl_g4.log']:
 p=pathlib.Path('/content/r027')/f;print(f,p.read_text(errors='replace')[-2500:] if p.exists() else 'missing')
print(subprocess.getoutput('du -sh /content/m/* /content/llama.cpp; ps -eo pid,ppid,args | grep -E "git|cmake|hf download" | head -20'))
