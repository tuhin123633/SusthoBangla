(function(){var b=document.querySelector('.mb'),n=document.getElementById('nav');
if(b)b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
var L=document.getElementById('list');if(!L)return;var C=window.ARTICLES,cat='',q=new URLSearchParams(location.search).get('q')||'';
var CN={"common-diseases": "রোগ ও লক্ষণ", "nutrition": "পুষ্টি", "fitness": "ফিটনেস", "mental-health": "মানসিক স্বাস্থ্য", "womens-health": "নারী স্বাস্থ্য", "childrens-health": "শিশু স্বাস্থ্য", "lifestyle": "সুস্থ জীবনযাপন", "prevention": "প্রতিরোধমূলক স্বাস্থ্য"};
function r(){var t=q.trim().toLowerCase();var m=C.filter(function(a){return(!cat||a.c===cat)&&(!t||(a.t+a.d).toLowerCase().indexOf(t)>-1)});
L.innerHTML=m.map(function(a){return '<article class="card"><div class="th">'+(a.i?'<img src="assets/img/'+E(a.i)+'" alt="" loading="lazy" width="600" height="315">':(ICONS[a.c]||''))+'</div><span class="tag">'+E(CN[a.c]||'')+'</span><h3><a href="'+(a.db?'post.html?s='+encodeURIComponent(a.s):'articles/'+encodeURIComponent(a.s)+'.html')+'">'+E(a.t)+'</a></h3><p>'+E(a.d)+'</p></article>'}).join('');
if(window.reveal)reveal();document.getElementById('status').textContent=m.length?m.length+'টি নিবন্ধ পাওয়া গেছে।':'কোনো নিবন্ধ পাওয়া যায়নি। অন্য শব্দ দিয়ে খুঁজুন বা সব বিভাগ দেখুন।'}
window.rerender=r;document.getElementById('chips').addEventListener('click',function(e){var x=e.target.closest('button');if(!x)return;cat=x.dataset.c;
document.querySelectorAll('#chips button').forEach(function(y){y.classList.toggle('on',y===x)});r()});
var i=document.getElementById('q');if(i)i.value=q;r()})();function E(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function reveal(){var els=document.querySelectorAll('.card:not(.rv)');
if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){els.forEach(function(e){e.classList.add('rv','in')});return}
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){var t=en.target;t.classList.add('in');io.unobserve(t);setTimeout(function(){t.style.transitionDelay=''},900)}})},{threshold:.1});
els.forEach(function(e,i){e.classList.add('rv');e.style.transitionDelay=(i%4)*70+'ms';io.observe(e)})}
(function(){var h=document.querySelector('.hd');if(h)window.addEventListener('scroll',function(){h.classList.toggle('sc',window.scrollY>8)},{passive:true})})();
function fitMenu(){var n=document.getElementById('nav');if(!n)return;document.documentElement.classList.add('js');
var m=n.querySelector('.more'),pop=n.querySelector('.mpop');if(!m||!pop)return;
Array.prototype.slice.call(pop.children).forEach(function(a){n.insertBefore(a,m)});n.classList.remove('ov');m.hidden=true;pop.hidden=true;m.querySelector('button').setAttribute('aria-expanded','false');
var L=Array.prototype.slice.call(n.children).filter(function(e){return e.tagName=='A'});
function tot(){var w=0;L.forEach(function(a){if(a.parentNode===n)w+=a.offsetWidth+6});return w}
if(tot()<=n.clientWidth)return;m.hidden=false;n.classList.add('ov');var mw=m.offsetWidth+6;
for(var i=L.length-1;i>=0&&tot()+mw>n.clientWidth;i--)pop.insertBefore(L[i],pop.firstChild)}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.mbtn'),pop=document.querySelector('.mpop');if(!pop)return;
if(b){var open=pop.hidden;pop.hidden=!open;b.setAttribute('aria-expanded',open);if(open){pop.style.left='0';pop.style.right='auto';var r=pop.getBoundingClientRect();if(r.right>innerWidth-8){pop.style.left='auto';pop.style.right='0'}}}
else if(!e.target.closest('.mpop')){pop.hidden=true;var x=document.querySelector('.mbtn');if(x)x.setAttribute('aria-expanded','false')}});
document.addEventListener('keydown',function(e){if(e.key=='Escape'){var p=document.querySelector('.mpop');if(p)p.hidden=true}});
window.addEventListener('resize',fitMenu);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fitMenu);fitMenu();
reveal();