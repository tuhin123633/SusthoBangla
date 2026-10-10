# চালান: python3 gen_images.py   (প্রতিটি নিবন্ধ/পরিকল্পিত বিষয়ের জন্য মৌলিক SVG ছবি বানায়; কোনো তৃতীয়-পক্ষের ছবি নয়)
import random,colorsys,importlib,build
from plan import items
def rgb(h): return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def hx(c): return '#%02x%02x%02x'%tuple(int(v*255) for v in c)
def art(slug,cat):
    R=random.Random(slug);h,l,s=colorsys.rgb_to_hls(*rgb(build.BG[cat]))
    c1=hx(colorsys.hls_to_rgb((h+R.uniform(-.04,.04))%1,min(l*1.3,.6),s));c2=hx(colorsys.hls_to_rgb((h+R.uniform(-.09,.09))%1,max(l*.65,.12),s))
    x2,y2=R.choice(((1,1),(0,1),(1,0)))
    o=''.join(f'<circle cx="{R.randint(0,1200)}" cy="{R.randint(0,630)}" r="{R.randint(40,220)}" fill="#fff" opacity="{R.uniform(.05,.15):.2f}"/>' for _ in range(7))
    for _ in range(2):
        y=R.randint(380,560);o+=f'<path d="M0 {y} C300 {y-R.randint(60,140)} 700 {y+R.randint(60,140)} 1200 {y-R.randint(0,80)} V630 H0Z" fill="#fff" opacity=".08"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="1200" height="630" fill="url(#g)"/>{o}<g transform="translate(300 115) scale(5)">{build.SH[cat]}</g></svg>'
todo=[(a[2],a[0]) for a in build.A]+[(c,k) for c,k,_ in items()]
for c,k in todo: open(f'assets/img/{k}.svg','w',encoding='utf-8').write(art(k,c))
L=list(items());out='# বিষয় পরিকল্পনা (স্লাগ: শিরোনাম)\nছবি assets/img/<স্লাগ>.svg-এ তৈরি। লেখা content/<স্লাগ>.md নামে রাখুন (ফরম্যাট README-তে)।\n';cur=None
for c,k,t in L:
    if c!=cur: out+=f'\n## {build.cn[c]} ({c})\n';cur=c
    out+=f'- {k}: {t}\n'
open('content/PLAN.md','w',encoding='utf-8').write(out)
importlib.reload(build);print(len(todo),'ছবি তৈরি')
