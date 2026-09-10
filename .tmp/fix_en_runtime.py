from pathlib import Path
files=[Path('index.html'),Path('en/index.html'),Path('ru/index.html'),Path('ky/index.html')]
old_get="const getLang=()=>document.documentElement.lang && document.documentElement.lang.toLowerCase().startsWith('ky')?'ky':'ru';"
new_get="const getLang=()=>{const l=(document.documentElement.lang||'en').toLowerCase();return l.startsWith('ky')?'ky':l.startsWith('ru')?'ru':'en';};"
for p in files:
    s=p.read_text(encoding='utf-8')
    if old_get not in s:
        raise RuntimeError(f'getLang pattern missing in {p}')
    s=s.replace(old_get,new_get)
    # Use typographic apostrophe so the English text remains grammatical without breaking single-quoted JS strings.
    s=s.replace("participants' home countries", "participants’ home countries")
    p.write_text(s,encoding='utf-8')
    print('fixed',p)
