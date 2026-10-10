-- Supabase Dashboard → SQL Editor-এ একবার চালান
create table public.admins(user_id uuid primary key references auth.users on delete cascade);
create table public.posts(slug text primary key check (slug ~ '^[a-z0-9-]+$'),title text not null,category text not null,summary text,body text not null,
 status text not null default 'draft' check (status in ('draft','published')),reviewed boolean not null default false,created_at timestamptz default now(),updated_at timestamptz default now());
create table public.saved(user_id uuid not null default auth.uid() references auth.users on delete cascade,post_slug text not null,created_at timestamptz default now(),primary key(user_id,post_slug));
create table public.feedback(id bigint generated always as identity primary key,user_id uuid not null default auth.uid() references auth.users on delete cascade,post_slug text not null,
 message text not null check (char_length(message) between 1 and 1000),created_at timestamptz default now());
alter table public.admins enable row level security;alter table public.posts enable row level security;
alter table public.saved enable row level security;alter table public.feedback enable row level security;
create function public.is_admin() returns boolean language sql security definer set search_path=public stable as $$ select exists(select 1 from public.admins where user_id=auth.uid()) $$;
create policy "own admin row" on public.admins for select to authenticated using (user_id=auth.uid());
create policy "read posts" on public.posts for select using (status='published' or public.is_admin());
create policy "admin insert posts" on public.posts for insert to authenticated with check (public.is_admin());
create policy "admin update posts" on public.posts for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "admin delete posts" on public.posts for delete to authenticated using (public.is_admin());
create policy "own saved" on public.saved for all to authenticated using (user_id=auth.uid()) with check (user_id=auth.uid());
create policy "send feedback" on public.feedback for insert to authenticated with check (user_id=auth.uid());
create policy "read feedback" on public.feedback for select to authenticated using (user_id=auth.uid() or public.is_admin());
create policy "admin delete feedback" on public.feedback for delete to authenticated using (public.is_admin());
-- নিজে সাইটে সাইন-আপ করার পর, Authentication → Users থেকে আপনার UUID নিয়ে চালান:
-- insert into public.admins(user_id) values ('আপনার-UUID');

-- ===== HARDENING (আগের সংস্করণ চালিয়ে থাকলে শুধু এই অংশ চালান) =====
create or replace function public.is_admin() returns boolean language sql security definer set search_path=public stable as $$
 select exists(select 1 from public.admins where user_id=auth.uid()) and coalesce(auth.jwt()->>'aal','')='aal2' $$;
revoke all on function public.is_admin() from public; grant execute on function public.is_admin() to anon, authenticated;
alter table public.posts add constraint posts_len check (char_length(title)<=200 and char_length(coalesce(summary,''))<=500 and char_length(body)<=100000);
alter table public.saved add constraint saved_len check (char_length(post_slug)<=100);
alter table public.feedback add constraint fb_len check (char_length(post_slug)<=100);
create or replace function public.limit_feedback() returns trigger language plpgsql security definer set search_path=public as $$
begin if (select count(*) from public.feedback where user_id=new.user_id and created_at>now()-interval '1 hour')>=5 then raise exception 'অনুরোধের সীমা পেরিয়েছে, পরে চেষ্টা করুন'; end if; return new; end $$;
create trigger fb_rate before insert on public.feedback for each row execute function public.limit_feedback();
create or replace function public.limit_saved() returns trigger language plpgsql security definer set search_path=public as $$
begin if (select count(*) from public.saved where user_id=new.user_id)>=200 then raise exception 'সংরক্ষণের সীমা পেরিয়েছে'; end if; return new; end $$;
create trigger saved_rate before insert on public.saved for each row execute function public.limit_saved();
-- ন্যূনতম অধিকার (RLS-এর পাশাপাশি)
revoke all on public.admins, public.saved, public.feedback from anon;
revoke insert,update,delete on public.posts from anon;
revoke insert,update,delete on public.admins from authenticated;
-- যাচাই: সব টেবিলে rowsecurity = true হওয়া চাই
-- select tablename,rowsecurity from pg_tables where schemaname='public';

-- ===== NEWSLETTER (নিউজলেটার চালু করতে এই অংশ চালান) =====
create table public.subscribers(id bigint generated always as identity primary key,
 email text not null unique check (char_length(email)<=254 and email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
 token uuid not null default gen_random_uuid(),consent_at timestamptz not null default now(),created_at timestamptz default now());
alter table public.subscribers enable row level security;
revoke all on public.subscribers from anon, authenticated;
grant select,delete on public.subscribers to authenticated;
create policy "admin read subscribers" on public.subscribers for select to authenticated using (public.is_admin());
create policy "admin delete subscribers" on public.subscribers for delete to authenticated using (public.is_admin());
create or replace function public.subscribe(p_email text) returns void language plpgsql security definer set search_path=public as $$
declare e text := lower(trim(p_email));
begin
 if e is null or char_length(e)>254 or e !~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' then raise exception 'অবৈধ ইমেইল'; end if;
 if (select count(*) from public.subscribers where created_at>now()-interval '1 hour')>=200 then raise exception 'অনুরোধের সীমা পেরিয়েছে, পরে চেষ্টা করুন'; end if;
 insert into public.subscribers(email) values(e) on conflict do nothing;
end $$;
create or replace function public.unsubscribe(p_email text,p_token uuid) returns boolean language plpgsql security definer set search_path=public as $$
begin delete from public.subscribers where email=lower(trim(p_email)) and token=p_token; return found; end $$;
revoke all on function public.subscribe(text), public.unsubscribe(text,uuid) from public;
grant execute on function public.subscribe(text), public.unsubscribe(text,uuid) to anon, authenticated;

-- ===== IMAGES (নিবন্ধে ছবির ফাইলের নাম রাখার কলাম) =====
alter table public.posts add column image text check (image is null or image ~ '^[a-z0-9][a-z0-9._-]{0,80}\.(webp|jpg|jpeg|png)$');
alter table public.posts add column image_alt text check (image_alt is null or char_length(image_alt)<=200);
