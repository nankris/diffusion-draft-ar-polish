"""Hard backstop, conservative 3h allocation cap ≈4.62 CU at L4 1.54 CU/h."""
import time,subprocess,datetime,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
deadline=datetime.datetime(2026,10,16,3,18,tzinfo=datetime.timezone.utc).timestamp()
while time.time()<deadline:time.sleep(min(30,max(0,deadline-time.time())))
p=subprocess.run(['colab','stop','-s','r3028'],capture_output=True,text=True)
(root/'results/budget_stop.txt').write_text(p.stdout+p.stderr)
