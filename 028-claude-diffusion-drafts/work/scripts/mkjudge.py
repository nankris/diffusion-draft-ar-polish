import sys,random
id,R,T=sys.argv[1:4]
a=open(f"{R}/{id}_A.txt").read().strip(); b=open(f"{R}/{id}_B.txt").read().strip()
flip=random.Random(id).random()<0.5
x,y=(b,a) if flip else (a,b)
open(f"{R}/{id}.order","w").write("X=B,Y=A" if flip else "X=A,Y=B")
print(f"""You are judging two Substack Notes on the topic: {T}.
Pick the better one for a general tech-savvy audience: clear hook, concrete, accurate, natural voice, 60-100 words.

Note X:
\"\"\"{x}\"\"\"

Note Y:
\"\"\"{y}\"\"\"

Answer with one line: "WINNER: X" or "WINNER: Y", then one short reason.""")
