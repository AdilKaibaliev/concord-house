from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
original=s
changes=[]

def one(old,new,label):
    global s
    n=s.count(old)
    assert n==1, f'{label}: expected 1 match, found {n}'
    s=s.replace(old,new,1)
    changes.append(label)

# Hero network: cap render density, reduce pair count modestly, and skip all drawing once hero is offscreen.
one(
"const cv=q('#heroCanvas'),ctx=cv.getContext('2d');let pts=[];function resize(){const d=window.devicePixelRatio||1;",
"const cv=q('#heroCanvas'),ctx=cv.getContext('2d');let pts=[],heroActive=true;const heroHost=cv.closest('.hero');if('IntersectionObserver' in window&&heroHost)new IntersectionObserver(([e])=>{heroActive=e.isIntersecting},{rootMargin:'120px 0px'}).observe(heroHost);function resize(){const d=Math.min(window.devicePixelRatio||1,innerWidth<900?1:1.5);",
'hero DPR + visibility observer')
one("Math.min(80,Math.floor(innerWidth/18))","Math.min(60,Math.floor(innerWidth/22))",'hero particle count')
one(
"function draw(){ctx.clearRect(0,0,innerWidth,Math.max(innerHeight,850));",
"function draw(){if(!heroActive||document.hidden||document.body.classList.contains('motion-off')){requestAnimationFrame(draw);return}ctx.clearRect(0,0,innerWidth,Math.max(innerHeight,850));",
'hero offscreen skip')

# Cinematic background: lower backing-store cost and render at a visually smooth 30fps instead of 60fps.
one(
"let W=0,H=0,dpr=1,t=0,last=performance.now(),motion=true,scene='hero';",
"let W=0,H=0,dpr=1,t=0,last=performance.now(),lastFrame=0,motion=true,scene='hero';",
'cinematic frame timestamp')
one(
"dpr=Math.min(devicePixelRatio||1,1.7);W=innerWidth;H=innerHeight;",
"dpr=Math.min(devicePixelRatio||1,innerWidth<900?1:1.5);W=innerWidth;H=innerHeight;",
'cinematic DPR cap')
one(
"  function draw(now){\n    const dt=Math.min(40,now-last);",
"  function draw(now){\n    requestAnimationFrame(draw);\n    if(document.hidden)return;\n    const targetFps=motion?30:6;\n    if(now-lastFrame<1000/targetFps)return;\n    lastFrame=now;\n    const dt=Math.min(40,now-last);",
'cinematic frame throttle')
one(
"    });\n    requestAnimationFrame(draw)\n  }\n  function updateScene(){",
"    });\n  }\n  function updateScene(){",
'remove duplicate cinematic RAF scheduling')
one(
"  function parallax(){mx+=(tx-mx)*.045;my+=(ty-my)*.045;root.style.setProperty('--mx',mx+'px');root.style.setProperty('--my',my+'px');requestAnimationFrame(parallax)}",
"  function parallax(){if(!document.hidden&&motion&&innerWidth>=900){const nx=mx+(tx-mx)*.045,ny=my+(ty-my)*.045;if(Math.abs(nx-mx)>.01||Math.abs(ny-my)>.01){mx=nx;my=ny;root.style.setProperty('--mx',mx+'px');root.style.setProperty('--my',my+'px')}}requestAnimationFrame(parallax)}",
'parallax idle/mobile skip')

# Make the first optimization's mobile compositor rule target actual heavy layers.
old_mobile='''  [class*="glass"], [class*="Glass"]{\n    -webkit-backdrop-filter: blur(8px) !important;\n    backdrop-filter: blur(8px) !important;\n  }'''
new_mobile='''  nav{ -webkit-backdrop-filter:blur(10px)!important; backdrop-filter:blur(10px)!important; }\n  section:not(.hero){ -webkit-backdrop-filter:none!important; backdrop-filter:none!important; }\n  .stat,.toggle-stage,.calc-controls,.calc-results,.case-pane,.step,.gov-pane,.principle,.legacy-card,.cta-card,.vision-shell{\n    -webkit-backdrop-filter:blur(6px)!important; backdrop-filter:blur(6px)!important;\n  }'''
one(old_mobile,new_mobile,'mobile compositor reduction')

p.write_text(s,encoding='utf-8',newline='')
print('Applied:', ', '.join(changes))
print('index bytes:', p.stat().st_size)

# Safety invariants: content/features preserved; only performance implementation changed.
for marker in ['ch-interactive-revision-js','quizCopy','engineCopy','heroCanvas','cinematicCanvas','ch-performance-optimization-css']:
    assert marker in s, marker
assert 'data:image/webp;base64,' not in s
assert 'assets/ch-' in s
assert len(s) > 250_000
print('Runtime optimization validation passed.')
