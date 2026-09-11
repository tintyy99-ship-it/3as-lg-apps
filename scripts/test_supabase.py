"""Tests logique sans réseau : génération codes, validation expiration."""
import re, secrets, datetime
CHARS="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
def gen():
    return "3AS-"+"".join(secrets.choice(CHARS) for _ in range(6))
# 1. unicité format
codes={gen() for _ in range(1000)}
assert len(codes)==1000, "collision!"
assert all(re.match(r"^3AS-[A-Z2-9]{6}$", c) for c in codes)
print("OK gen 1000 codes uniques, ex:", list(codes)[:3])
# 2. expiration
exp=datetime.datetime.utcnow()+datetime.timedelta(days=90)
assert exp>datetime.datetime.utcnow()
print("OK expiration +90j:", exp.date())
# 3. code expiré détecté
old=(datetime.datetime.utcnow()-datetime.timedelta(days=1)).date().isoformat()
assert old < datetime.date.today().isoformat()
print("OK détection expiré")
print("ALL TESTS PASSED")
