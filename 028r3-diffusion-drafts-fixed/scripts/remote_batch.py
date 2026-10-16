import pathlib,json,subprocess,time,sys,os
R=pathlib.Path('/content/r3028');R.mkdir(exist_ok=True)
B=pathlib.Path('/content/llama.cpp/build/bin')
topics=json.loads(pathlib.Path('/content/topics.json').read_text())
for item in topics:item['direct_first']=int(item['id'][1:])%2==0
dg=next(pathlib.Path('/content/m/dg').glob('*.gguf'));g4=next(pathlib.Path('/content/m/g4').glob('*.gguf'))
def atomic(p,t):
 q=p.with_suffix(p.suffix+'.tmp');q.write_text(t);q.replace(p)
def run(item,arm,prompt):
 p=R/f"{item['id']}_{arm}.json"
 if p.exists():return json.loads(p.read_text())
 prefix=R/f"{item['id']}_{arm}"
 args=([str(B/'llama-diffusion-cli'),'-m',str(dg),'-ngl','99','-n','512'] if arm=='C' else [str(B/'llama-completion'),'-m',str(g4),'-ngl','99','-cnv','-st','--chat-template','gemma','--temp','0.7','-c','4096','-n','300','--no-display-prompt','--simple-io'])+['--seed',str(2803+int(item['id'][1:])),'-p',prompt]
 start=time.monotonic()
 with open(str(prefix)+'.out','w') as out,open(str(prefix)+'.err','w') as err:
  try:rc=subprocess.run(args,stdin=subprocess.DEVNULL,stdout=out,stderr=err,timeout=300).returncode
  except subprocess.TimeoutExpired:rc=124
 elapsed=time.monotonic()-start
 text=subprocess.check_output([sys.executable,'/content/extract.py',str(prefix)+'.out'],text=True).strip()
 record=dict(id=item['id'],arm=arm,prompt=prompt,text=text,seconds=elapsed,returncode=rc,args=args)
 atomic(p,json.dumps(record));print(item['id'],arm,rc,elapsed,flush=True)
 return record
# One batch only. Local controller downloads all outputs before launching the next batch.
completed=0
for item in topics:
 if all((R/f"{item['id']}_{a}.json").exists() for a in 'CAB'):continue
 w=f"Write a Substack Note (60-100 words, plain text, one short paragraph or two, no hashtags, no title) about: {item['topic']}."
 if item['direct_first']:run(item,'B',w)
 c=run(item,'C',w)
 p=f"Topic: {item['topic']}\n\nHere is a rough draft of a Substack Note:\n\"\"\"\n{c['text']}\n\"\"\"\n\nPolish it: fix errors, sharpen the wording and the hook, keep it 60-100 words, plain text, no hashtags."
 run(item,'A',p)
 if not item['direct_first']:run(item,'B',w)
 completed+=1
 if completed>=5:break
atomic(R/'batch.done',str(time.time()))
