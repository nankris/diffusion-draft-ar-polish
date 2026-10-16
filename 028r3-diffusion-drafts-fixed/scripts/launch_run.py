import subprocess,pathlib
p=pathlib.Path('/content/launch_run.pid')
if p.exists():print('already scheduled',p.read_text())
else:
 cmd='while ! grep -q ALL_SETUP_DONE /content/r027/status 2>/dev/null; do sleep 5; done; python3 /content/run.py'
 child=subprocess.Popen(['bash','-c',cmd],stdout=open('/content/run.log','w'),stderr=subprocess.STDOUT,start_new_session=True)
 p.write_text(str(child.pid));print('scheduled',child.pid)
