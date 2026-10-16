import json, pathlib, random
root=pathlib.Path(__file__).resolve().parent
subjects=['AI coding assistants','password managers','home solar','remote work','digital subscriptions','open source maintenance','smart home devices','online education','electric bicycles','cloud storage','phone repair','recommendation algorithms','team documentation','personal budgeting apps','public transit technology']
angles=['a hidden maintenance cost','an example where the default fails','a useful habit for beginners','a tradeoff between convenience and control','a small experiment before buying','a common misleading metric','an overlooked accessibility concern','a reason to keep a manual fallback','a realistic failure and recovery','a change that saves time without hype']
items=[{'id':f'n{i+1:03}','topic':f'{s}: {a}'} for i,(s,a) in enumerate((s,a) for s in subjects for a in angles)]
random.Random(280150).shuffle(items)
for i,p in enumerate(items):p['id']=f'n{i+1:03}'
(root/'topics_round1.json').write_text(json.dumps(items,indent=2)+'\n')
(root/'topics_round2.json').write_text(json.dumps([dict(p,topic=p['topic']+'. Include a concrete hypothetical example and acknowledge a credible counterargument within the word limit.') for p in items],indent=2)+'\n')
