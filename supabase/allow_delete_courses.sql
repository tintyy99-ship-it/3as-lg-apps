-- ============================================
-- 3AS LG - Migration : autoriser l'Admin à SUPPRIMER les cours
-- À exécuter UNE FOIS dans Supabase Dashboard > SQL Editor > Run
-- Contexte : le schéma d'origine n'autorisait l'anon qu'en
-- SELECT + INSERT sur public.courses → le bouton admin
-- "Supprimer cours / section / matière" recevait 0 ligne (bloqué RLS).
-- Après ce script, DELETE (+ UPDATE) fonctionne pour l'Admin.
-- (MVP : auth custom par code, comme students/messages.)
-- ============================================

drop policy if exists "anon delete courses" on public.courses;
create policy "anon delete courses" on public.courses
  for delete to anon, authenticated using (true);

drop policy if exists "anon update courses" on public.courses;
create policy "anon update courses" on public.courses
  for update to anon, authenticated using (true) with check (true);
