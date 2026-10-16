import os,signal,subprocess,pathlib
# Stop the accidental second setup process group; preserve the first download.
try:os.killpg(8002,signal.SIGTERM)
except ProcessLookupError:pass
print(subprocess.getoutput('ls /content/llama.cpp | head; git -C /content/llama.cpp status -sb; git -C /content/llama.cpp log -1 --oneline'))
cmd='cd /content/llama.cpp && git fetch origin pull/24423/head:diffusiongemma && git checkout diffusiongemma && git log -1 > /content/r027/commit.txt && cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DLLAMA_CURL=OFF && cmake --build build -j8 --config Release --target llama-diffusion-cli llama-completion; echo BUILD_EXIT=$?'
p=subprocess.Popen(['bash','-c',cmd],stdout=open('/content/r027/build_repair.log','w'),stderr=subprocess.STDOUT,start_new_session=True);print('repair build',p.pid)
