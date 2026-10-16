import subprocess
print(subprocess.getoutput('/content/llama.cpp/build/bin/llama-completion --help 2>&1 | grep -iE -A1 "reasoning|display-prompt|enable_thinking|simple-io|chat-template-kwargs"; /content/llama.cpp/build/bin/llama-diffusion-cli --help 2>&1 | grep -iE -A1 "reasoning|thinking|system"; ps aux|grep -c llama'))
