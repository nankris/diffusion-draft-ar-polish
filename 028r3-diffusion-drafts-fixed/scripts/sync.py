import pathlib,json,base64,hashlib
r=pathlib.Path('/content/r3028'); ack=[]
files={}
if r.exists():
 for p in r.iterdir():
  if p.is_file() and p.suffix!='.ack': files[p.name]=base64.b64encode(p.read_bytes()).decode()
 ack=[p.stem for p in r.glob('*.done')]
for name,path in {'_run.log':'/content/run.log','_setup.status':'/content/r027/status','_buildtail.log':'/content/r027/build.log'}.items():
 p=pathlib.Path(path)
 if p.exists():files[name]=base64.b64encode(p.read_bytes()[-5000:]).decode()
files={k:v for k,v in files.items() if globals().get('known',{}).get(k)!=hashlib.sha256(base64.b64decode(v)).hexdigest()}
print('PAYLOAD:' +json.dumps(files))
# ACK is deliberately a separate local call after durable local write.
