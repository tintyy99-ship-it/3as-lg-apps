-- ============================================
-- Seed cours 3AS LG (extrait - à compléter)
-- ============================================

insert into public.courses (matiere, niveau, chapitre, contenu_cours, explications_simplifiees, ressources_associees, ordre) values

-- ===== ALLEMAND =====
('Allemand','3AS LG','1. Passiv (Voix passive)',
'Le Passiv se forme avec werden + Partizip II. Ex: Das Haus wird gebaut. Präteritum: wurde + Partizip II. Perfekt: ist ... worden.',
'Pense comme en français "être + participe". werden = être/ devenir. Astuce débutant: repère wird/wurde/worden = passif. Ex simple: Ich lerne Deutsch → Deutsch wird gelernt.',
'[{"titre":"Tableau Passiv","url":""},{"titre":"Exercices A2/B1","url":""}]',1),

('Allemand','3AS LG','2. Konjuktiv II (Souhait / politesse)',
'Konjunktiv II: wäre, hätte, würde + Infinitiv. Ex: Ich würde gern studieren. Wenn ich Zeit hätte, käme ich.',
'Pour dire "si / j''aimerais". Retiens 3 mots magiques: wäre (serait), hätte (aurait), würde (ferait). Ex: Ich hätte gern Hilfe = J''aimerais de l''aide.',
'[]',2),

('Allemand','3AS LG','3. Relativsätze (Propositions relatives)',
'Pronoms: der, die, das, den, dem, deren... Ex: Der Mann, der dort steht, ist mein Lehrer.',
'Comme "qui/que" en français mais qui change selon le genre/cas. Astuce: le verbe va à la fin. Ex: Das Buch, das ich lese...',
'[]',3),

('Allemand','3AS LG','4. Wortschatz: Umwelt und Technologie',
'Vokabeln: die Umwelt (environnement), der Klimawandel, die Energie, nachhaltig (durable), die Erfindung.',
'Mémorise 5 mots/jour avec phrase exemple. Ex: Wir schützen die Umwelt = Nous protégeons l''environnement.',
'[]',4),

('Allemand','3AS LG','5. Textproduktion: Meinung äußern (BAC)',
'Structure BAC: Einleitung (Thema vorstellen), Hauptteil (Vor- und Nachteile + Beispiele), Schluss (eigene Meinung). Connecteurs: zunächst, außerdem, jedoch, abschließend.',
'Plan en 3 parties toujours. Apprends 10 connecteurs par cœur, ça donne +3 points au BAC.',
'[]',5),

-- ===== ANGLAIS =====
('Anglais','3AS LG','1. Reported Speech',
'She said: "I am tired" → She said (that) she was tired. Backshift: present→past, will→would, can→could.',
'Discours indirect = reculer le temps d''un cran. Say + phrase simple.',
'[]',6),

('Anglais','3AS LG','2. Conditionals (0,1,2,3)',
'Type2: If + past simple, would + BV. Ex: If I had time, I would travel. Type3: If + past perfect, would have + PP.',
'0=vérité, 1=réel futur, 2=rêve présent, 3=regret passé.',
'[]',7),

-- ===== FRANÇAIS =====
('Français','3AS LG','1. Le texte argumentatif',
'Thèse, arguments, exemples, connecteurs logiques. Types: pour/contre, concessif.',
'Question BAC: repère thèse dès l''intro, 3 arguments = 3 paragraphes.',
'[]',8),

('Français','3AS LG','2. Figures de style essentielles',
'Métaphore, comparaison, anaphore, hyperbole, antithèse. Ex BAC filière langues.',
'Apprends définition + 1 exemple chacune.',
'[]',9),

-- ===== ARABE =====
('Arabe','3AS LG','1. البناء اللغوي - الإعراب',
'مراجعة النواسخ، الممنوع من الصرف، البدل والعطف.',
'ركز على إعراب الجمل BAC شعبة لغات.',
'[]',10),

-- ===== ESPAGNOL =====
('Espagnol','3AS LG','1. Subjuntivo presente',
'Formación: hablar→hable, comer→coma, vivir→viva. Uso: quiero que, es necesario que.',
'Como en francés subjonctif après "vouloir que".',
'[]',11),

-- ===== HISTOIRE-GEO =====
('Histoire-Géo','3AS LG','1. Le monde depuis 1945 - Guerre froide',
'Bipolarisation USA/URSS, coexistence pacifique, crises (Cuba, Vietnam), détente.',
'Frise: 1945-1991. Retiens 4 dates clés.',
'[]',12),

-- ===== PHILOSOPHIE =====
('Philosophie','3AS LG','1. Méthodologie dissertation BAC',
'Problématiser, thèse/antithèse/synthèse, exemples philosophiques.',
'Plan dialectique en 3 parties.',
'[]',13),

-- ===== SCIENCES ISLAMIQUES =====
('Sciences Islamiques','3AS LG','1. العقيدة والشريعة',
'أركان الإيمان، مقاصد الشريعة، الميراث.',
'احفظ الآيات والأحاديث بالشواهد.',
'[]',14);
