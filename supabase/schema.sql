-- ============================================
-- 3AS LG - Schéma Supabase (plan gratuit)
-- Tables: students, messages, courses
-- À exécuter dans Supabase Dashboard > SQL Editor
-- ============================================

-- Extensions
create extension if not exists "pgcrypto";

-- ---------- TABLE students ----------
create table if not exists public.students (
  id uuid primary key default gen_random_uuid(),
  nom text not null,
  prenom text not null,
  email text,
  code_reference text unique not null,
  date_creation timestamptz default now(),
  date_expiration_code timestamptz default (now() + interval '90 days'),
  statut_actif boolean default true,
  informations_personnelles jsonb default '{}'::jsonb
);

create index if not exists idx_students_code on public.students(code_reference);
create index if not exists idx_students_actif on public.students(statut_actif);

-- ---------- TABLE messages ----------
create table if not exists public.messages (
  id uuid primary key default gen_random_uuid(),
  sender_id text not null,
  receiver_id text not null,
  contenu text not null check (char_length(contenu) > 0 and char_length(contenu) <= 5000),
  timestamp timestamptz default now(),
  lu boolean default false,
  -- optionnel : lien élève pour filtrage rapide
  student_id uuid references public.students(id) on delete cascade
);

create index if not exists idx_messages_conversation
  on public.messages(sender_id, receiver_id, timestamp desc);
create index if not exists idx_messages_student on public.messages(student_id, timestamp desc);

-- ---------- TABLE courses ----------
create table if not exists public.courses (
  id uuid primary key default gen_random_uuid(),
  matiere text not null,
  niveau text default '3AS LG',
  chapitre text not null,
  contenu_cours text not null,
  explications_simplifiees text,
  ressources_associees jsonb default '[]'::jsonb,
  ordre int default 0,
  created_at timestamptz default now()
);

create index if not exists idx_courses_matiere on public.courses(matiere, ordre);

-- ---------- Fonction génération code unique ----------
-- Format: 3AS-XXXXXX (alphanumérique majuscules sans ambiguïté)
create or replace function public.generate_reference_code()
returns text language plpgsql as $$
declare
  chars text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  result text := '3AS-';
  i int;
begin
  for i in 1..6 loop
    result := result || substr(chars, (random() * (char_length(chars)-1) + 1)::int, 1);
  end loop;
  -- garantir unicité (retry si collision)
  if exists (select 1 from public.students where code_reference = result) then
    return public.generate_reference_code();
  end if;
  return result;
end;
$$;

-- ---------- Row Level Security (MVP) ----------
-- NOTE: Auth par code custom (pas Supabase Auth).
-- Pour le MVP plan gratuit : politiques permissives pour anon.
-- À durcir ensuite (ex: Edge Function de validation).
alter table public.students enable row level security;
alter table public.messages enable row level security;
alter table public.courses enable row level security;

drop policy if exists "anon all students" on public.students;
create policy "anon all students" on public.students
  for all to anon, authenticated using (true) with check (true);

drop policy if exists "anon all messages" on public.messages;
create policy "anon all messages" on public.messages
  for all to anon, authenticated using (true) with check (true);

drop policy if exists "anon read courses" on public.courses;
create policy "anon read courses" on public.courses
  for select to anon, authenticated using (true);

drop policy if exists "anon write courses" on public.courses;
create policy "anon write courses" on public.courses
  for insert to anon, authenticated with check (true);

-- ---------- Realtime ----------
-- Dans Dashboard > Database > Replication : activer
-- students, messages, courses pour Supabase Realtime.
-- Ou via SQL :
do $$
begin
  if not exists (select 1 from pg_publication_tables where pubname='supabase_realtime' and tablename='messages') then
    alter publication supabase_realtime add table public.messages;
  end if;
  if not exists (select 1 from pg_publication_tables where pubname='supabase_realtime' and tablename='students') then
    alter publication supabase_realtime add table public.students;
  end if;
  if not exists (select 1 from pg_publication_tables where pubname='supabase_realtime' and tablename='courses') then
    alter publication supabase_realtime add table public.courses;
  end if;
exception when others then
  raise notice 'Realtime: à activer manuellement dans Dashboard > Replication si erreur';
end $$;

-- ---------- Vue dashboard admin ----------
create or replace view public.v_student_activity as
select
  s.id, s.nom, s.prenom, s.code_reference,
  s.statut_actif, s.date_expiration_code,
  (select count(*) from public.messages m where m.student_id = s.id) as nb_messages,
  (select max(m.timestamp) from public.messages m where m.student_id = s.id) as derniere_activite
from public.students s;
