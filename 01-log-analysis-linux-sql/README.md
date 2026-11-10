# Project 01 — Investigating an SSH Brute-Force Attack with Linux

**Role:** SOC Analyst (lab exercise)
**Tools:** Linux CLI — `grep`, `awk`, `sed`, `sort`, `uniq`, `cut`

>  Lab project. The log data is **simulated** for training purposes only.

## Scenario
The server `web-prod-01` showed suspicious mid-morning activity. I analyzed its
SSH authentication log (`auth.log`) to determine whether an attack occurred and
whether any account was compromised.

## Methodology & Findings

**1. Abnormal volume of failed logins**
grep -c “Failed password” auth.log -> 240
240 failed logins in a short window — far beyond normal user error.

**2. Single source IP (brute-force signature)**
All 240 failures came from **one external IP: 185.220.101.47**. A single source
hammering the server indicates an automated brute-force attack.

**3. Dictionary attack across multiple usernames**
The attacker tried **10 different usernames** (postgres, ubuntu, root, maria,
oracle...), confirming an automated username/password spraying attack.

**4. Confirmed compromise**
A **successful** login from the attacker's IP — the account **maria** was compromised.

**5. Attack timeline**
First failed attempt 10:14:04 -> compromise 10:24:21 (~10 minutes).

## Indicators of Compromise (IOCs)
| Type | Value |
|------|-------|
| Attacker IP | 185.220.101.47 |
| Compromised account | maria |
| Time of compromise | Mar 14, 10:24:21 |
| Attack type | SSH brute-force / dictionary |

## Recommendations
- Block 185.220.101.47 at the firewall.
- Reset maria's password and review its post-compromise session activity.
- Deploy **fail2ban** to auto-ban IPs after repeated failures.
- Enforce **key-based SSH authentication** and disable password login.
- Enable **MFA** for remote access.

## What I learned
How to chain Linux text-processing tools (`grep | awk | sort | uniq -c`) to turn
hundreds of raw log lines into a clear attack timeline, and how a successful login
right after a burst of failures reveals a compromise.
