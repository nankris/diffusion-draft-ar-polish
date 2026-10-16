#!/bin/bash
# #028 pipeline on Colab L4. Per note: C=DG draft, A=AR polish of DG draft, B=AR direct, then blind pairwise judge (A vs B, random order).
B=/content/llama.cpp/build/bin; R=/content/r028; mkdir -p $R
DG=$(ls /content/m/dg/*.gguf); G4=$(ls /content/m/g4/*.gguf)
NOTES=${NOTES:-50}
ARF="${ARF:--ngl 99 -cnv -st --chat-template gemma --temp 0.7 -c 4096 -n 300 --no-display-prompt --simple-io}"
ids=$(python3 -c "import json;[print(p['id']) for p in json.load(open('/content/topics.json'))][:$NOTES]" | head -$NOTES)
ar() { # $1 prompt-file $2 out-prefix
  s=$(date +%s.%N); $B/llama-completion -m $G4 $ARF -p "$(cat $1)" < /dev/null > $2.out 2> $2.err; e=$(date +%s.%N); echo "$2 wall $(echo "$e-$s"|bc)" >> $R/walls.txt; }
for id in $ids; do
  T=$(python3 -c "import json;print([p['topic'] for p in json.load(open('/content/topics.json')) if p['id']=='$id'][0])")
  W="Write a Substack Note (60-100 words, plain text, one short paragraph or two, no hashtags, no title) about: $T."
  echo "$W" > $R/$id.w
  s=$(date +%s.%N); timeout 300 $B/llama-diffusion-cli -m $DG -ngl 99 -n 512 -p "$(cat $R/$id.w)" > $R/${id}_C.out 2> $R/${id}_C.err; e=$(date +%s.%N); echo "$R/${id}_C wall $(echo "$e-$s"|bc)" >> $R/walls.txt
  python3 /content/extract.py $R/${id}_C.out > $R/${id}_C.txt
  printf 'Topic: %s\n\nHere is a rough draft of a Substack Note:\n"""\n%s\n"""\n\nPolish it: fix errors, sharpen the wording and the hook, keep it 60-100 words, plain text, no hashtags.' "$T" "$(cat $R/${id}_C.txt)" > $R/$id.p
  ar $R/$id.p $R/${id}_A
  ar $R/$id.w $R/${id}_B
  python3 /content/extract.py $R/${id}_A.out > $R/${id}_A.txt
  python3 /content/extract.py $R/${id}_B.out > $R/${id}_B.txt
  python3 /content/mkjudge.py $id $R "$T" > $R/$id.j
  ar $R/$id.j $R/${id}_J
  echo "done $id" >> $R/progress.txt
done
echo PIPE_DONE >> $R/progress.txt
