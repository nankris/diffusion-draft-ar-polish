import json,pathlib,subprocess,time,random,sys,os
R=pathlib.Path('/content/r3028');R.mkdir(exist_ok=True)
B=pathlib.Path('/content/llama.cpp/build/bin')
DG=next(pathlib.Path('/content/m/dg').glob('*.gguf'));G4=next(pathlib.Path('/content/m/g4').glob('*.gguf'))
topics=json.load(open('/content/topics.json'))
def run(id,arm,prompt):
    record=R/f'{id}_{arm}.json'
    if record.exists():return json.loads(record.read_text())
    (R/f'{id}_{arm}.prompt').write_text(prompt)
    args=([str(B/'llama-diffusion-cli'),'-m',str(DG),'-ngl','99','-n','512','--seed',str(2803+int(id[1:]))] if arm=='C' else [str(B/'llama-completion'),'-m',str(G4),'-ngl','99','-cnv','-st','--chat-template','gemma','--temp','0.7','-c','4096','-n','300','--no-display-prompt','--simple-io','--seed',str(2803+int(id[1:]))])+['-p',prompt]
    start=time.monotonic()
    with open(R/f'{id}_{arm}.out','w') as out,open(R/f'{id}_{arm}.err','w') as err:
        p=subprocess.run(args,stdin=subprocess.DEVNULL,stdout=out,stderr=err,timeout=300)
    seconds=time.monotonic()-start
    if p.returncode:raise RuntimeError(f'{id} {arm}: exit {p.returncode}')
    text=subprocess.check_output(['python3','/content/extract.py',str(R/f'{id}_{arm}.out')],text=True).strip()
    obj=dict(id=id,arm=arm,text=text,seconds=seconds,args=args)
    tmp=record.with_suffix('.tmp');tmp.write_text(json.dumps(obj));tmp.replace(record)
    return obj
for t in topics:
    id=t['id'];topic=t['topic']
    w=f'Write a Substack Note (60-100 words, plain text, one short paragraph or two, no hashtags, no title) about: {topic}.'
    # Balanced deterministic ordering; draft precedes polish whenever A runs.
    def pipeline():
        c=run(id,'C',w)
        return run(id,'A',f'Topic: {topic}\n\nHere is a rough draft of a Substack Note:\n"""\n{c["text"]}\n"""\n\nPolish it: fix errors, sharpen the wording and the hook, keep it 60-100 words, plain text, no hashtags.')
    if int(id[1:])%2: pipeline();run(id,'B',w)
    else:run(id,'B',w);pipeline()
    (R/f'{id}.done').write_text('complete\n')
    print(id,flush=True)
    # Local controller releases each five-note batch only after copying ALL outputs.
    if int(id[1:]) % 5 == 0:
        while not (R/f'{id}.ack').exists():time.sleep(1)
(R/'COMPLETE').write_text('done\n')
