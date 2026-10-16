import subprocess,pathlib
cmd='cd /content/llama.cpp && cmake --build build -j3 --config Release --target llama-diffusion-cli llama-completion >> /content/setup_logs/build.log 2>&1; code=$?; echo BUILD_DONE $code >> /content/setup_logs/status; if [ $code = 0 ]; then echo ALL_SETUP_DONE >> /content/setup_logs/status; fi'
p=subprocess.Popen(['bash','-c',cmd],stdout=open('/content/resume_build.log','w'),stderr=subprocess.STDOUT,start_new_session=True)
print('RESUMED_BUILD',p.pid)
