import json,random,pathlib,shutil
root=pathlib.Path(__file__).resolve().parents[1]
subjects=['AI coding assistants','password managers','home solar','remote work','digital subscriptions','open source maintenance','smart home devices','online education','electric bicycles','cloud storage','phone repair','recommendation algorithms','team documentation','personal budgeting apps','public transit technology']
angles=['a hidden maintenance cost','an example where the default fails','a useful habit for beginners','a tradeoff between convenience and control','a small experiment before buying','a common misleading metric','an overlooked accessibility concern','a reason to keep a manual fallback','a realistic failure and recovery','a change that saves time without hype']
items=[{'topic':f'{s}: {a}'} for s in subjects for a in angles]
random.Random(2803150).shuffle(items)
for i,p in enumerate(items):p.update(id=f'n{i+1:03}',direct_first=i%2==0)
(root/'topics.json').write_text(json.dumps(items,indent=2)+'\n')
shutil.copyfile(root.parent/'028-claude-diffusion-drafts/work/scripts/extract.py',root/'scripts/extract.py')
s=(root.parent/'028-claude-diffusion-drafts/work/scripts/setup_l4.sh').read_text().replace('set -x','set -euxo pipefail').replace('/content/r027','/content/setup_logs').replace('CMAKE_CUDA_ARCHITECTURES=89','CMAKE_CUDA_ARCHITECTURES=native')
(root/'scripts/setup.sh').write_text(s)
