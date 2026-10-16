from scipy.stats import binom,beta
import json
out={}
for n in [150,200,857,1000]:
 sup=[k for k in range(n+1) if 2*min(binom.cdf(k,n,.5),binom.sf(k-1,n,.5))<.05 and k>n/2]
 eq=[k for k in range(1,n) if beta.ppf(.05,k,n-k+1)>.45 and beta.ppf(.95,k+1,n-k)<.55]
 out[n]={'superiority_min_wins':min(sup) if sup else None,'power_p59':sum(binom.pmf(k,n,.59) for k in sup),'power_p60':sum(binom.pmf(k,n,.60) for k in sup),'power_p65':sum(binom.pmf(k,n,.65) for k in sup),'equivalence_power_p50':sum(binom.pmf(k,n,.5) for k in eq),'equivalence_k_range':[min(eq),max(eq)] if eq else None}
print(json.dumps(out,indent=2))
