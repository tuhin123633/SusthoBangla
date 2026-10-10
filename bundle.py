import re,os,json,posixpath
import base64
MIME={'svg':'image/svg+xml','webp':'image/webp','png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg'}
def duri(fn):
    return 'data:'+MIME[fn.rsplit('.',1)[1]]+';base64,'+base64.b64encode(open('assets/img/'+fn,'rb').read()).decode()
def inl(h): return re.sub(r'src="(?:\.\./)?assets/img/([^"]+)"',lambda m:'src="'+duri(m.group(1))+'"',h)
pages={}
def rw(html,d):
    def f(m):
        h=m.group(2)
        if h.startswith(('http','#','mailto')): return m.group(0)
        p=posixpath.normpath(posixpath.join(d,h)); return f'{m.group(1)}"#/{p}"'
    return re.sub(r'(href=)"([^"]+)"',f,html)
for r,_,fs in os.walk('.'):
    for fn in fs:
        if fn.endswith('.html') and fn!='404.html':
            p=os.path.normpath(os.path.join(r,fn)).replace('\\','/'); d=posixpath.dirname(p)
            s=open(p,encoding='utf-8').read()
            t=re.search(r'<title>(.*?)</title>',s).group(1)
            m=re.search(r'<main id="main" class="w">(.*?)</main>',s,re.S).group(1)
            m=re.sub(r'<script type="application/ld\+json">.*?</script>','',m,flags=re.S)
            pages[p]=[t,inl(rw(m,d))]
s=open('index.html',encoding='utf-8').read()
hd=rw(re.search(r'<a class="skip".*?<main',s,re.S).group(0)[:-5],'')
hd=re.sub(r'<form class="sf"[^>]*>','<form class="sf" id="sform" role="search">',hd)
ft=rw(re.search(r'<footer.*?</footer>',s,re.S).group(0),'')
css=open('style.css',encoding='utf-8').read()
arts=open('assets/articles.js',encoding='utf-8').read()
cn=re.search(r'var CN=(\{.*?\});',open('script.js',encoding='utf-8').read()).group(1)
slugs=re.findall(r'"s": "([^"]+)"',arts)
imgs={}
for sl in slugs:
    for e in ('webp','jpg','jpeg','png','svg'):
        if os.path.exists(f'assets/img/{sl}.{e}'): imgs[sl]=duri(f'{sl}.{e}');break
pj=json.dumps(pages,ensure_ascii=False).replace('</','<\\/')
js="window.__BUNDLE=1;window.SB_CONFIG={};"+arts+open("anim.js",encoding="utf-8").read()+open("auth.js",encoding="utf-8").read()+"var IMGS="+json.dumps(imgs)+";var PAGES="+pj+";var CN="+cn+""";
var main=document.getElementById('main'),q='';
function init(){var L=document.getElementById('list');if(!L)return;var cat='';
function r(){var t=q.trim().toLowerCase();var m=ARTICLES.filter(function(a){return(!cat||a.c===cat)&&(!t||(a.t+a.d).toLowerCase().indexOf(t)>-1)});
L.innerHTML=m.map(function(a){return '<article class="card"><div class="th">'+(IMGS[a.s]?'<img src="'+IMGS[a.s]+'" alt="" loading="lazy" width="600" height="315">':(ICONS[a.c]||''))+'</div><span class="tag">'+E(CN[a.c]||'')+'</span><h3><a href="#/articles/'+a.s+'.html">'+E(a.t)+'</a></h3><p>'+E(a.d)+'</p></article>'}).join('');
reveal();document.getElementById('status').textContent=m.length?m.length+'টি নিবন্ধ পাওয়া গেছে।':'কোনো নিবন্ধ পাওয়া যায়নি। অন্য শব্দ দিয়ে খুঁজুন বা সব বিভাগ দেখুন।'}
document.getElementById('chips').addEventListener('click',function(e){var x=e.target.closest('button');if(!x)return;cat=x.dataset.c;document.querySelectorAll('#chips button').forEach(function(y){y.classList.toggle('on',y===x)});r()});r()}
function route(){var p=location.hash.replace(/^#\\//,'')||'index.html';p=p.split('#')[0].split('?')[0]||'index.html';var pg=PAGES[p]||PAGES['index.html'];
main.innerHTML=pg[1];document.title=pg[0];window.scrollTo(0,0);document.getElementById('nav').classList.remove('open');init();reveal();AUTH.boot()}
window.addEventListener('hashchange',route);
document.addEventListener('click',function(e){var a=e.target.closest('a[href^="#s"]');if(a){e.preventDefault();var t=document.getElementById(a.getAttribute('href').slice(1));if(t)t.scrollIntoView()}});
document.getElementById('sform').addEventListener('submit',function(e){e.preventDefault();q=document.getElementById('q').value;if(location.hash!==''&&location.hash!=='#/index.html'){location.hash='#/index.html'}else route()});
var b=document.querySelector('.mb'),n=document.getElementById('nav');if(b)b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
route();"""
out=f'<!DOCTYPE html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>সুস্থ বাংলা</title><link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&display=swap" rel="stylesheet"><style>{css}</style></head><body>{hd}<main id="main" class="w"></main>{ft}<script>{js}</script></body></html>'
open('/mnt/user-data/outputs/shustho-bangla-live.html','w',encoding='utf-8').write(out)
print(len(out))
