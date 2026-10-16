import subprocess,time,pathlib,json,sys,tarfile,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]; LOG=ROOT/'results'; SESSION='r3028'
started=time.time(); deadline=started+94*60 # L4 1.54 CU/h, <=4.5 CU including setup margin

def cli(args,timeout=360):
 p=subprocess.run(['colab']+args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
 with (LOG/'controller.log').open('a') as f:f.write(datetime.datetime.now(datetime.timezone.utc).isoformat()+' '+repr(args)+'\n'+p.stdout+'\n')
 if p.returncode:raise RuntimeError(p.stdout)
 return p.stdout

def execute(code):
 p=ROOT/'scripts/_cell.py';p.write_text(code)
 for attempt in range(3):
  try:return cli(['exec','-s',SESSION,'--timeout','300','-f',str(p)])
  except (subprocess.TimeoutExpired,RuntimeError):
   if attempt==2:raise
   time.sleep(5)
def sync():
 execute('import tarfile, pathlib\nwith tarfile.open("/content/snapshot.tgz","w:gz") as t:\n for name in ["r3028","setup_logs","setup.out","batch.out"]:\n  p=pathlib.Path("/content")/name\n  if p.exists():t.add(str(p),arcname=name)\nprint("SNAPSHOT_READY")')
 cli(['download','-s',SESSION,'/content/snapshot.tgz',str(LOG/'snapshot.tgz')])
 with tarfile.open(LOG/'snapshot.tgz') as t:t.extractall(LOG/'raw',filter='data')

def pause(seconds):
 for _ in range(seconds//10):
  if time.time()>deadline:raise TimeoutError('GPU time/CU budget reached')
  time.sleep(10)
try:
 cli(['usage'])
 payload={name:(ROOT/local).read_text() for name,local in [('setup.sh','scripts/setup.sh'),('extract.py','scripts/extract.py'),('remote_batch.py','scripts/remote_batch.py'),('topics.json','topics.json')]}
 execute('import pathlib,subprocess\nfiles='+repr(payload)+'\nfor name,content in files.items():pathlib.Path("/content",name).write_text(content)\nprint(subprocess.getoutput("nvidia-smi --query-gpu=name --format=csv,noheader"))\nsubprocess.Popen(["bash","/content/setup.sh"],stdout=open("/content/setup.out","w"),stderr=subprocess.STDOUT)\nprint("SETUP_LAUNCHED")')
 # Restore durable generation records from interrupted first session.
 records={p.name:p.read_text() for p in (LOG/'raw').glob('n*') if p.is_file()}
 execute('import pathlib\nr=pathlib.Path("/content/r3028");r.mkdir(exist_ok=True)\nrecords='+repr(records)+'\nfor name,content in records.items():(r/name).write_text(content)\nprint("RESTORED")')
 while True:
  out=execute('from pathlib import Path; p=Path("/content/setup_logs/status"); print(p.read_text() if p.exists() else "WAITING")')
  sync()
  if 'ALL_SETUP_DONE' in out:break
  if 'BUILD_DONE 0' not in out and any(x in out for x in ['BUILD_DONE 1','BUILD_DONE 2']):raise RuntimeError('build failed')
  pause(40)
 for batch in range(30):
  if time.time()>deadline:raise TimeoutError('budget')
  execute('import pathlib,subprocess; pathlib.Path("/content/r3028").mkdir(exist_ok=True); pathlib.Path("/content/r3028/batch.done").unlink(missing_ok=True); subprocess.Popen(["python3","/content/remote_batch.py"],stdout=open("/content/batch.out","w"),stderr=subprocess.STDOUT); print("BATCH_LAUNCHED")')
  while True:
   pause(40)
   sync()
   out=execute('from pathlib import Path; print("BATCH_DONE" if Path("/content/r3028/batch.done").exists() else "RUNNING"); print(Path("/content/batch.out").read_text()[-1500:])')
   print(batch+1,out,flush=True)
   if 'Traceback' in out:raise RuntimeError(out)
   if 'BATCH_DONE' in out:break
  sync()
  if len(list((LOG/'raw/r3028').glob('*_A.json')))>=150:break
 (LOG/'generation_complete').write_text('150 notes complete\n')
except BaseException as e:
 (LOG/'controller_error.txt').write_text(repr(e))
 try:sync()
 except Exception:pass
finally:
 try:cli(['stop','-s',SESSION])
 except Exception as e:(LOG/'stop_error.txt').write_text(str(e))
 try:(LOG/'usage_after.txt').write_text(cli(['usage']))
 except Exception:pass
 (LOG/'controller_finished').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat())
