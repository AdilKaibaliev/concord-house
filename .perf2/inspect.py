from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
for token in ["const cv=q('#heroCanvas')", "function resize(){", "function draw(){", "const root=document.documentElement", "function parallax(){"]:
    print('\n###', token)
    start=0
    n=0
    while True:
        i=s.find(token,start)
        if i<0: break
        n+=1
        print('MATCH',n,'AT',i)
        print(s[max(0,i-300):min(len(s),i+3500)])
        start=i+1
        if n>=5: break
