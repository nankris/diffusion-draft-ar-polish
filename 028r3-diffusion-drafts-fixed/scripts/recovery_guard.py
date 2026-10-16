import pathlib,time,datetime,subprocess
r=pathlib.Path(__file__).resolve().parents[1]
# First session began 00:19:30, terminated/pruned 01:51:05 (~2.35 CU).
# Two short failed recovery sessions add ~0.11 CU; cap this last session at 91 minutes.
deadline=datetime.datetime(2026,10,16,4,15,tzinfo=datetime.timezone.utc).timestamp()
while time.time()<deadline:
 if (r/'results/controller_finished').exists():break
 time.sleep(min(20,max(0,deadline-time.time())))
else:
 p=subprocess.run(['colab','stop','-s','r3028'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
 (r/'results/recovery_guard_stop.txt').write_text(p.stdout)
