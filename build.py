import os, json, re
try: SBO=re.search(r'url:"(https://[^"]+)"',open('config.js',encoding='utf-8').read()).group(1).rstrip('/')
except Exception: SBO="https://*.supabase.co"
BASE="https://tuhin123633.github.io/SusthoBangla"
BP=re.sub(r"^https?://[^/]+","",BASE)+"/"  # বদলান
NAME="সুস্থ বাংলা"; TAG="স্বাস্থ্য জানুন, সচেতন থাকুন।"
CATS=[("common-diseases","রোগ ও লক্ষণ","সাধারণ রোগ ও লক্ষণ সম্পর্কে প্রাথমিক ধারণা।"),
("nutrition","পুষ্টি","সুষম খাদ্য ও স্বাস্থ্যকর খাওয়ার অভ্যাস।"),
("fitness","ফিটনেস","শরীরচর্চা ও সক্রিয় থাকার সহজ উপায়।"),
("mental-health","মানসিক স্বাস্থ্য","মানসিক চাপ ও মনের যত্ন।"),
("womens-health","নারী স্বাস্থ্য","নারীর স্বাস্থ্য বিষয়ক সাধারণ তথ্য।"),
("childrens-health","শিশু স্বাস্থ্য","শিশুর স্বাস্থ্য বিষয়ক সাধারণ তথ্য।"),
("lifestyle","সুস্থ জীবনযাপন","ঘুম ও দৈনন্দিন অভ্যাস।"),
("prevention","প্রতিরোধমূলক স্বাস্থ্য","রোগ প্রতিরোধে সচেতনতা ও পরীক্ষা।")]
W="https://www.who.int/news-room/fact-sheets/detail/"
NHS="https://www.nhs.uk/"
A=[
("water","প্রতিদিন পর্যাপ্ত পানি পান করার গুরুত্ব","nutrition","পানি শরীরের তাপমাত্রা নিয়ন্ত্রণ ও বর্জ্য অপসারণসহ নানা কাজে সাহায্য করে।",
[("পানি কেন দরকার","শরীরের বিভিন্ন কাজে পানি প্রয়োজন। গরমে ঘাম হলে বা অসুস্থতায় পানির চাহিদা বাড়তে পারে।"),("কতটা পানি যথেষ্ট","প্রয়োজন বয়স, আবহাওয়া ও কাজের ধরনের ওপর নির্ভর করে। প্রস্রাবের রং হালকা হলে সাধারণত পর্যাপ্ত পানি পান করা হচ্ছে বলে ধরা হয়।"),("কখন চিকিৎসকের কাছে যাবেন","অতিরিক্ত তৃষ্ণা, ঘন ঘন প্রস্রাব, ঝিমুনি বা তীব্র পানিশূন্যতার লক্ষণ থাকলে চিকিৎসকের পরামর্শ নিন। কিডনি বা হৃদরোগ থাকলে পানির পরিমাণ নিয়ে চিকিৎসকের নির্দেশ মানুন।")],
[("NHS: Water, drinks and your health",NHS+"live-well/eat-well/food-guidelines-and-food-labels/water-drinks-nutrition/")]),
("balanced-diet","সুষম খাদ্য কী এবং কেন প্রয়োজন","nutrition","বিভিন্ন খাদ্যগোষ্ঠী থেকে পরিমিত খাবার খাওয়াই সুষম খাদ্য।",
[("সুষম খাদ্য মানে কী","শাকসবজি, ফল, ডাল, মাছ, ডিম, শস্য ও পরিমিত তেল-চিনি-লবণ মিলিয়ে খাওয়া।"),("সহজ অভ্যাস","প্লেটে সবজি বাড়ানো, প্রক্রিয়াজাত খাবার ও অতিরিক্ত চিনি-লবণ কমানো।"),("সতর্কতা","বিশেষ রোগ, গর্ভাবস্থা বা শিশুর খাদ্য নিয়ে চিকিৎসক বা পুষ্টিবিদের পরামর্শ নিন।")],
[("WHO: Healthy diet",W+"healthy-diet")]),
("sleep","ভালো ঘুমের অভ্যাস গড়ে তোলার উপায়","lifestyle","নিয়মিত সময়ে ঘুমানো ও ঘুমের পরিবেশ ঠিক রাখা সাহায্য করতে পারে।",
[("ঘুমের সাধারণ অভ্যাস","প্রতিদিন একই সময়ে ঘুমানো ও ওঠা, শোবার ঘর অন্ধকার ও শান্ত রাখা।"),("যা এড়ানো ভালো","ঘুমের আগে বেশি ক্যাফেইন, ভারী খাবার ও দীর্ঘ সময় মোবাইল ব্যবহার।"),("কখন চিকিৎসকের কাছে যাবেন","দীর্ঘদিন ঘুমের সমস্যা, জোরে নাক ডাকা বা ঘুমে শ্বাস বন্ধ হওয়ার মতো লক্ষণ থাকলে চিকিৎসকের পরামর্শ নিন।")],
[("NHS: How to fall asleep faster and sleep better",NHS+"every-mind-matters/mental-wellbeing-tips/how-to-fall-asleep-faster-and-sleep-better/")]),
("walking","নিয়মিত হাঁটার সম্ভাব্য স্বাস্থ্য উপকারিতা","fitness","হাঁটা সহজ ও সাধারণত নিরাপদ শারীরিক কার্যকলাপ।",
[("হাঁটার উপকারিতা","নিয়মিত শারীরিক কার্যকলাপ হৃদরোগ, টাইপ-২ ডায়াবেটিস ও মানসিক চাপের ঝুঁকি কমাতে সাহায্য করে বলে WHO জানায়।"),("কীভাবে শুরু করবেন","অল্প সময় দিয়ে শুরু করে ধীরে বাড়ান। আরামদায়ক জুতা পরুন।"),("সতর্কতা","হাঁটার সময় বুকে ব্যথা, মাথা ঘোরা বা শ্বাসকষ্ট হলে থামুন ও জরুরি চিকিৎসা নিন।")],
[("WHO: Physical activity",W+"physical-activity")]),
("stress","মানসিক চাপ সামলানোর স্বাস্থ্যকর পদ্ধতি","mental-health","ছোট ছোট অভ্যাস চাপ সামলাতে সাহায্য করতে পারে।",
[("চাপ কী","চাপ চ্যালেঞ্জের প্রতি শরীর ও মনের স্বাভাবিক প্রতিক্রিয়া, কিন্তু দীর্ঘস্থায়ী হলে ক্ষতি করতে পারে।"),("কিছু উপায়","গভীর শ্বাস, নিয়মিত হাঁটা, ঘুম, ভরসাযোগ্য কারও সঙ্গে কথা বলা।"),("কখন সাহায্য নেবেন","দৈনন্দিন কাজ ব্যাহত হলে বা নিজের ক্ষতির চিন্তা এলে এখনই কোনো স্বাস্থ্যকর্মী বা বিশ্বস্ত ব্যক্তির সাহায্য নিন।")],
[("WHO: Stress",  "https://www.who.int/news-room/questions-and-answers/item/stress")]),
("food-labels","খাবারের লেবেল কীভাবে পড়বেন","nutrition","লেবেল দেখে চিনি, লবণ ও চর্বির পরিমাণ তুলনা করা যায়।",
[("কী দেখবেন","পরিবেশন মাত্রা, উপাদানের তালিকা এবং চিনি, লবণ ও চর্বির পরিমাণ।"),("তুলনা","একই ধরনের দুটি পণ্যের প্রতি ১০০ গ্রামের মান তুলনা করুন।"),("মনে রাখুন","দেশভেদে লেবেলের নিয়ম আলাদা হতে পারে; স্থানীয় নিয়ম সম্পাদকীয় পর্যায়ে যাচাই করুন।")],
[("NHS: How to read food labels",NHS+"live-well/eat-well/food-guidelines-and-food-labels/how-to-read-food-labels/")]),
("hypertension","উচ্চ রক্তচাপ সম্পর্কে প্রাথমিক ধারণা","common-diseases","উচ্চ রক্তচাপের অনেক সময় কোনো লক্ষণ থাকে না, তাই পরিমাপ জরুরি।",
[("উচ্চ রক্তচাপ কী","ধমনিতে রক্তের চাপ বেশি থাকাকে উচ্চ রক্তচাপ বলে। এটি হৃদরোগ ও স্ট্রোকের ঝুঁকি বাড়ায়।"),("জীবনযাপনের ভূমিকা","লবণ কমানো, সক্রিয় থাকা, ধূমপান এড়ানো ও ওজন নিয়ন্ত্রণ সাহায্য করে।"),("কখন জরুরি সাহায্য","হঠাৎ তীব্র বুকে ব্যথা, কথা জড়িয়ে যাওয়া, মুখ বেঁকে যাওয়া বা একদিকে দুর্বলতা হলে অবিলম্বে হাসপাতালে যান। ওষুধ নিজে শুরু বা বন্ধ করবেন না।")],
[("WHO: Hypertension",W+"hypertension")]),
("diabetes-prevention","ডায়াবেটিস প্রতিরোধে জীবনযাপনের ভূমিকা","prevention","স্বাস্থ্যকর খাদ্য ও শারীরিক কার্যকলাপ টাইপ-২ ডায়াবেটিসের ঝুঁকি কমাতে সাহায্য করতে পারে।",
[("ঝুঁকি কমানোর অভ্যাস","সুষম খাদ্য, নিয়মিত শারীরিক কার্যকলাপ, স্বাস্থ্যকর ওজন ও তামাক এড়ানো।"),("পরীক্ষা","ঝুঁকি থাকলে কখন কোন পরীক্ষা করাবেন তা চিকিৎসকের সঙ্গে আলোচনা করুন।"),("কখন চিকিৎসকের কাছে যাবেন","অতিরিক্ত তৃষ্ণা, ঘন ঘন প্রস্রাব, অকারণে ওজন কমা বা ক্লান্তি থাকলে পরীক্ষা করান।")],
[("WHO: Diabetes",W+"diabetes")]),
]
from expand import NEW
for i,a in enumerate(A):
    if a[0] in NEW: A[i]=(a[0],a[1],a[2],a[3],NEW[a[0]],a[5])
A[5]=A[5][:5]+([A[5][5][0],('NHS: Food labelling terms',NHS+'live-well/eat-well/food-labelling-terms/')],)
import glob, html as _hh
def load_md():
    out=[];ok={c[0] for c in CATS}
    for f in sorted(glob.glob('content/*.md')):
        t=open(f,encoding='utf-8').read();m=re.match(r'---\n(.*?)\n---\n(.*)',t,re.S)
        if not m: continue
        meta={};refs=[]
        for l in m.group(1).split('\n'):
            if l.startswith('- '):
                n,_,u=l[2:].partition('|');u=u.strip()
                if u.startswith('https://'): refs.append((_hh.escape(n.strip()),_hh.escape(u)))
            elif ':' in l:
                k,_,v=l.partition(':');meta[k.strip()]=v.strip()
        secs=[];cur=None
        for l in m.group(2).split('\n'):
            if l.startswith('## '): cur=[l[3:].strip(),[]];secs.append(cur)
            elif cur is not None: cur[1].append(l)
        secs=[(_hh.escape(h),'\n\n'.join(_hh.escape(p.strip()) for p in re.split(r'\n\s*\n','\n'.join(bl).strip()) if p.strip())) for h,bl in secs]
        s=meta.get('slug','')
        if re.fullmatch(r'[a-z0-9-]+',s) and meta.get('category') in ok and secs and refs and not any(a[0]==s for a in A):
            out.append((s,_hh.escape(meta.get('title',s)),meta['category'],_hh.escape(meta.get('summary','')),secs,refs))
        else: print('বাদ (slug/category/সূত্র দরকার):',f)
    return out
A+=load_md()
cn={c[0]:c[1] for c in CATS}
BG={"common-diseases":"#0f766e","nutrition":"#16a34a","fitness":"#0369a1","mental-health":"#7c3aed","womens-health":"#db2777","childrens-health":"#f59e0b","lifestyle":"#1e3a8a","prevention":"#0d9488"}
SH={"common-diseases":'<rect x="50" y="18" width="20" height="44" rx="4" fill="#fff"/><rect x="38" y="30" width="44" height="20" rx="4" fill="#fff"/>',
"nutrition":'<circle cx="60" cy="44" r="20" fill="#ef4444"/><path d="M60 24c0-8 6-12 12-12-1 8-5 12-12 12z" fill="#bbf7d0"/>',
"fitness":'<rect x="30" y="30" width="10" height="20" rx="3" fill="#fff"/><rect x="42" y="36" width="36" height="8" fill="#fff"/><rect x="80" y="30" width="10" height="20" rx="3" fill="#fff"/><rect x="22" y="34" width="6" height="12" rx="2" fill="#bae6fd"/><rect x="92" y="34" width="6" height="12" rx="2" fill="#bae6fd"/>',
"mental-health":'<circle cx="60" cy="40" r="22" fill="#fde68a"/><circle cx="52" cy="35" r="3" fill="#4c1d95"/><circle cx="68" cy="35" r="3" fill="#4c1d95"/><path d="M50 46q10 10 20 0" stroke="#4c1d95" stroke-width="3" fill="none" stroke-linecap="round"/>',
"womens-health":'<circle cx="60" cy="32" r="14" fill="none" stroke="#fff" stroke-width="5"/><path d="M60 46v24M50 58h20" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
"childrens-health":'<circle cx="46" cy="22" r="8" fill="#92400e"/><circle cx="74" cy="22" r="8" fill="#92400e"/><circle cx="60" cy="42" r="22" fill="#b45309"/><circle cx="52" cy="38" r="3" fill="#fff"/><circle cx="68" cy="38" r="3" fill="#fff"/><ellipse cx="60" cy="49" rx="8" ry="6" fill="#fcd34d"/>',
"lifestyle":'<path d="M70 18a24 24 0 1 0 0 44 20 20 0 0 1 0-44z" fill="#fde68a"/><circle cx="90" cy="24" r="3" fill="#fff"/><circle cx="32" cy="22" r="2" fill="#fff"/>',
"prevention":'<path d="M60 12l26 10v18c0 16-11 26-26 30-15-4-26-14-26-30V22z" fill="#fff"/><path d="M48 40l9 9 16-18" stroke="#0d9488" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'}
def ico(k): return f'<svg viewBox="0 0 120 80" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMid slice"><rect width="120" height="80" fill="{BG[k]}"/>{SH[k]}</svg>'
def head(t,d,p,canon):
    return f'''<!DOCTYPE html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' {SBO}; base-uri 'self'; form-action 'self'; object-src 'none'"><meta name="referrer" content="strict-origin-when-cross-origin"><title>{t} | {NAME}</title><meta name="description" content="{d}"><link rel="canonical" href="{BASE}/{canon}"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:type" content="website"><meta property="og:locale" content="bn_BD"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}style.css"></head><body><a class="skip" href="#main">মূল অংশে যান</a><header class="hd"><div class="w hdi"><a class="logo" href="{p}index.html"><svg class="st" viewBox="0 0 32 32" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4v8a6 6 0 0 0 12 0V4"/><path d="M14 18v3a6 6 0 0 0 12 0v-3"/><circle cx="26" cy="15" r="3"/><circle cx="8" cy="4" r="1" fill="currentColor"/><circle cx="20" cy="4" r="1" fill="currentColor"/></svg><span>{NAME}</span><svg class="st mir" viewBox="0 0 32 32" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4v8a6 6 0 0 0 12 0V4"/><path d="M14 18v3a6 6 0 0 0 12 0v-3"/><circle cx="26" cy="15" r="3"/><circle cx="8" cy="4" r="1" fill="currentColor"/><circle cx="20" cy="4" r="1" fill="currentColor"/></svg></a><nav id="nav" aria-label="প্রধান মেনু">'''+"".join(f'<a href="{p}categories/{s}.html">{n}</a>' for s,n,_ in CATS)+f'''<div class="more" hidden><button type="button" class="mbtn" aria-haspopup="true" aria-expanded="false">আরও ▾</button><div class="mpop" hidden></div></div></nav><form class="sf" action="{p}index.html" role="search"><label class="sr" for="q">নিবন্ধ খুঁজুন</label><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><input id="q" name="q" type="search" placeholder="কী জানতে চান?" autocomplete="off"><button aria-label="খুঁজুন">→</button></form><div class="authbox"><a href="{p}login.html" id="authlink" class="authl">লগইন</a><a href="{p}login.html#new" id="signup" class="sgn">নতুন অ্যাকাউন্ট</a></div></div></header><main id="main" class="w">'''
def foot(p):
    return f'''</main><footer class="ft"><div class="w"><p><strong>{NAME}</strong> — {TAG}</p><p><a href="{p}about.html">আমাদের সম্পর্কে</a> · <a href="{p}contact.html">যোগাযোগ</a> · <a href="{p}privacy-policy.html">গোপনীয়তা নীতি</a> · <a href="{p}disclaimer.html">দাবিত্যাগ</a> · <a href="{p}editorial-policy.html">সম্পাদকীয় নীতি</a></p><p class="sm">এই সাইটের তথ্য সাধারণ শিক্ষামূলক, চিকিৎসকের পরামর্শের বিকল্প নয়। © {NAME}</p></div></footer><script src="{p}assets/articles.js"></script><script src="{p}config.js"></script><script src="{p}auth.js"></script><script src="{p}script.js"></script></body></html>'''
import html as _html
ALTS=json.load(open('assets/img/alts.json',encoding='utf-8')) if os.path.exists('assets/img/alts.json') else {}
def img(s):
    for e in ('webp','jpg','jpeg','png','svg'):
        if os.path.exists(f'assets/img/{s}.{e}'): return f'{s}.{e}'
def thumb(a,p):
    im=img(a[0])
    return f'<img src="{p}assets/img/{im}" alt="" loading="lazy" decoding="async" width="600" height="315">' if im else ico(a[2])
def banner(s,t,c):
    im=img(s)
    if im: return f'<figure class="th ban"><img src="../assets/img/{im}" alt="{_html.escape(ALTS.get(s,t+" — সম্পর্কিত চিত্র"))}" width="1200" height="630" fetchpriority="high"></figure>'
    return f'<div class="th ban" role="img" aria-label="{cn[c]} বিষয়ক চিত্র">{ico(c)}</div>'
def card(a,p):
    return f'<article class="card"><div class="th">{thumb(a,p)}</div><span class="tag">{cn[a[2]]}</span><h3><a href="{p}articles/{a[0]}.html">{a[1]}</a></h3><p>{a[3]}</p><p class="sm">খসড়া — সম্পাদকীয় পর্যালোচনা প্রয়োজন</p></article>'
def w(path,s):
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True); open(path,"w",encoding="utf-8").write(s)
# index
f=A[0]
w("index.html",head("স্বাস্থ্য তথ্য বাংলায়","বাংলায় সহজ ভাষায় স্বাস্থ্য, পুষ্টি, ফিটনেস ও মানসিক স্বাস্থ্য বিষয়ক সাধারণ তথ্য।","","index.html")+f'''<section class="hero"><div><h1>{TAG}</h1><p>সহজ বাংলায় স্বাস্থ্য বিষয়ক সাধারণ শিক্ষামূলক তথ্য।</p></div><div class="hi"><div class="th">{ico("nutrition")}</div><div class="th">{ico("fitness")}</div><div class="th">{ico("prevention")}</div></div></section>
<section aria-labelledby="ft"><h2 id="ft">বিশেষ নিবন্ধ</h2><article class="card big"><div class="th">{thumb(f,"")}</div><span class="tag">{cn[f[2]]}</span><h3><a href="articles/{f[0]}.html">{f[1]}</a></h3><p>{f[3]}</p><p class="sm">লেখক: সম্পাদকীয় খসড়া · হালনাগাদ: তারিখ নির্ধারিত হয়নি</p></article></section>
<section aria-labelledby="tp"><h2 id="tp">জনপ্রিয় বিষয়</h2><div class="chips" id="chips"><button data-c="" class="on">সব</button>'''+"".join(f'<button data-c="{s}">{n}</button>' for s,n,_ in CATS)+f'''</div></section>
<section aria-labelledby="la"><h2 id="la">নিবন্ধসমূহ</h2><p id="status" class="sm" role="status"></p><div class="grid" id="list">'''+"".join(card(a,"") for a in A)+f'''</div></section>
<section class="box"><h2>তথ্য কীভাবে যাচাই হয়</h2><p>আমরা WHO, NHS ও অন্যান্য নির্ভরযোগ্য উৎস ব্যবহার করি। প্রতিটি নিবন্ধ প্রকাশের আগে যোগ্য চিকিৎসা পেশাজীবীর পর্যালোচনা প্রয়োজন। <a href="editorial-policy.html">সম্পাদকীয় নীতি পড়ুন</a>।</p></section>
<section class="box" id="nl"><h2>নিউজলেটার</h2><p>নতুন স্বাস্থ্য-নিবন্ধের খবর ইমেইলে পেতে সাবস্ক্রাইব করুন। যেকোনো সময় আনসাবস্ক্রাইব করা যায়।</p><form id="nlForm" class="frm"><label class="sr" for="nle">ইমেইল</label><input id="nle" type="email" required maxlength="254" autocomplete="email" placeholder="আপনার ইমেইল"><input class="hp" id="nlh" tabindex="-1" autocomplete="off" aria-hidden="true"><label class="cons"><input type="checkbox" id="nlc" required> আমি <a href="privacy-policy.html">গোপনীয়তা নীতি</a> পড়েছি এবং ইমেইল পেতে সম্মত।</label><button type="submit">সাবস্ক্রাইব করুন</button><p id="nlmsg" class="msg" role="status"></p></form></section>'''+foot(""))
# articles
for i,a in enumerate(A):
    s,t,c,d,secs,refs=a
    toc="".join(f'<li><a href="#s{j}">{h}</a></li>' for j,(h,_) in enumerate(secs))
    body="".join(f'<h2 id="s{j}">{h}</h2>{"".join("<p>"+q+"</p>" for q in x.split(chr(10)*2))}' for j,(h,x) in enumerate(secs))
    rel="".join(f'<li><a href="{r[0]}.html">{r[1]}</a></li>' for r in A if r[0]!=s and r[2]==c) or "".join(f'<li><a href="{r[0]}.html">{r[1]}</a></li>' for r in A[:3] if r[0]!=s)
    ld=json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":t,"inLanguage":"bn","description":d,"mainEntityOfPage":f"{BASE}/articles/{s}.html"},ensure_ascii=False)
    w(f"articles/{s}.html",head(t,d,"../",f"articles/{s}.html")+f'''<nav class="bc" aria-label="ব্রেডক্রাম্ব"><a href="../index.html">হোম</a> › <a href="../categories/{c}.html">{cn[c]}</a> › {t}</nav><article class="art"><div class="warn" role="note"><strong>খসড়া:</strong> এই নিবন্ধ যোগ্য চিকিৎসা পেশাজীবীর পর্যালোচনা ও সূত্র যাচাইয়ের আগে প্রকাশ করবেন না।</div><h1>{t}</h1>{banner(s,t,c)}<p class="lead">{d}</p><p class="sm">লেখক: সম্পাদকীয় খসড়া (যাচাইকৃত যোগ্যতা নেই) · মেডিকেল রিভিউয়ার: এখনও নেই · প্রকাশ ও হালনাগাদের তারিখ: নির্ধারিত হয়নি · <a href="../editorial-policy.html">সম্পাদকীয় তথ্য</a></p><nav class="toc" aria-label="সূচিপত্র"><h2>সূচিপত্র</h2><ol>{toc}</ol></nav>{body}<h2>মূল কথা</h2><p>{d} ব্যক্তিগত উপসর্গ বা চিকিৎসা নিয়ে সিদ্ধান্তের আগে চিকিৎসকের সঙ্গে কথা বলুন।</p><h2>তথ্যসূত্র</h2><ul>'''+"".join(f'<li><a href="{u}" rel="noopener">{n}</a> (প্রকাশের আগে লিংক ও তথ্য মিলিয়ে নিন)</li>' for n,u in refs)+f'''</ul><div class="warn">এটি সাধারণ শিক্ষামূলক তথ্য; রোগ নির্ণয় বা চিকিৎসার বিকল্প নয়। জরুরি অবস্থায় নিকটস্থ হাসপাতালে যান। <a href="../disclaimer.html">দাবিত্যাগ</a></div><h2>সম্পর্কিত নিবন্ধ</h2><ul>{rel}</ul><!-- AD PLACEHOLDER: অনুমোদনের পর নিজের বিজ্ঞাপন কোড এখানে বসান --></article><script type="application/ld+json">{ld}</script>'''+foot("../"))
for s,n,d in CATS:
    items=[a for a in A if a[2]==s]
    cards="".join(card(a,"../") for a in items) or '<p>এই বিভাগে শীঘ্রই নিবন্ধ যোগ হবে।</p>'
    w(f"categories/{s}.html",head(n,d,"../",f"categories/{s}.html")+f'<nav class="bc"><a href="../index.html">হোম</a> › {n}</nav><h1>{n}</h1><p>{d}</p><div class="grid">{cards}</div>'+foot("../"))
def page(f,t,body): w(f,head(t,t+" — "+NAME,"",f)+f"<h1>{t}</h1>{body}"+foot(""))
page("about.html","আমাদের সম্পর্কে",f"<p>{NAME} বাংলাদেশের পাঠকদের জন্য সহজ বাংলায় সাধারণ স্বাস্থ্য-শিক্ষা দেওয়ার একটি উদ্যোগ। আমরা চিকিৎসা সেবা দিই না। এখানে কোনো চিকিৎসক বা রিভিউয়ারের নাম ততক্ষণ দেখানো হবে না, যতক্ষণ না তাঁদের যোগ্যতা যাচাই হচ্ছে।</p>")
page("contact.html","যোগাযোগ","<p>ভুল তথ্য জানাতে বা মতামত দিতে ইমেইল করুন: <strong>[আপনার ইমেইল এখানে দিন]</strong>। এই সাইটে কোনো ফর্ম-সার্ভার নেই।</p>")
page("privacy-policy.html","গোপনীয়তা নীতি","<p>অ্যাকাউন্ট খুললে আপনার ইমেইল, সংরক্ষিত নিবন্ধের তালিকা ও পাঠানো মতামত Supabase-এ সংরক্ষিত হয়; পাসওয়ার্ড আমরা দেখতে পাই না। অ্যাকাউন্ট ছাড়া ব্যবহারে সাইট নিজে ব্যক্তিগত তথ্য সংগ্রহ করে না। নিউজলেটারে সাবস্ক্রাইব করলে আপনার ইমেইল ও সম্মতির সময় Supabase-এ সংরক্ষিত হয়; প্রতিটি ইমেইলের আনসাবস্ক্রাইব লিংকে তালিকা থেকে সরানো যায়। (চালুর আগে এই বিবরণ নিজের ব্যবস্থার সঙ্গে মিলিয়ে নিন।) ভবিষ্যতে অ্যানালিটিক্স বা বিজ্ঞাপন (যেমন Google AdSense) যোগ করলে কুকি ও তৃতীয় পক্ষের তথ্য সংগ্রহ নিয়ে এই পাতা হালনাগাদ করতে হবে। ফন্ট Google Fonts থেকে লোড হয়।</p>")
page("disclaimer.html","দাবিত্যাগ","<p>এই সাইটের সব তথ্য সাধারণ শিক্ষামূলক। এটি রোগ নির্ণয়, চিকিৎসা বা ব্যক্তিগত পরামর্শ নয়। স্বাস্থ্য সংক্রান্ত সিদ্ধান্তের আগে যোগ্য চিকিৎসকের পরামর্শ নিন। জরুরি অবস্থায় নিকটস্থ হাসপাতালে যান।</p>")
page("editorial-policy.html","সম্পাদকীয় নীতি","<h2>প্রকাশের আগের ধাপ</h2><ol><li>নির্ভরযোগ্য উৎস (WHO, DGHS, NHS, CDC, পিয়ার-রিভিউড গবেষণা) থেকে খসড়া।</li><li>প্রতিটি দাবি ও লিংক যাচাই।</li><li>যোগ্য চিকিৎসা পেশাজীবীর পর্যালোচনা।</li><li>অনুমোদনের পর তারিখসহ প্রকাশ।</li></ol><h2>সংশোধন নীতি</h2><p>ভুল জানালে আমরা দ্রুত যাচাই করে সংশোধন করব এবং হালনাগাদের তারিখ দেব।</p><h2>বিজ্ঞাপন</h2><p>বিজ্ঞাপন (যদি থাকে) সম্পাদকীয় সিদ্ধান্তকে প্রভাবিত করবে না।</p>")

page("login.html","লগইন / নতুন অ্যাকাউন্ট",'<div class="tabs" role="tablist"><button type="button" role="tab" id="tin" aria-selected="true">লগইন</button><button type="button" role="tab" id="tup" aria-selected="false">নতুন অ্যাকাউন্ট</button></div><form id="loginForm" class="frm"><label for="em">ইমেইল</label><input id="em" type="email" autocomplete="email" required><label for="pw">পাসওয়ার্ড (অন্তত ৮ অক্ষর)</label><input id="pw" type="password" autocomplete="current-password" required><div id="pw2w" hidden><label for="pw2">পাসওয়ার্ড আবার লিখুন</label><input id="pw2" type="password" autocomplete="new-password"></div><div id="mfaw" hidden><label for="mfac">অথেন্টিকেটর কোড (৬ সংখ্যা)</label><input id="mfac" inputmode="numeric" maxlength="6" autocomplete="one-time-code"></div><button id="bgo" type="submit">লগইন করুন</button><p id="lmsg" role="status" class="msg"></p></form><p class="sm">অ্যাকাউন্ট দিয়ে নিবন্ধ সংরক্ষণ ও মতামত দেওয়া যায়। <a href="privacy-policy.html">গোপনীয়তা নীতি</a></p>')
page("account.html","আমার অ্যাকাউন্ট",'<div id="account"><p id="amsg" role="status" class="msg"></p><p>ইমেইল: <strong id="who"></strong> <button id="out" type="button">লগআউট</button></p><h2>দুই-ধাপে যাচাই (MFA)</h2><p class="sm">অ্যাডমিনের জন্য বাধ্যতামূলক; সবার জন্য সুপারিশ করা হয়।</p><p id="mfamsg" role="status" class="msg"></p><div id="mfabox"></div><h2>সংরক্ষিত নিবন্ধ</h2><ul id="savedList"></ul></div>')
page("admin.html","অ্যাডমিন প্যানেল",'<p id="adm" class="msg" role="status"></p><div id="adminApp" hidden><form id="pform" class="frm"><label for="f_slug">স্লাগ (ইংরেজি, যেমন: my-article)</label><input id="f_slug" required><label for="f_title">শিরোনাম</label><input id="f_title" required><label for="cat">বিভাগ</label><select id="cat"></select><label for="f_summary">সারসংক্ষেপ</label><input id="f_summary"><label for="f_image">ছবির ফাইলের নাম (assets/img/ ফোল্ডারে আপলোড করা, যেমন water.webp)</label><input id="f_image" maxlength="90"><label for="f_image_alt">ছবির বর্ণনা (alt)</label><input id="f_image_alt" maxlength="200"><label for="f_body">মূল লেখা (নতুন অনুচ্ছেদের মাঝে ফাঁকা লাইন; শিরোনামের জন্য লাইনের শুরুতে ## )</label><textarea id="f_body" rows="14" required></textarea><label for="status">অবস্থা</label><select id="status"><option value="draft">খসড়া</option><option value="published">প্রকাশিত</option></select><label><input id="reviewed" type="checkbox"> যোগ্য চিকিৎসা পেশাজীবী পর্যালোচনা করেছেন</label><button>সংরক্ষণ</button></form><p id="amsg2" class="msg" role="status"></p><h2>নিউজলেটার গ্রাহক</h2><p id="subc"></p><button id="subx" type="button">CSV ডাউনলোড</button><h2>সব নিবন্ধ</h2><ul id="plist"></ul><h2>সাম্প্রতিক মতামত</h2><ul id="flist"></ul></div>')
page("post.html","নিবন্ধ",'<div id="postView"><p id="pmsg" class="msg" role="status">লোড হচ্ছে…</p><article class="art" id="postBody"></article></div>')
page("unsubscribe.html","আনসাবস্ক্রাইব",'<p id="usmsg" class="msg" role="status">লোড হচ্ছে…</p><button id="usgo" type="button" hidden>আনসাবস্ক্রাইব নিশ্চিত করুন</button>')
for f in ("login.html","account.html","admin.html","unsubscribe.html"):
    t=open(f,encoding="utf-8").read().replace("</head>",'<meta name="robots" content="noindex"></head>',1); open(f,"w",encoding="utf-8").write(t)
w("404.html",head("পাতা পাওয়া যায়নি","পাতাটি পাওয়া যায়নি।",BP,"404.html")+'<h1>পাতা পাওয়া যায়নি</h1><p><a href="'+BP+'index.html">হোমপেজে ফিরুন</a></p>'+foot(BP))
w("assets/articles.js","window.ARTICLES="+json.dumps([{"s":a[0],"t":a[1],"c":a[2],"d":a[3],**({"i":img(a[0])} if img(a[0]) else {})} for a in A],ensure_ascii=False)+";window.CATNAMES="+json.dumps(cn,ensure_ascii=False)+";window.ICONS="+json.dumps({c[0]:ico(c[0]) for c in CATS},ensure_ascii=False)+";")
w("script.js","""(function(){var b=document.querySelector('.mb'),n=document.getElementById('nav');
if(b)b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
var L=document.getElementById('list');if(!L)return;var C=window.ARTICLES,cat='',q=new URLSearchParams(location.search).get('q')||'';
var CN="""+json.dumps(cn,ensure_ascii=False)+""";
function r(){var t=q.trim().toLowerCase();var m=C.filter(function(a){return(!cat||a.c===cat)&&(!t||(a.t+a.d).toLowerCase().indexOf(t)>-1)});
L.innerHTML=m.map(function(a){return '<article class="card"><div class="th">'+(a.i?'<img src="assets/img/'+E(a.i)+'" alt="" loading="lazy" width="600" height="315">':(ICONS[a.c]||''))+'</div><span class="tag">'+E(CN[a.c]||'')+'</span><h3><a href="'+(a.db?'post.html?s='+encodeURIComponent(a.s):'articles/'+encodeURIComponent(a.s)+'.html')+'">'+E(a.t)+'</a></h3><p>'+E(a.d)+'</p></article>'}).join('');
if(window.reveal)reveal();document.getElementById('status').textContent=m.length?m.length+'টি নিবন্ধ পাওয়া গেছে।':'কোনো নিবন্ধ পাওয়া যায়নি। অন্য শব্দ দিয়ে খুঁজুন বা সব বিভাগ দেখুন।'}
window.rerender=r;document.getElementById('chips').addEventListener('click',function(e){var x=e.target.closest('button');if(!x)return;cat=x.dataset.c;
document.querySelectorAll('#chips button').forEach(function(y){y.classList.toggle('on',y===x)});r()});
var i=document.getElementById('q');if(i)i.value=q;r()})();"""+open('anim.js',encoding='utf-8').read()+"reveal();")
w("style.css",""":root{--g:#0f766e;--d:#134e4a;--l:#ecfdf5;--t:#1f2937}*{box-sizing:border-box}body{margin:0;font-family:'Hind Siliguri','Noto Sans Bengali',sans-serif;color:var(--t);line-height:1.8;background:#fff}
.w{max-width:1100px;margin:auto;padding:0 16px}a{color:var(--g)}:focus-visible{outline:3px solid #f59e0b;outline-offset:2px}.sr,.skip:not(:focus){position:absolute;left:-9999px}
.hd{border-bottom:1px solid #e5e7eb;position:sticky;top:0;background:#fff;z-index:5}.hdi{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:8px 16px}.logo{font-weight:700;font-size:1.5rem;text-decoration:none;color:var(--d);display:inline-flex;align-items:center;gap:8px}.logo svg{width:30px;height:30px;color:var(--g);flex:none}.logo .mir{transform:scaleX(-1)}
nav#nav{display:none;width:100%;flex-direction:column}nav#nav.open{display:flex}nav#nav a{padding:6px 0;text-decoration:none}.mb{margin-left:auto}.sf{display:flex;gap:4px;width:100%}.sf input{flex:1}
input,button{font:inherit;padding:6px 12px;border:1px solid #9ca3af;border-radius:8px;background:#fff;color:#1f2937}button{cursor:pointer}.chips button.on{background:var(--g);color:#fff}.chips{display:flex;flex-wrap:wrap;gap:8px}
.hero{background:var(--l);padding:32px 16px;margin:16px 0;border-radius:12px}.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
.card{border:1px solid #e5e7eb;border-radius:12px;padding:16px}.card h3{margin:4px 0}.card a{text-decoration:none;color:var(--d)}.big{background:#f0fdfa}.tag{background:var(--l);color:var(--d);padding:2px 8px;border-radius:99px;font-size:.85rem}
.sm{font-size:.9rem;color:#4b5563}.box,.toc{background:var(--l);padding:16px;border-radius:12px;margin:24px 0}.warn{background:#fffbeb;border:1px solid #f59e0b;padding:12px;border-radius:8px;margin:16px 0}
.th{height:110px;border-radius:8px;overflow:hidden;margin-bottom:8px}.th svg{width:100%;height:100%;display:block}.ban{height:200px}.hi{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.hi .th{height:130px;margin:0}.hero{display:grid;gap:16px;align-items:center}@media(min-width:800px){.hero{grid-template-columns:1fr 1fr}}.art{max-width:760px}.ft{background:var(--d);color:#fff;padding:16px 0;margin-top:40px}.ft a{color:#a7f3d0}.bc{font-size:.9rem;margin:12px 0}
@media(min-width:800px){.mb{display:none}nav#nav{display:flex;flex-direction:row;flex-wrap:wrap;gap:12px;width:auto;order:3}.sf{width:auto;margin-left:auto}}"""+open('anim.css',encoding='utf-8').read())
w("robots.txt",f"User-agent: *\nDisallow: /admin.html\nDisallow: /account.html\nDisallow: /login.html\nDisallow: /unsubscribe.html\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
urls=["index.html","about.html","contact.html","privacy-policy.html","disclaimer.html","editorial-policy.html"]+[f"categories/{c[0]}.html" for c in CATS]+[f"articles/{a[0]}.html" for a in A]
w("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}/{u}</loc></url>" for u in urls)+"</urlset>")
w("README.md","""# সুস্থ বাংলা
## লোকালি চালান
`python3 -m http.server 8000` তারপর http://localhost:8000
## GitHub Pages
1. GitHub-এ repo বানিয়ে সব ফাইল আপলোড করুন (index.html রুটে)।
2. Settings → Pages → Branch `main`, folder `/ (root)` → Save।
3. `build.py`-এর `BASE` এবং robots.txt/sitemap.xml/canonical-এর `YOUR-USERNAME` নিজের URL দিয়ে বদলান (`python3 build.py` আবার চালালে সব হালনাগাদ হবে)।
4. Google Search Console-এ সাইট যোগ করে sitemap.xml জমা দিন। কাস্টম ডোমেইন Pages সেটিংসে যোগ করুন।
## লগইন, সংরক্ষণ, মতামত ও অ্যাডমিন (Supabase, বিনামূল্যের প্ল্যান)
1. supabase.com-এ প্রজেক্ট খুলুন; SQL Editor-এ `supabase_setup.sql` চালান।
2. Authentication-এ ইমেইল নিশ্চিতকরণ চালু রাখুন, ন্যূনতম পাসওয়ার্ড ৮+ করুন, Site URL-এ নিজের সাইটের ঠিকানা দিন।
3. Project Settings → API থেকে URL ও anon (publishable) কী `config.js`-এ বসান। **service_role কী কখনো বসাবেন না।**
4. সাইটে সাইন-আপ করুন, তারপর SQL-ফাইলের শেষের মন্তব্য অনুযায়ী নিজের UUID `admins` টেবিলে যোগ করুন। এরপর `admin.html` থেকে নিবন্ধ যোগ/সম্পাদনা/মুছতে পারবেন।
- অ্যাডমিন-অধিকার ব্রাউজারে নয়, ডাটাবেসের RLS নিয়মে নিয়ন্ত্রিত।
- ডাটাবেসের নিবন্ধ (`post.html?s=...`) ব্রাউজারে লোড হয়, তাই সার্চ ইঞ্জিনে স্ট্যাটিক নিবন্ধের চেয়ে দুর্বল। গুরুত্বপূর্ণ নিবন্ধ চূড়ান্ত হলে স্ট্যাটিক পাতা হিসেবেও রাখুন।
- স্প্যাম ঠেকাতে Supabase-এর রেট লিমিট/CAPTCHA সেটিংস দেখুন।
## নিরাপত্তা (সংক্ষেপে; বিস্তারিত `SECURITY.md`)
- সব ডাটা-অ্যাক্সেস Supabase RLS দিয়ে সার্ভারে নিয়ন্ত্রিত; অ্যাডমিনের জন্য MFA (aal2) বাধ্যতামূলক।
- `supabase_setup.sql`-এর শেষে `HARDENING` অংশ (সীমা, রেট-লিমিট ট্রিগার, ন্যূনতম অধিকার) অবশ্যই চালান।
- Cloudflare Pages ব্যবহার করলে `_headers` ফাইল কাজ করে; GitHub Pages হেডার সেট করতে দেয় না (শুধু `<meta>` CSP থাকে)।
## নিবন্ধ যোগ করা (content/ ফোল্ডার)
1. `content/PROMPT.md`-এর প্রম্পট দিয়ে AI-কে লেখা বানাতে বলুন; ফলাফল `content/<স্লাগ>.md` নামে রাখুন (বিষয়ের তালিকা `content/PLAN.md`)।
2. **প্রতিটি দাবি ও লিংক যাচাই করুন এবং যোগ্য চিকিৎসা পেশাজীবীকে দিয়ে পর্যালোচনা করান।** সূত্র (`- নাম | https://...`) না থাকলে নিবন্ধ বাদ পড়ে।
3. `python3 gen_images.py` (ছবি, দরকার হলে) তারপর `python3 build.py`; সব পাতা, সূচি, সাইটম্যাপ নিজে তৈরি হবে। তারপর আপলোড করুন।
## AdSense
শুধু আসল, পর্যালোচিত কনটেন্ট হলেই আবেদন করুন; অনুমোদনের গ্যারান্টি নেই। নিবন্ধ পাতায় `AD PLACEHOLDER` কমেন্টে নিজের অনুমোদিত কোড বসাবেন। কোনো ভুয়া publisher ID ব্যবহার করবেন না।
## প্রকাশের আগে চেকলিস্ট
- [ ] সব লিংক ও তথ্যসূত্র খুলে মিলিয়েছেন
- [ ] যোগ্য চিকিৎসক প্রতিটি নিবন্ধ পর্যালোচনা করেছেন; লেখক/রিভিউয়ার ও তারিখ বসেছে, "খসড়া" সতর্কতা সরেছে
- [ ] মোবাইল/ট্যাবলেট/ডেস্কটপ লেআউট, কিবোর্ড ফোকাস, কনট্রাস্ট
- [ ] মেটা, canonical, sitemap, 404, contact ইমেইল
- [ ] অনুসন্ধান ও ক্যাটাগরি ফিল্টার কাজ করছে
""")

w("_headers",f"""/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' {SBO}; base-uri 'self'; form-action 'self'; object-src 'none'; frame-ancestors 'none'
""")
