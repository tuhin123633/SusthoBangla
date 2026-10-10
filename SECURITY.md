# নিরাপত্তা নোট
| বিষয় | অবস্থা |
|---|---|
| SQL injection | কোনো কাঁচা SQL নেই; supabase-js প্যারামিটারাইজড অনুরোধ পাঠায়। SQL ফাংশনে `search_path` স্থির। |
| XSS | ডাটাবেসের লেখা শুধু `textContent` বা `E()` এস্কেপ করে দেখানো হয়; CSP `script-src 'self'`; Supabase লাইব্রেরি নিজের সার্ভার থেকে (`assets/vendor`)। |
| CSRF | সেশন কুকি নয়, `Authorization` বেয়ারার টোকেন; তাই ক্লাসিক CSRF প্রযোজ্য নয়। অতিরিক্ত: `form-action 'self'`, ফ্রেম-ব্লক। টোকেন localStorage-এ থাকে, তাই XSS প্রতিরোধই আসল ঢাল। |
| ফাইল আপলোড | সাইটে আপলোড সুবিধা নেই। ভবিষ্যতে Storage যোগ করলে বাকেট-নীতি, টাইপ/সাইজ সীমা ও সার্ভার-সাইড যাচাই আবশ্যক। |
| SSRF | সাইটে সার্ভার-সাইড কোড বা ইউআরএল-ফেচ নেই। ভবিষ্যতে Edge Function-এ ইউআরএল ফেচ করলে অ্যালাউ-লিস্ট দিন। |
| BOLA/IDOR | RLS: `saved` ও `feedback` শুধু নিজের সারি; `posts` লেখা শুধু অ্যাডমিন; `admins`-এ ক্লায়েন্ট থেকে লেখা বন্ধ। |
| রেট লিমিট | ডাটাবেস ট্রিগার (ফিডব্যাক ঘণ্টায় ৫, সংরক্ষণ সর্বোচ্চ ২০০) + Supabase Auth-এর বিল্ট-ইন সীমা (Dashboard → Authentication → Rate Limits)। ক্লায়েন্ট-সাইড সীমা নিরাপত্তা নয়। |
| পাসওয়ার্ড হ্যাশ | Supabase Auth নিজে bcrypt দিয়ে হ্যাশ করে; আমরা কখনো পাসওয়ার্ড সংরক্ষণ করি না। |
| MFA | TOTP (অ্যাকাউন্ট পাতা)। অ্যাডমিন অধিকার `aal2` ছাড়া RLS-এ কাজ করে না। |
| অনুমতি | ক্লায়েন্টের "অ্যাডমিন" পরীক্ষা শুধু UI; আসল নিয়ন্ত্রণ RLS + `is_admin()`। |
## আপনাকে ড্যাশবোর্ডে যা করতে হবে
1. Authentication → Providers → Email: ইমেইল নিশ্চিতকরণ চালু, ন্যূনতম পাসওয়ার্ড ১০+ , (প্ল্যানে থাকলে) leaked-password protection চালু।
2. Authentication → Multi-Factor: TOTP চালু।
3. Authentication → Attack Protection: CAPTCHA (Turnstile/hCaptcha) চালু করতে চাইলে সাইট-কী লাগবে; ক্লায়েন্টে টোকেন পাঠানোর কোড আলাদা করে যোগ করতে হবে (এখনো যোগ করা নেই)।
4. Authentication → URL Configuration: Site URL শুধু নিজের ডোমেইন।
5. SQL Editor-এ `select tablename,rowsecurity from pg_tables where schemaname='public';` চালিয়ে সব `true` নিশ্চিত করুন।
6. `config.js`-এ কেবল anon/publishable কী; service_role কখনো নয়।

## দ্বিতীয় ধাপের নিরাপত্তা
| বিষয় | অবস্থা |
|---|---|
| JWT secret / API secret | সাইটে কোনো গোপন কী নেই (স্ক্যান করা হয়েছে)। শুধু anon কী `config.js`-এ। JWT secret ও service_role শুধু Supabase ড্যাশবোর্ডে; ফাঁস হলে Project Settings → API/JWT Keys থেকে রোটেট করুন। |
| টোকেন localStorage থেকে | সেশন এখন `sessionStorage`-এ (ট্যাব বন্ধ হলে মুছে যায়); পুরোনো `sb-*` localStorage কী মুছে ফেলা হয়। সীমাবদ্ধতা: XSS হলে `sessionStorage`-ও পড়া যায়; আসল httpOnly কুকি পেতে সার্ভার (যেমন Cloudflare Pages Functions + `@supabase/ssr`) লাগবে। নতুন ট্যাবে আবার লগইন করতে হয়। |
| ডিফল্ট ক্রেডেনশিয়াল | কোডে কোনো ডিফল্ট ইউজার/পাসওয়ার্ড নেই। আপনি: Supabase ডাটাবেস পাসওয়ার্ড নতুন করুন, Supabase ও GitHub অ্যাকাউন্টে 2FA দিন, `contact.html`-এ নিজের ইমেইল বসান। |
| CORS | Supabase API CORS ড্রাশবোর্ড থেকে ডোমেইন-ভিত্তিক করা যায় না (ব্রাউজার ব্যবহারের জন্য খোলা; সুরক্ষা RLS+JWT)। আমরা CSP `connect-src` শুধু আপনার প্রজেক্ট URL-এ সীমিত করি (`config.js`-এ URL দিয়ে `python3 build.py` চালালে নিজে বসে), এবং Auth → URL Configuration-এ Redirect URL শুধু নিজের ডোমেইন রাখুন। ভবিষ্যতে Edge Function: `Access-Control-Allow-Origin` কখনো `*` নয়। |
| Webhook signature | সাইটে কোনো webhook রিসিভার নেই। যোগ করলে: কাঁচা বডিতে HMAC-SHA256, constant-time তুলনা, টাইমস্ট্যাম্প সীমা, রিপ্লে প্রতিরোধ। |
| Sourcemap | কোনো `.map` ফাইল বা `sourceMappingURL` নেই। |
| লগ | কোডে `console.*` নেই; UI-তে সার্ভারের কাঁচা এরর (টেবিল/পলিসির নাম) দেখানো হয় না, সাধারণ বার্তা। টোকেন/ইমেইল/পাসওয়ার্ড কোথাও লগ হয় না। |
| ডিপেন্ডেন্সি | একমাত্র লাইব্রেরি `@supabase/supabase-js@2.117.2` (প্রকাশ ২০২৬-০৯-২৫, ১৪+ দিন পুরোনো); `npm audit`: ০ দুর্বলতা। নিয়মিত হালনাগাদ করুন, `assets/vendor/` প্রতিস্থাপন করে। |
## নিউজলেটার
- গ্রাহক তালিকা `subscribers` টেবিলে; ক্লায়েন্ট (anon) শুধু `subscribe()` ফাংশন চালাতে পারে, তালিকা পড়তে পারে না। শুধু MFA-যাচাইকৃত অ্যাডমিন পড়তে/মুছতে পারে।
- হানিপট ফিল্ড, ক্লায়েন্ট-সাইড বিরতি, ডাটাবেসে ইমেইল ফরম্যাট/সংখ্যার সীমা (ঘণ্টায় ২০০)। একই ইমেইল আবার দিলে আলাদা উত্তর দেয় না (গ্রাহক আছে কি না বোঝা যায় না)।
- সীমাবদ্ধতা: নিশ্চিতকরণ ইমেইল (double opt-in) নেই, কারণ সাইট ইমেইল পাঠাতে পারে না। অন্যের ইমেইল দিয়ে কেউ সাইন-আপ করতে পারে; তাই প্রথম ইমেইলে নিশ্চিতকরণ চাইলে Brevo/Buttondown/MailerLite-এর মতো সেবা ব্যবহার করুন। CAPTCHA যোগ করলে স্প্যাম কমবে।
- আনসাবস্ক্রাইব: CSV-এর `unsubscribe_link` প্রতিটি ইমেইলে বসান (টোকেন ছাড়া কেউ অন্যকে সরাতে পারে না)।
