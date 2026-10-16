import os,signal
try:os.killpg(8202,signal.SIGTERM);print('Stopped duplicate repair group only')
except ProcessLookupError:print('already ended')
