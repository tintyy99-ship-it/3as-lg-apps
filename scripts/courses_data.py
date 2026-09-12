# -*- coding: utf-8 -*-
"""تجميع كل الدروس الكاملة (78) — المصدر الوحيد المعتمد.
الصيغة: (المادة، العنوان، الثلاثي، القسم، الدرس الكامل، الزبدة، الترتيب)
"""
from courses_ar1 import COURSES_DE
from courses_ar2 import COURSES_ENFR
from courses_ar3 import COURSES_AR_ES_IT
from courses_ar4 import COURSES_HG_PHILO
from courses_ar5 import COURSES_ISL_MATH

COURSES = COURSES_DE + COURSES_ENFR + COURSES_AR_ES_IT + COURSES_HG_PHILO + COURSES_ISL_MATH

MATIERES = ["الألمانية", "الإنجليزية", "الفرنسية", "العربية", "الإسبانية",
            "الإيطالية", "التاريخ", "الجغرافيا", "الفلسفة",
            "العلوم الإسلامية", "الرياضيات"]

if __name__ == "__main__":
    from collections import Counter
    print("TOTAL:", len(COURSES))
    print(dict(Counter(c[0] for c in COURSES)))
    print("trimestres:", dict(Counter(c[2] for c in COURSES)))
    bad = [c for c in COURSES if len(c[4]) < 400]
    print("dروس قصيرة (<400):", len(bad), [c[1][:30] for c in bad])
