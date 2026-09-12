# -*- coding: utf-8 -*-
"""تجميع كل الدروس الكاملة (78) — المصدر الوحيد المعتمد.
الصيغة: (المادة، العنوان، الثلاثي، القسم، الدرس الكامل، الزبدة، الترتيب)
"""
from courses_ar1 import COURSES_DE
from courses_ar2 import COURSES_ENFR
from courses_ar3 import COURSES_AR_ES_IT
from courses_ar4 import COURSES_HG_PHILO
from courses_ar5 import COURSES_ISL_MATH
from courses_ar6 import COURSES_TOP

COURSES = COURSES_DE + COURSES_ENFR + COURSES_AR_ES_IT + COURSES_HG_PHILO + COURSES_ISL_MATH + COURSES_TOP

MATIERES = ["الألمانية", "الإنجليزية", "الفرنسية", "العربية", "الإسبانية",
            "الإيطالية", "الأمازيغية", "التاريخ", "الجغرافيا", "الفلسفة",
            "العلوم الإسلامية", "الرياضيات"]
# المعاملات الرسمية الجديدة (القرار الوزاري جويلية 2026) — الفلسفة والرياضيات خارج برنامج اللغات
COEFS = {"الألمانية": 6, "الإسبانية": 6, "الإيطالية": 6, "الإنجليزية": 4,
         "الفرنسية": 4, "العربية": 2, "التاريخ": 2, "الجغرافيا": 2,
         "العلوم الإسلامية": 2, "الأمازيغية": 2, "الفلسفة": 0, "الرياضيات": 0}

if __name__ == "__main__":
    from collections import Counter
    print("TOTAL:", len(COURSES))
    print(dict(Counter(c[0] for c in COURSES)))
    print("trimestres:", dict(Counter(c[2] for c in COURSES)))
    bad = [c for c in COURSES if len(c[4]) < 400]
    print("dروس قصيرة (<400):", len(bad), [c[1][:30] for c in bad])
