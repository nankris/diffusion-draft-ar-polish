import json,os,glob
R="/content/r028"; out={"walls":open(R+"/walls.txt").read(),"progress":open(R+"/progress.txt").read(),"notes":{}}
for l in out["progress"].split():
    pass
ids=[l.split()[1] for l in out["progress"].splitlines() if l.startswith("done ")]
def rd(p):
    try: return open(p,errors="ignore").read()
    except Exception: return None
for i in ids:
    out["notes"][i]={k:rd(f"{R}/{i}{s}") for k,s in [("C","_C.txt"),("A","_A.txt"),("B","_B.txt"),("J","_J.out"),("order",".order"),("C_err_tail","_C.err")]}
    e=out["notes"][i]["C_err_tail"]; out["notes"][i]["C_err_tail"]=e[-600:] if e else e
print("JSONSTART"+json.dumps(out)+"JSONEND")
