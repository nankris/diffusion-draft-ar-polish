import json,re,sys,collections
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
t=open(sys.argv[1]).read(); d=json.loads(re.search(r"JSONSTART(.*)JSONEND",t,re.S).group(1))
json.dump(d,open("results/raw/colab_r028_pull.json","w"),indent=1)
walls=collections.defaultdict(dict)
for l in d["walls"].splitlines():
    p,_,w=l.split(); k=p.split("/")[-1]; i,s=k.split("_"); walls[i][s]=float(w)
rows=[]; wins=collections.Counter()
for i,n in d["notes"].items():
    m=re.search(r"WINNER:\s*\**\s*([XY])",n["J"] or "")
    w=None
    if m:
        o=dict(x.split("=") for x in n["order"].split(","))
        w=o[m.group(1)]
    wins[w]+=1
    wc={k:len((n[k] or "").split()) for k in "CAB"}
    rows.append(dict(id=i,winner=w,**{f"wc_{k}":v for k,v in wc.items()},**{f"t_{k}":walls[i].get(k) for k in "CABJ"}))
N=len(rows); mean=lambda k:sum(r[k] for r in rows)/N
inr=lambda k:sum(60<=r[k]<=100 for r in rows)
S=dict(N=N,A_wins=wins["A"],B_wins=wins["B"],unparsed=wins[None],
  t_C=mean("t_C"),t_A=mean("t_A"),t_B=mean("t_B"),t_J=mean("t_J"),
  wc_C=mean("wc_C"),wc_A=mean("wc_A"),wc_B=mean("wc_B"),
  inr_C=inr("wc_C"),inr_A=inr("wc_A"),inr_B=inr("wc_B"),
  x_picks=sum("WINNER: X" in (n["J"] or "") for n in d["notes"].values()),
  total_min=sum(sum(walls[r["id"]].values()) for r in rows)/60)
json.dump(dict(summary=S,rows=rows),open("results/summary.json","w"),indent=1)
print(json.dumps(S,indent=1))
fig,ax=plt.subplots(1,2,figsize=(10,4))
ax[0].bar(["DG draft → AR polish (A)","AR direct (B)"],[S["A_wins"],S["B_wins"]],color=["#4C72B0","#DD8452"])
ax[0].set_title(f"Blind pairwise judge wins (n={N})"); ax[0].set_ylabel("notes won")
for j,v in enumerate([S["A_wins"],S["B_wins"]]): ax[0].text(j,v,str(v),ha="center",va="bottom")
ax[1].bar(["A: DG draft","A: AR polish","B: AR direct"],[S["t_C"],S["t_A"],S["t_B"]],color=["#55A868","#4C72B0","#DD8452"])
ax[1].set_title("Mean wall time per note (s, L4, incl. model load)"); ax[1].set_ylabel("seconds")
for j,v in enumerate([S["t_C"],S["t_A"],S["t_B"]]): ax[1].text(j,v,f"{v:.1f}",ha="center",va="bottom")
for a in ax: a.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("results/chart.png",dpi=120)
