from pathlib import Path
import re

ROOT = Path('.')
INDEX = ROOT / 'index.html'
s = INDEX.read_text(encoding='utf-8')


def replace(old, new, minimum=1):
    global s
    count = s.count(old)
    if count < minimum:
        raise RuntimeError(f'Expected at least {minimum} occurrence(s) of {old!r}, found {count}')
    s = s.replace(old, new)
    print(f'replaced {count}: {old[:80]}')

# Make performance assets route-safe for /en/, /ru/, /ky/ pages.
s = s.replace("'assets/ch-", "'/assets/ch-")
s = s.replace('"assets/ch-', '"/assets/ch-')

# English fallback / accessibility strings that were still Russian.
replace('href="#top">Перейти к содержанию</a>', 'href="#top" data-static-i18n="skip">Skip to content</a>')
replace('Для интерактивных схем и калькулятора требуется JavaScript. Основное содержание страницы остаётся доступным.', 'Interactive diagrams and the calculator require JavaScript. The main page content remains available.')
replace('<nav aria-label="Основная навигация">', '<nav aria-label="Primary navigation" data-static-i18n="nav">')
replace('<span class="vm-dot v6" id="homelandDot">Связь с родиной</span>', '<span class="vm-dot v6" id="homelandDot">Connection to home countries</span>')
s = s.replace('+10.9 п.п.', '+10.9 pp')

# English copy editing: grammar, idiom and U.S. business phrasing.
corrections = {
    'What should remain after us?': 'What should we leave behind?',
    'The decision should follow from facts, values and time horizon.': 'The decision should follow from facts, values, and your time horizon.',
    'The terms should be changed or declined first': 'The terms would need to change, or I would decline to participate.',
    'Based on your answers, the mechanism is clear, the evidence is sufficient and the rules raise no fundamental objection.': 'Based on your answers, the mechanism is clear, the evidence is sufficient, and you have no fundamental objections to the rules.',
    'One coordinated negotiation replaces repeated approaches.': 'One coordinated negotiation replaces multiple separate negotiations.',
    '"Repeat supply"': '"Repeat orders"',
    "participants home countries": "participants' home countries",
    'the economics of organized purchasing demand are credible?': 'the economics of pooled purchasing are credible?',
    'analysis of the economics of organized purchasing demand.': 'analysis of pooled purchasing economics.',
    '"grocers operated separately."': '"Grocers operated separately."',
    '"businesses purchased goods without owning the distribution infrastructure."': '"Businesses purchased goods without owning the distribution infrastructure."',
    '"smaller businesses began without shared infrastructure."': '"Smaller businesses began without shared infrastructure."',
    'data and the financial operation.': 'data and financial operations.',
    'Only proven economic gains become a basis for the next layer of infrastructure and future opportunities.': 'Only proven economic gains should become the basis for the next layer of infrastructure and future opportunities.',
    'A supplier values a predictable, recurring large customer differently from a series of small one-off orders.': 'Suppliers value predictable, recurring volume differently from a series of small one-off orders.',
    'Three questions before deciding.': 'Three questions before you decide.',
    'This is not a promised timetable. It is a sequence: validate the mechanism, build operating infrastructure, then expand only where the evidence supports it.': 'The sequence is simple: validate the mechanism, build operating infrastructure, then expand only where the evidence supports it.'
}
for old, new in corrections.items():
    if old in s:
        n = s.count(old)
        s = s.replace(old, new)
        print(f'copy edit {n}: {old[:75]}')
    else:
        print(f'copy edit not found (non-fatal): {old[:75]}')

# URL must override a previously saved preference so a shared language link always opens in that language.
old_init = "applyLang(['ru','ky','en'].includes(localStorage.getItem('concordhouse-lang')) ? localStorage.getItem('concordhouse-lang') : 'en');"
new_init = """let initialLang='en';try{const routeLang=(location.pathname.match(/^\\/(en|ru|ky)(?:\\/|$)/)||[])[1];const queryLang=new URLSearchParams(location.search).get('lang');const savedLang=localStorage.getItem('concordhouse-lang');initialLang=['ru','ky','en'].includes(routeLang)?routeLang:['ru','ky','en'].includes(queryLang)?queryLang:['ru','ky','en'].includes(savedLang)?savedLang:'en'}catch(e){}applyLang(initialLang);"""
replace(old_init, new_init)

# Keep non-i18n accessibility text and the URL synchronized with the selected language.
static_sync = r'''
<script id="languageRouteSync">
(()=>{
 const copy={
  en:{skip:'Skip to content',nav:'Primary navigation',pause:'Pause background animation',resume:'Resume background animation',home:'Connection to home countries'},
  ru:{skip:'Перейти к содержанию',nav:'Основная навигация',pause:'Приостановить фоновую анимацию',resume:'Возобновить фоновую анимацию',home:'Связь с родиной'},
  ky:{skip:'Мазмунга өтүү',nav:'Негизги навигация',pause:'Фондук анимацияны токтотуу',resume:'Фондук анимацияны улантуу',home:'Мекен менен байланыш'}
 };
 const route={en:'/en/',ru:'/ru/',ky:'/ky/'};
 function sync(l){
  l=copy[l]?l:'en'; const c=copy[l];
  const skip=document.querySelector('[data-static-i18n="skip"]');if(skip)skip.textContent=c.skip;
  const nav=document.querySelector('[data-static-i18n="nav"]');if(nav)nav.setAttribute('aria-label',c.nav);
  const home=document.getElementById('homelandDot');if(home)home.textContent=c.home;
  const motion=document.getElementById('motionToggle');if(motion){const off=document.body.classList.contains('motion-off');motion.setAttribute('aria-label',off?c.resume:c.pause);}
 }
 document.querySelectorAll('.lang button').forEach(btn=>btn.addEventListener('click',()=>{
  const l=btn.dataset.lang;if(!copy[l])return;
  setTimeout(()=>{sync(l);try{history.replaceState(null,'',route[l]+location.hash)}catch(e){}},0);
 }));
 sync(document.documentElement.lang||'en');
 window.addEventListener('popstate',()=>sync(document.documentElement.lang||'en'));
})();
</script>
'''
replace('</body>', static_sync + '</body>')

# Clean obsolete head comment.
s = s.replace('<!-- Production build. Domain-specific canonical/og:url are intentionally added only after the final domain is selected. -->', '<!-- Production build. Language-specific sharing metadata enabled. -->')

META = {
 'en': {
  'title':'Concord House | Shared Purchasing Power',
  'description':'Concord House combines recurring business purchasing demand to build purchasing power, shared infrastructure and long-term institutional value.',
  'og_title':'Concord House — Shared Purchasing Power',
  'og_desc':'Combine recurring business demand. Build purchasing power, shared infrastructure and lasting institutional value.',
  'locale':'en_US',
  'twitter_title':'Concord House — Shared Purchasing Power',
  'twitter_desc':'Recurring demand → purchasing power → shared infrastructure → long-term institutional value.',
  'noscript':'Interactive diagrams and the calculator require JavaScript. The main page content remains available.'
 },
 'ru': {
  'title':'Concord House | Объединённая закупочная сила',
  'description':'Concord House / Ынтымак Ордосу объединяет регулярный спрос компаний, чтобы создавать закупочную силу, общую инфраструктуру и долгосрочный капитал.',
  'og_title':'Concord House — Объединённая закупочная сила',
  'og_desc':'Регулярный спрос → закупочная сила → общая инфраструктура → долгосрочный институциональный капитал.',
  'locale':'ru_RU',
  'twitter_title':'Concord House — Объединённая закупочная сила',
  'twitter_desc':'Регулярный спрос → закупочная сила → общая инфраструктура → долгосрочный институциональный капитал.',
  'noscript':'Для интерактивных схем и калькулятора требуется JavaScript. Основное содержание страницы остаётся доступным.'
 },
 'ky': {
  'title':'Concord House | Бириктирилген сатып алуу күчү',
  'description':'Concord House / Ынтымак Ордосу компаниялардын туруктуу сатып алуу муктаждыктарын бириктирип, жалпы сатып алуу күчүн, инфраструктураны жана узак мөөнөттүү капиталды түзүүгө шарт түзөт.',
  'og_title':'Concord House — Бириктирилген сатып алуу күчү',
  'og_desc':'Туруктуу суроо-талап → сатып алуу күчү → жалпы инфраструктура → узак мөөнөттүү институттук капитал.',
  'locale':'ky_KG',
  'twitter_title':'Concord House — Бириктирилген сатып алуу күчү',
  'twitter_desc':'Туруктуу суроо-талап → сатып алуу күчү → жалпы инфраструктура → узак мөөнөттүү институттук капитал.',
  'noscript':'Интерактивдүү схемалар жана калькулятор үчүн JavaScript керек. Барактын негизги мазмуну жеткиликтүү бойдон калат.'
 }
}


def sub1(text, pattern, repl):
    out, n = re.subn(pattern, repl, text, count=1, flags=re.I)
    if n != 1:
        raise RuntimeError(f'Metadata pattern expected once, got {n}: {pattern}')
    return out


def build_page(template, lang):
    m = META[lang]
    text = template
    text = sub1(text, r'<html lang="[^"]*">', f'<html lang="{lang}">')
    text = sub1(text, r'<title>.*?</title>', f'<title>{m["title"]}</title>')
    text = sub1(text, r'<meta content="[^"]*" name="description"/>', f'<meta content="{m["description"]}" name="description"/>')
    text = sub1(text, r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{m["og_title"]}" property="og:title"/>')
    text = sub1(text, r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{m["og_desc"]}" property="og:description"/>')
    # Replace locale + any immediately adjacent alternates with a full language set.
    text = re.sub(r'<meta content="[^"]*" property="og:locale"/>(?:<meta content="[^"]*" property="og:locale:alternate"/>)*',
                  f'<meta content="{m["locale"]}" property="og:locale"/><meta content="en_US" property="og:locale:alternate"/><meta content="ru_RU" property="og:locale:alternate"/><meta content="ky_KG" property="og:locale:alternate"/>',
                  text, count=1)
    text = sub1(text, r'<meta content="[^"]*" name="twitter:title"/>', f'<meta content="{m["twitter_title"]}" name="twitter:title"/>')
    text = sub1(text, r'<meta content="[^"]*" name="twitter:description"/>', f'<meta content="{m["twitter_desc"]}" name="twitter:description"/>')
    # Remove any prior canonical/hreflang/og:url tags before reinserting canonical language metadata.
    text = re.sub(r'<link[^>]+rel="canonical"[^>]*/?>', '', text, flags=re.I)
    text = re.sub(r'<link[^>]+rel="alternate"[^>]+hreflang="[^"]+"[^>]*/?>', '', text, flags=re.I)
    text = re.sub(r'<meta[^>]+property="og:url"[^>]*/?>', '', text, flags=re.I)
    url=f'https://www.concordhouse.us/{lang}/'
    tags=(f'<link rel="canonical" href="{url}"/>'
          f'<link rel="alternate" hreflang="en" href="https://www.concordhouse.us/en/"/>'
          f'<link rel="alternate" hreflang="ru" href="https://www.concordhouse.us/ru/"/>'
          f'<link rel="alternate" hreflang="ky" href="https://www.concordhouse.us/ky/"/>'
          f'<link rel="alternate" hreflang="x-default" href="https://www.concordhouse.us/en/"/>'
          f'<meta content="{url}" property="og:url"/>')
    text = text.replace('</head>', tags + '</head>', 1)
    text = re.sub(r'(<noscript><div class="noscript-note">).*?(</div></noscript>)', lambda x:x.group(1)+m['noscript']+x.group(2), text, count=1, flags=re.S)
    return text

# Root remains a convenient English entry point; explicit language routes are share-safe.
root_page = build_page(s, 'en')
INDEX.write_text(root_page, encoding='utf-8')
for lang in ('en','ru','ky'):
    d = ROOT / lang
    d.mkdir(exist_ok=True)
    (d/'index.html').write_text(build_page(s, lang), encoding='utf-8')

print('Generated root + /en/ + /ru/ + /ky/ language-aware pages')
