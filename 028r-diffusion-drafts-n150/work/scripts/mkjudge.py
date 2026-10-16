import sys, pathlib
id,folder,topic,order=sys.argv[1:5]
r=pathlib.Path(folder)
a,b=[(r/f'{id}_{arm}.txt').read_text().strip() for arm in 'AB']
x,y=(a,b) if order=='AB' else (b,a)
print(f'''You are judging two Substack Notes on the topic: {topic}.
Pick the better one for a general tech-savvy audience: clear hook, concrete, accurate, natural voice, 60-100 words.
Note X:
"""{x}"""
Note Y:
"""{y}"""
Answer with one line: "WINNER: X" or "WINNER: Y", then one short reason.''')
