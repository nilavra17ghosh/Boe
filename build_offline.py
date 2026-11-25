"""Build site/BoE_Study_Guide_offline.html: one self-contained file (no network needed)."""
import json, re, pathlib
site = pathlib.Path(__file__).parent / 'site'
html = (site / 'index.html').read_text(encoding='utf-8')
marked = (site / 'marked.min.js').read_text(encoding='utf-8')
md = (pathlib.Path(__file__).parent / 'BoE_EndSem_Study_Guide.md').read_text(encoding='utf-8')
html = re.sub(r'<link[^>]*fonts\.g[^>]*>\s*', '', html)          # drop web fonts (falls back to Georgia/system)
html = html.replace('<script src="marked.min.js"></script>', '<script>' + marked.replace(r'</script', '<\/script') + '</script>')
html = html.replace("fetch('guide.md',{cache:'no-cache'})", 'Promise.resolve({ok:true,text:()=>Promise.resolve(window.__MD)})')
html = html.replace('<script>\nconst REPO', '<script>window.__MD=' + json.dumps(md).replace('</', '<\/') + ';</script>\n<script>\nconst REPO', 1)
html = re.sub(r'<a id="dl"[^>]*>.*?</a>', '', html)
(site / 'BoE_Study_Guide_offline.html').write_text(html, encoding='utf-8')
print('ok', len(html))
