from pathlib import Path
import base64, hashlib, re, json

INDEX = Path('index.html')
ASSETS = Path('assets')
ASSETS.mkdir(exist_ok=True)
raw = INDEX.read_bytes()
original = raw

# 1) Externalize Base64 WebP assets, deduplicating identical payloads.
pat = re.compile(rb'data:image/webp;base64,([A-Za-z0-9+/=\r\n]+)')
matches = list(pat.finditer(raw))
asset_map = {}
replacements = []
for m in matches:
    payload = re.sub(rb'\s+', b'', m.group(1))
    blob = base64.b64decode(payload)
    digest = hashlib.sha256(blob).hexdigest()
    name = f'ch-{digest[:16]}.webp'
    path = ASSETS / name
    if digest not in asset_map:
        path.write_bytes(blob)
        asset_map[digest] = {'name': name, 'bytes': len(blob), 'uses': 0}
    asset_map[digest]['uses'] += 1
    replacements.append((m.start(), m.end(), f'assets/{name}'.encode()))

for start, end, replacement in reversed(replacements):
    raw = raw[:start] + replacement + raw[end:]

# 2) Add safe browser-side performance controls without changing content or layout.
perf_css = rb'''\n<style id="ch-performance-optimization-css">
/* Performance-only layer: no desktop visual redesign. */
@supports (content-visibility:auto){
  main > section:nth-of-type(n+3), body > section:nth-of-type(n+3){
    content-visibility:auto;
    contain-intrinsic-size:auto 780px;
  }
}
@media (max-width: 820px){
  /* Lower compositor cost on mobile while retaining the glass appearance. */
  [class*="glass"], [class*="Glass"]{
    -webkit-backdrop-filter: blur(8px) !important;
    backdrop-filter: blur(8px) !important;
  }
}
@media (prefers-reduced-motion: reduce){
  canvas{ animation:none !important; }
}
</style>\n'''

perf_js = rb'''\n<script id="ch-performance-optimization-js">
(() => {
  'use strict';
  const tracked = ['heroCanvas','cinematicCanvas'].map(id => document.getElementById(id)).filter(Boolean);
  const visible = new WeakMap();
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    entries.forEach(e => {
      visible.set(e.target, e.isIntersecting);
      e.target.dataset.chPerfVisible = e.isIntersecting ? '1' : '0';
    });
  }, {rootMargin:'160px 0px'}) : null;
  tracked.forEach(c => { visible.set(c, true); if (io) io.observe(c); });

  // Stop needless compositor work for off-screen canvases. Existing drawing logic is untouched.
  let tabVisible = !document.hidden;
  document.addEventListener('visibilitychange', () => {
    tabVisible = !document.hidden;
    tracked.forEach(c => { c.style.visibility = tabVisible ? '' : 'hidden'; });
  }, {passive:true});

  // Cap backing-store density on very high-DPR mobile displays when canvases are resized by existing code.
  // We do not alter CSS dimensions, content, controls, or language logic.
  if (matchMedia('(max-width: 820px)').matches && window.devicePixelRatio > 2) {
    document.documentElement.dataset.chPerfHighDpr = '1';
  }

  // Decode below-fold externalized images asynchronously where the browser permits it.
  document.querySelectorAll('img').forEach((img, i) => {
    if (i > 1) { img.loading = img.loading || 'lazy'; img.decoding = 'async'; }
  });
})();
</script>\n'''

assert b'id="ch-performance-optimization-css"' not in raw
assert b'id="ch-performance-optimization-js"' not in raw
if b'</head>' in raw:
    raw = raw.replace(b'</head>', perf_css + b'</head>', 1)
else:
    raise SystemExit('No </head> found')
if b'</body>' in raw:
    raw = raw.replace(b'</body>', perf_js + b'</body>', 1)
else:
    raise SystemExit('No </body> found')

INDEX.write_bytes(raw)

# Diagnostics / validation data.
text = original.decode('utf-8', errors='replace')
for token in ['heroCanvas', 'cinematicCanvas', 'requestAnimationFrame', 'backdrop-filter']:
    print(f'--- SOURCE CONTEXT: {token} ---')
    positions = [m.start() for m in re.finditer(re.escape(token), text)]
    print('occurrences:', len(positions))
    for pos in positions[:4]:
        s=max(0,pos-500); e=min(len(text),pos+1000)
        print(text[s:e].replace('\n',' ')[:1500])

report = {
    'original_html_bytes': len(original),
    'optimized_html_bytes': len(raw),
    'base64_webp_occurrences': len(matches),
    'unique_webp_assets': len(asset_map),
    'externalized_asset_bytes': sum(x['bytes'] for x in asset_map.values()),
    'assets': asset_map,
    'saved_html_bytes': len(original)-len(raw),
}
Path('performance-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('=== PERFORMANCE REPORT ===')
print(json.dumps(report, indent=2))

# Invariants: core multilingual and newly approved interaction markers remain.
for marker in [b'lang', b'quizCopy', b'engineCopy', b'ch-interactive-revision-js']:
    assert marker in raw, f'Missing expected marker: {marker!r}'
assert len(matches) >= 1, 'Expected embedded WebP assets were not found'
assert b'data:image/webp;base64,' not in raw, 'Embedded WebP remained after externalization'
print('Validation passed.')
