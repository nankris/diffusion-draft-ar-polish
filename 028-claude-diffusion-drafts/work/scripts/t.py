import subprocess
print(subprocess.getoutput("pkill -f 'pipelin[e].sh'; pkill llama-; sleep 2"))
print(subprocess.getoutput('''cd /content; G=$(ls m/g4/*.gguf); llama.cpp/build/bin/llama-completion -m $G -ngl 99 -cnv -st --chat-template gemma --temp 0.7 -c 4096 -n 200 --no-display-prompt --simple-io -p "Write a Substack Note (60-100 words) about SQLite for side projects. Output only the note." </dev/null 2>/dev/null | head -c 1200'''))
