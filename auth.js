(function(){
if(!window.__BUNDLE&&top!==self){try{top.location=self.location}catch(e){document.documentElement.hidden=true}}
var C=window.SB_CONFIG||{},sb=null,U=null,ADM=false,CATS=window.CATNAMES||{};
var CDN=(function(){var l=document.querySelector('.logo');return(l?l.getAttribute('href').replace('index.html',''):'')+'assets/vendor/supabase.js'})();
var ready=new Promise(function(res){if(!(C.url&&C.key))return res();var s=document.createElement('script');s.src=CDN;
s.onload=function(){try{Object.keys(localStorage).forEach(function(k){if(k.indexOf('sb-')==0)localStorage.removeItem(k)})}catch(e){}
sb=window.supabase.createClient(C.url,C.key,{auth:{storage:window.sessionStorage,persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});res()};s.onerror=res;document.head.appendChild(s)});
function $(i){return document.getElementById(i)}
function el(t,x,c){var e=document.createElement(t);if(x)e.textContent=x;if(c)e.className=c;return e}
function P(){var l=document.querySelector('.logo');return l?l.getAttribute('href').replace('index.html',''):''}
function say(i,t,bad){var e=$(i);if(e){e.textContent=t;e.className='msg'+(bad?' bad':'')}}
function ER(e){return e&&/সীমা/.test(e.message||'')?e.message:'ব্যর্থ হয়েছে, আবার চেষ্টা করুন।'}
function nosb(i){say(i,'লগইন সেবা এখনো যুক্ত নয়। config.js-এ Supabase তথ্য দিন (README দেখুন)।',1)}
function slug(){var m=(location.hash+location.pathname).match(/articles\/([\w-]+)\.html/);if(m)return m[1];m=location.search.match(/[?&]s=([\w-]+)/);return m?m[1]:''}
async function who(){U=null;ADM=false;if(!sb)return;try{var r=await sb.auth.getUser();U=(r.data&&r.data.user)||null;
if(U){var a=await sb.from('admins').select('user_id').eq('user_id',U.id);ADM=!!(a.data&&a.data.length)}}catch(e){}}
function login(){var f=$('loginForm');if(!f)return;var up=/new/.test(location.hash+location.search),pend=null;
function mode(u){up=u;$('tin').setAttribute('aria-selected',!u);$('tup').setAttribute('aria-selected',u);$('pw2w').hidden=!u;$('pw2').required=u;
$('bgo').textContent=u?'অ্যাকাউন্ট তৈরি করুন':'লগইন করুন';$('pw').autocomplete=u?'new-password':'current-password';say('lmsg','');if(!sb)nosb('lmsg')}
$('tin').onclick=function(){mode(false)};$('tup').onclick=function(){mode(true)};mode(up);if(!sb)return;
f.onsubmit=async function(e){e.preventDefault();
if(pend){var v=await sb.auth.mfa.challengeAndVerify({factorId:pend,code:$('mfac').value.trim()});if(v.error){say('lmsg','কোড ভুল হয়েছে।',1);return}location.href=P()+'account.html';return}
var em=$('em').value.trim(),pw=$('pw').value;
if(!em||pw.length<8){say('lmsg','ইমেইল দিন এবং অন্তত ৮ অক্ষরের পাসওয়ার্ড দিন।',1);return}
if(up&&pw!==$('pw2').value){say('lmsg','দুটি পাসওয়ার্ড মেলেনি।',1);return}
var r=up?await sb.auth.signUp({email:em,password:pw}):await sb.auth.signInWithPassword({email:em,password:pw});
if(r.error){say('lmsg',(up?'অ্যাকাউন্ট তৈরি করা যায়নি; তথ্য দেখে আবার চেষ্টা করুন।':'ইমেইল/পাসওয়ার্ড সঠিক নয়, অথবা ইমেইল নিশ্চিত করা হয়নি।'),1);return}
if(up&&!r.data.session){say('lmsg','অ্যাকাউন্ট তৈরি হয়েছে। ইমেইলে পাঠানো লিংকে নিশ্চিত করে লগইন করুন।');return}
var a=await sb.auth.mfa.getAuthenticatorAssuranceLevel();
if(a.data&&a.data.nextLevel=='aal2'&&a.data.currentLevel!='aal2'){var fl=await sb.auth.mfa.listFactors();pend=fl.data.totp[0].id;$('mfaw').hidden=false;$('bgo').textContent='যাচাই করুন';say('lmsg','অথেন্টিকেটর অ্যাপের ৬ সংখ্যার কোড দিন।');$('mfac').focus();return}
location.href=P()+'account.html'}}
async function mfaUI(){var box=$('mfabox');if(!box)return;box.textContent='';var fl=await sb.auth.mfa.listFactors(),ver=(fl.data&&fl.data.totp)||[];
if(ver.length){var p=el('p','MFA চালু আছে (অথেন্টিকেটর অ্যাপ)। '),rm=el('button','বন্ধ করুন');rm.type='button';
rm.onclick=async function(){var r=await sb.auth.mfa.unenroll({factorId:ver[0].id});say('mfamsg',r.error?ER(r.error):'MFA বন্ধ হয়েছে।',!!r.error);mfaUI()};box.append(p,rm);return}
var b=el('button','MFA চালু করুন');b.type='button';
b.onclick=async function(){var old=((fl.data&&fl.data.all)||[]).filter(function(f){return f.status=='unverified'});for(var i=0;i<old.length;i++)await sb.auth.mfa.unenroll({factorId:old[i].id});
var r=await sb.auth.mfa.enroll({factorType:'totp'});if(r.error){say('mfamsg',ER(r.error),1);return}
var d=r.data,img=document.createElement('img');img.src=d.totp.qr_code;img.alt='অথেন্টিকেটর অ্যাপে স্ক্যান করার QR কোড';img.width=180;img.height=180;
var sec=el('p','অথবা কোড হাতে লিখুন: '+d.totp.secret),inp=document.createElement('input');inp.inputMode='numeric';inp.maxLength=6;inp.setAttribute('aria-label','অথেন্টিকেটর কোড');
var ok=el('button','যাচাই করুন');ok.type='button';
ok.onclick=async function(){var c=await sb.auth.mfa.challenge({factorId:d.id});if(c.error){say('mfamsg',ER(c.error),1);return}
var v=await sb.auth.mfa.verify({factorId:d.id,challengeId:c.data.id,code:inp.value.trim()});say('mfamsg',v.error?'কোড ভুল হয়েছে।':'MFA চালু হয়েছে।',!!v.error);if(!v.error)mfaUI()};
box.textContent='';box.append(img,sec,inp,ok)};box.appendChild(b)}
async function account(){if(!$('account'))return;if(!sb){nosb('amsg');return}if(!U){say('amsg','অ্যাকাউন্ট দেখতে লগইন করুন।',1);return}
mfaUI();$('who').textContent=U.email;$('out').onclick=async function(){await sb.auth.signOut();location.href=P()+'login.html'};
var r=await sb.from('saved').select('post_slug').order('created_at',{ascending:false}),L=$('savedList'),d=r.data||[];L.textContent='';
if(!d.length){L.appendChild(el('li','এখনো কিছু সংরক্ষণ করেননি।'));return}
d.forEach(function(x){var a=(window.ARTICLES||[]).find(function(y){return y.s==x.post_slug}),li=el('li'),k=el('a',a?a.t:x.post_slug);
k.href=P()+(a?'articles/'+x.post_slug+'.html':'post.html?s='+x.post_slug);li.appendChild(k);L.appendChild(li)})}
function widget(){var t=document.querySelector('article.art');if(!t||$('wg'))return;var s=slug();if(!s)return;
var w=el('section','','box');w.id='wg';w.appendChild(el('h2','সংরক্ষণ ও মতামত'));
if(!sb){w.appendChild(el('p','লগইন সেবা এখনো যুক্ত নয়।','msg bad'));t.appendChild(w);return}
if(!U){var p=el('p','সংরক্ষণ বা মতামত দিতে '),a=el('a','লগইন করুন');a.href=P()+'login.html';p.appendChild(a);w.appendChild(p);t.appendChild(w);return}
var b=el('button','সংরক্ষণ করুন'),m=el('p','','msg');b.type='button';m.setAttribute('role','status');
sb.from('saved').select('post_slug').eq('post_slug',s).then(function(r){var on=r.data&&r.data.length;b.textContent=on?'সংরক্ষণ বাতিল':'সংরক্ষণ করুন';b.dataset.on=on?1:''});
b.onclick=async function(){var on=b.dataset.on,r=on?await sb.from('saved').delete().eq('post_slug',s):await sb.from('saved').insert({post_slug:s});
if(r.error){m.textContent=ER(r.error);return}b.dataset.on=on?'':1;b.textContent=on?'সংরক্ষণ করুন':'সংরক্ষণ বাতিল'};
var ta=document.createElement('textarea');ta.maxLength=1000;ta.rows=4;ta.setAttribute('aria-label','আপনার মতামত');
var fb=el('button','মতামত পাঠান');fb.type='button';
fb.onclick=async function(){var v=ta.value.trim();if(!v){m.textContent='মতামত লিখুন।';return}
var r=await sb.from('feedback').insert({post_slug:s,message:v});if(r.error){m.textContent=ER(r.error);return}ta.value='';m.textContent='ধন্যবাদ, মতামত পাঠানো হয়েছে।'};
w.append(b,ta,fb,m);t.appendChild(w)}
async function post(){if(!$('postView'))return;if(!sb){nosb('pmsg');return}var s=slug();if(!s){say('pmsg','নিবন্ধ পাওয়া যায়নি।',1);return}
var r=await sb.from('posts').select('*').eq('slug',s).maybeSingle();if(!r.data){say('pmsg','নিবন্ধ পাওয়া যায়নি।',1);return}
var p=r.data,b=$('postBody');document.title=p.title+' | সুস্থ বাংলা';$('pmsg').textContent='';b.textContent='';
b.appendChild(el('h1',p.title));b.appendChild(el('p',p.summary,'lead'));
if(p.image&&/^[a-z0-9][a-z0-9._-]{0,80}\.(webp|jpg|jpeg|png)$/.test(p.image)){var im=document.createElement('img');im.src=P()+'assets/img/'+p.image;im.alt=p.image_alt||p.title;im.width=1200;im.height=630;im.className='pimg';b.appendChild(im)}
if(!p.reviewed)b.appendChild(el('p','খসড়া: যোগ্য চিকিৎসা পেশাজীবীর পর্যালোচনা এখনও হয়নি।','warn'));
p.body.split(/\n\n+/).forEach(function(x){b.appendChild(x.indexOf('## ')==0?el('h2',x.slice(3)):el('p',x))});
b.appendChild(el('div','এটি সাধারণ শিক্ষামূলক তথ্য; চিকিৎসকের পরামর্শের বিকল্প নয়।','warn'));widget()}
async function admin(){var c=$('adminApp');if(!c)return;if(!sb){nosb('adm');return}if(!U){say('adm','প্রথমে লগইন করুন।',1);return}
if(!ADM){say('adm','এই পাতা শুধু অ্যাডমিনের জন্য।',1);return}
var al=await sb.auth.mfa.getAuthenticatorAssuranceLevel();if(!al.data||al.data.currentLevel!='aal2'){say('adm','অ্যাডমিন হতে MFA লাগবে। অ্যাকাউন্ট পাতায় MFA চালু করে কোডসহ আবার লগইন করুন।',1);return}
$('adm').textContent='';c.hidden=false;var cs=$('cat');cs.textContent='';
Object.keys(CATS).forEach(function(k){var o=el('option',CATS[k]);o.value=k;cs.appendChild(o)});var L=$('plist');
async function load(){var r=await sb.from('posts').select('slug,title,status').order('updated_at',{ascending:false});L.textContent='';
(r.data||[]).forEach(function(p){var li=el('li',p.title+' ('+(p.status=='published'?'প্রকাশিত':'খসড়া')+')'),e=el('button','সম্পাদনা'),x=el('button','মুছুন');e.type=x.type='button';
e.onclick=async function(){var q=await sb.from('posts').select('*').eq('slug',p.slug).single(),d=q.data;
['slug','title','summary','body','image','image_alt'].forEach(function(k){$('f_'+k).value=d[k]||''});$('cat').value=d.category;$('status').value=d.status;$('reviewed').checked=!!d.reviewed;$('f_slug').readOnly=true;window.scrollTo(0,0)};
x.onclick=async function(){if(!confirm('"'+p.title+'" মুছে ফেলবেন?'))return;var q=await sb.from('posts').delete().eq('slug',p.slug);
say('amsg2',q.error?ER(q.error):'মুছে ফেলা হয়েছে।',!!q.error);load()};li.append(e,x);L.appendChild(li)})}
$('pform').onsubmit=async function(ev){ev.preventDefault();var s=$('f_slug').value.trim();
if(!/^[a-z0-9-]+$/.test(s)){say('amsg2','স্লাগে শুধু ইংরেজি ছোট হাতের অক্ষর, সংখ্যা ও হাইফেন দিন।',1);return}
var im0=$('f_image').value.trim();if(im0&&!/^[a-z0-9][a-z0-9._-]{0,80}\.(webp|jpg|jpeg|png)$/.test(im0)){say('amsg2','ছবির নাম ঠিক নয় (যেমন: water.webp)।',1);return}
var row={slug:s,title:$('f_title').value.trim(),category:$('cat').value,summary:$('f_summary').value.trim(),image:$('f_image').value.trim()||null,image_alt:$('f_image_alt').value.trim()||null,body:$('f_body').value,status:$('status').value,reviewed:$('reviewed').checked,updated_at:new Date().toISOString()};
var q=await sb.from('posts').upsert(row,{onConflict:'slug'});say('amsg2',q.error?ER(q.error):'সংরক্ষিত হয়েছে।',!!q.error);
if(!q.error){ev.target.reset();$('f_slug').readOnly=false;load()}};
load();var sr=await sb.from('subscribers').select('email,token,consent_at').order('created_at',{ascending:false}).limit(5000),SD=sr.data||[];
$('subc').textContent='মোট গ্রাহক: '+SD.length;
$('subx').onclick=function(){function c(v){v=String(v);return '"'+(/^[=+\-@]/.test(v)?"'"+v:v).replace(/"/g,'""')+'"'}
var base=new URL(P()+'unsubscribe.html',location.href).href;
var rows=['email,consent_at,unsubscribe_link'].concat(SD.map(function(s){return [c(s.email),c(s.consent_at),c(base+'?e='+encodeURIComponent(s.email)+'&t='+s.token)].join(',')}));
var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([rows.join('\n')],{type:'text/csv'}));a.download='subscribers.csv';a.click();setTimeout(function(){URL.revokeObjectURL(a.href)},1500)};
var fr=await sb.from('feedback').select('post_slug,message').order('created_at',{ascending:false}).limit(50),FL=$('flist');
(fr.data||[]).forEach(function(f){FL.appendChild(el('li',f.post_slug+': '+f.message))})}
async function feed(){if(!sb||!$('list')||!window.rerender)return;
var r=await sb.from('posts').select('slug,title,category,summary,image').eq('status','published');
(r.data||[]).forEach(function(p){if(!window.ARTICLES.some(function(a){return a.s==p.slug}))window.ARTICLES.push({s:p.slug,t:p.title,c:p.category,d:p.summary||'',db:1,i:(p.image&&/^[a-z0-9][a-z0-9._-]{0,80}\.(webp|jpg|jpeg|png)$/.test(p.image))?p.image:''})});window.rerender()}
function newsletter(){var f=$('nlForm');if(!f)return;var b=f.querySelector('button[type=submit]'),last=0;
if(!sb){say('nlmsg','নিউজলেটার সেবা এখনো যুক্ত নয় (config.js ও README দেখুন)।',1);b.disabled=true;return}
f.onsubmit=async function(e){e.preventDefault();if($('nlh').value){say('nlmsg','ধন্যবাদ!');return}
var em=$('nle').value.trim().toLowerCase();if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)||em.length>254){say('nlmsg','সঠিক ইমেইল দিন।',1);return}
if(!$('nlc').checked){say('nlmsg','চালিয়ে যেতে সম্মতি দিন।',1);return}
if(Date.now()-last<5000)return;last=Date.now();b.disabled=true;
var r=await sb.rpc('subscribe',{p_email:em});b.disabled=false;
if(r.error){say('nlmsg',ER(r.error),1);return}f.reset();say('nlmsg','ধন্যবাদ! আপনার সাবস্ক্রিপশন নথিভুক্ত হয়েছে। প্রতিটি ইমেইলে আনসাবস্ক্রাইব লিংক থাকবে।')}}
function unsub(){var b=$('usgo');if(!b)return;var q=new URLSearchParams(location.search),em=q.get('e')||'',t=q.get('t')||'';
if(!sb){say('usmsg','সেবা এখনো যুক্ত নয়।',1);return}
if(!/^[0-9a-f-]{36}$/i.test(t)||em.length>254||em.indexOf('@')<1){say('usmsg','লিংকটি সঠিক নয়।',1);return}
say('usmsg',em+' — এই ঠিকানা তালিকা থেকে সরাতে নিশ্চিত করুন।');b.hidden=false;
b.onclick=async function(){b.disabled=true;var r=await sb.rpc('unsubscribe',{p_email:em,p_token:t});
say('usmsg',r.error?ER(r.error):(r.data?'আপনাকে তালিকা থেকে সরানো হয়েছে।':'লিংকটি সঠিক নয় বা আগেই সরানো হয়েছে।'),!!r.error);b.hidden=true}}
async function boot(){await ready;await who();var a=$('authlink');
if(a){a.textContent=U?'আমার অ্যাকাউন্ট':'লগইন';a.href=P()+(U?'account.html':'login.html')}var sg=$('signup');if(sg)sg.hidden=!!U;
login();account();admin();post();if(!$('postView'))widget();feed();newsletter();unsub()}
window.AUTH={boot:boot};if(!window.__BUNDLE)document.addEventListener('DOMContentLoaded',boot);
})();
