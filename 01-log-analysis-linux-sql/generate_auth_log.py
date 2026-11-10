#!/usr/bin/env python3
"""Generates a SIMULATED Linux SSH auth.log for a lab exercise (fake data)."""
import random
from datetime import datetime, timedelta

random.seed(42)
HOST, start = "web-prod-01", datetime(2025, 3, 14, 8, 0, 0)

legit = {"sebastian": "10.0.0.15", "maria": "10.0.0.22", "admin": "10.0.0.5"}
ATTACKER_IP = "185.220.101.47"
attack_users = ["root","admin","test","oracle","postgres","user","ubuntu","git","maria","sebastian"]

lines = []
tfmt = lambda dt: dt.strftime("%b %d %H:%M:%S")
pid  = lambda: random.randint(1000, 9999)

t = start
for _ in range(12):
    u = random.choice(list(legit)); ip = legit[u]
    t += timedelta(minutes=random.randint(3, 25))
    lines.append((t, f"{tfmt(t)} {HOST} sshd[{pid()}]: Accepted password for {u} from {ip} port {random.randint(40000,60000)} ssh2"))

t = start + timedelta(hours=2, minutes=14)
for _ in range(240):
    u = random.choice(attack_users)
    t += timedelta(seconds=random.randint(1, 4))
    inv = "invalid user " if u in ("test","oracle","postgres","user","ubuntu","git") else ""
    lines.append((t, f"{tfmt(t)} {HOST} sshd[{pid()}]: Failed password for {inv}{u} from {ATTACKER_IP} port {random.randint(40000,60000)} ssh2"))

t += timedelta(seconds=3)
lines.append((t, f"{tfmt(t)} {HOST} sshd[{pid()}]: Accepted password for maria from {ATTACKER_IP} port {random.randint(40000,60000)} ssh2"))

for _ in range(6):
    u = random.choice(list(legit)); ip = legit[u]
    t += timedelta(minutes=random.randint(5, 30))
    lines.append((t, f"{tfmt(t)} {HOST} sshd[{pid()}]: Accepted password for {u} from {ip} port {random.randint(40000,60000)} ssh2"))

lines.sort(key=lambda x: x[0])
with open("auth.log", "w") as f:
    for _, line in lines:
        f.write(line + "\n")
print(f"Wrote auth.log with {len(lines)} lines")
