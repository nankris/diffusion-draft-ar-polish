import pathlib,json,re,collections
import numpy as np
from scipy.stats import binom,binomtest,beta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=pathlib.Path(__file__).resolve().parents[1];R=ROOT/'results';RAW=R/'raw/r3028'
def objects(text):
 decoder=json.JSONDecoder()
 for i,c in enumerate(text):
  if c=='{':
   try:yield decoder.raw_decode(text[i:])[0]
   except (ValueError,TypeError):pass

def findjudgments(value):
 if isinstance(value,dict):
  if isinstance(value.get('judgments'),list):return value['judgments']
  for v in value.values():
   got=findjudgments(v)
   if got:return got
 elif isinstance(value,list):
  for v in value:
   got=findjudgments(v)
   if got:return got
 elif isinstance(value,str):
  for obj in objects(value):
   if isinstance(obj,dict) and isinstance(obj.get('judgments'),list):return obj['judgments']
 return None
votes=collections.defaultdict(dict);invalid=[];positions=collections.Counter()
for p in sorted((R/'judges').glob('*.json')):
 if p.name.endswith('.mapping.json') or not re.match(r'n\d{3}_',p.name):continue
 rec=json.loads(p.read_text());mapping=json.loads(p.with_name(p.stem+'.mapping.json').read_text())
 # Read only final answer / stdout; stderr may contain echoed prompt examples.
 js=findjudgments(rec.get('answer',rec.get('stdout','')))
 if not js:invalid.append(p.name);continue
 seen=set()
 for j in js:
  id=j.get('id');w=j.get('winner')
  if id not in mapping or id in seen or w not in ['X','Y']:invalid.append(p.name+':'+str(id));continue
  seen.add(id);key=rec['engine']+('_rev' if rec['reverse'] else '_fwd')
  votes[id][key]=mapping[id][w];positions[w]+=1
 for id in set(mapping)-seen:invalid.append(p.name+':missing:'+id)
rows=[];lat=[]
for item in json.loads((ROOT/'topics.json').read_text()):
 id=item['id'];records={}
 for a in 'CAB':
  p=RAW/f'{id}_{a}.json'
  if p.exists():records[a]=json.loads(p.read_text())
 if len(records)<3:continue
 valid=all(x.get('returncode',0)==0 and x['text'].strip() for x in records.values())
 a=records['A']['seconds']+records['C']['seconds'];b=records['B']['seconds'];lat.append([a,b])
 v=votes[id];ac=sum(x=='A' for x in v.values())
 winner=('A' if ac>=3 else 'B' if ac<=1 else 'tie') if len(v)==4 and valid else 'incomplete'
 rows.append(dict(id=id,valid_generation=valid,winner=winner,votes=v,A_seconds=a,B_seconds=b,**{f'{arm}_words':len(rec['text'].split()) for arm,rec in records.items()}))
counts=collections.Counter(x['winner'] for x in rows);a=counts['A'];b=counts['B'];n=a+b
summary=dict(generated=len(rows),counts=dict(counts),decisive=n,invalid_judgments=invalid,positions=dict(positions))
if n:
 test=binomtest(a,n,.5);ci=test.proportion_ci(.95);ci90=test.proportion_ci(.90)
 tost=max(float(binom.sf(a-1,n,.45)),float(binom.cdf(a,n,.55)))
 verdict=('PROVEN' if a>n/2 else 'DISPROVEN') if test.pvalue<.05 else 'DISPROVEN' if tost<.05 else 'STILL INCONCLUSIVE'
 summary.update(win_rate=a/n,pvalue=test.pvalue,ci95=[ci.low,ci.high],ci90=[ci90.low,ci90.high],tost_pvalue=tost,verdict=verdict)
else:summary['verdict']='STILL INCONCLUSIVE'
if lat:
 x=np.array(lat);rng=np.random.default_rng(2803);means=x[rng.integers(0,len(x),(10000,len(x)))].mean(axis=1);delta=means[:,0]-means[:,1]
 summary['latency']=dict(n=len(x),A_mean=x[:,0].mean(),B_mean=x[:,1].mean(),difference=float((x[:,0]-x[:,1]).mean()),difference_ci95=np.quantile(delta,[.025,.975]).tolist(),ratio=float(x[:,0].mean()/x[:,1].mean()),ratio_ci95=np.quantile(means[:,0]/means[:,1],[.025,.975]).tolist(),A_ci95=np.quantile(means[:,0],[.025,.975]).tolist(),B_ci95=np.quantile(means[:,1],[.025,.975]).tolist())
for engine in ['grok','codex']:
 pairs=[v for v in votes.values() if engine+'_fwd' in v and engine+'_rev' in v]
 summary[engine+'_order_agreement']={'n':len(pairs),'agree':sum(v[engine+'_fwd']==v[engine+'_rev'] for v in pairs)}
(R/'notes.json').write_text(json.dumps(rows,indent=2));(R/'summary.json').write_text(json.dumps(summary,indent=2))
fig,axes=plt.subplots(1,2,figsize=(10,4))
if n:
 lo,hi=summary['ci95'];axes[0].axvspan(.45,.55,color='gray',alpha=.2,label='Equivalence band');axes[0].errorbar([a/n],[0],xerr=[[a/n-lo],[hi-a/n]],fmt='o',capsize=6);axes[0].set(xlim=(0,1),ylim=(-.5,.5),yticks=[],xlabel='A win rate among decisive notes',title=f'{a} A wins / {n} decisive; 95% exact CI');axes[0].axvline(.5,color='gray',linestyle=':')
else:axes[0].text(.5,.5,'No decisive judgments',ha='center',va='center');axes[0].set_axis_off()
if lat:
 l=summary['latency'];axes[1].bar(['DG draft + AR polish','AR direct'],[l['A_mean'],l['B_mean']],color=['#7760bf','#37a4a0']);axes[1].set(ylabel='Seconds / note (includes model loading)',title=f"Paired difference {l['difference']:.1f}s; 95% bootstrap CI\n{l['difference_ci95'][0]:.1f} to {l['difference_ci95'][1]:.1f}s")
else:axes[1].text(.5,.5,'No latency observations',ha='center',va='center');axes[1].set_axis_off()
fig.suptitle('028 round 3 — '+summary['verdict']);fig.tight_layout();fig.savefig(ROOT/'chart.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
