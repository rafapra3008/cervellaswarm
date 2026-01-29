# Security Audit: SNCP Secrets Detection

**Date:** 29 Gennaio 2026
**Auditor:** Cervella Security
**Scope:** `.sncp/progetti/` - All memory files
**Trigger:** Moltbot plaintext secrets vulnerability (see `reports/RICERCA_MEMORIA_PERSISTENTE_MOLTBOT.md`)

---

## Executive Summary

**Status:** 🚨 **CRITICAL ISSUES FOUND**

**Findings:**
- **1 CRITICAL** - Real database credentials in plaintext
- **0 HIGH** - No additional high-risk patterns
- **172 MEDIUM** - Keyword usage (legitimate context)

**Top Issue:** File `CREDENZIALI_ERICSOFT_S315.md` contains real SQL Server admin password + API keys in plaintext.

**Immediate Action Required:** YES

---

## Critical Findings

### 🚨 CRITICAL-001: Plaintext Database Credentials

**File:** `.sncp/progetti/miracollo/bracci/miracallook/ricerche/CREDENZIALI_ERICSOFT_S315.md`

**Risk:** CRITICAL
**Impact:** Full database compromise if file accessed by unauthorized party
**Probability:** MEDIUM (file in private repo, but still exposed in git history)

**What was found:**
- SQL Server admin credentials (`sa` user + password)
- SQL Server read-only user credentials (`miracollook_reader` + password)
- Bedzzle API keys (PublicKey, PrivateKey, ProductKey)
- Connection strings with IP address + port

**Why this is critical:**
1. **Admin credentials** (`sa` user) = FULL control over database (452 tables)
2. **Committed to git** = Permanent in history (even if file deleted)
3. **Rotation required** = Credentials must be changed NOW
4. **Pattern match** = Exactly like Moltbot vulnerability

**Exploitation scenario:**
```
Attacker gains access to repo (git clone/leaked backup)
  → Reads CREDENZIALI_ERICSOFT_S315.md
  → Connects to NLTERMINAL01\SQLERICSOFT22 with sa credentials
  → Full database access (read, write, delete, dump)
  → Exfiltrates guest data (GDPR violation!)
```

---

### 🟡 MEDIUM FINDINGS: Keyword Usage (Legitimate)

**172 files** contain keywords like "password", "token", "secret", "API key" in legitimate contexts:

- Research documents (e.g., `RICERCA_ENCRYPTION_TOKENS_SQLITE.md` - about encryption)
- Technical documentation (explaining authentication flows)
- Architecture docs (describing what credentials SHOULD be used)

**Verdict:** NOT a security issue - documentation is using terms correctly (describing systems, not exposing actual secrets).

---

## Related Files Review

### File: `SUBROADMAP_CONNETTORE_ERICSOFT.md`

**Status:** ⚠️ CONTAINS REFERENCES TO CREDENTIALS

**Content:**
- References same Bedzzle API keys as CREDENZIALI_ERICSOFT_S315.md
- PublicKey: `[REDACTED-PUBLIC-KEY]`
- PrivateKey: `[REDACTED-PRIVATE-KEY]`
- ProductKey: `[REDACTED-PRODUCT-KEY]`

**Risk:** MEDIUM (API keys, not database credentials)

**Note:** These are third-party API keys (Bedzzle/MyReception). Less critical than database admin access, but still should NOT be in memory files.

---

## Attack Vectors

### Vector 1: Git History Exposure

```
Current situation:
  - Files committed to private repo
  - Git history contains credentials
  - Even if file deleted, history preserves it

Mitigation required:
  1. Remove credentials from files
  2. Rewrite git history (git filter-branch or BFG)
  3. Force-push cleaned history
  4. Rotate ALL exposed credentials
```

### Vector 2: Backup/Clone Leakage

```
Risk:
  - Developer laptop backup (Time Machine, Dropbox sync)
  - Accidental public push
  - Repo clone on compromised machine

Mitigation:
  - Assume credentials already compromised
  - Rotate immediately
```

### Vector 3: Malware/Infostealer

```
Moltbot learned lesson:
  - Malware (Redline, Lumma, Vidar) targets AI assistant directories
  - CervellaSwarm/.sncp/ is a known location
  - Automated scraping for credential patterns

Mitigation:
  - NO credentials in memory files (policy)
  - Automated pre-commit scanning
```

---

## Root Cause Analysis

### Why did this happen?

**Context:** Sessione 315-316 documented database exploration for Miracollook connector.

**Developer intent:** Good (documentation of system access for troubleshooting/handoff).

**Mistake:** Stored ACTUAL credentials instead of REFERENCE to credentials.

**Contributing factors:**
1. No pre-commit hook to detect secrets
2. No warning in documentation about credential storage
3. Convenient to "just document it quickly"

**Lesson:** Even with good intentions, plaintext secrets creep in without automated prevention.

---

## Comparison: SNCP vs Moltbot

| Aspect | Moltbot | SNCP (CervellaSwarm) |
|--------|---------|----------------------|
| **Credential storage** | ⚠️ Plaintext in MEMORY.md | ⚠️ Plaintext in CREDENZIALI_*.md |
| **Scope of exposure** | 🚨 User-facing (~/clawd/) | 🟡 Developer-only (.sncp/progetti/) |
| **Version control** | ⚠️ Recommended private git | ✅ Already in private git |
| **Detection** | ❌ No automated scanning | ❌ No automated scanning (yet!) |
| **Prevention** | ❌ No pre-commit hook | ❌ No pre-commit hook (yet!) |

**Verdict:** CervellaSwarm is BETTER (private repo, developer-only access) but STILL VULNERABLE to same pattern.

---

## Recommended Fix

### Immediate Actions (TODAY)

1. **Rotate credentials** (HIGH PRIORITY)
   ```sql
   -- On NLTERMINAL01\SQLERICSOFT22
   ALTER LOGIN sa WITH PASSWORD = '[NEW_COMPLEX_PASSWORD]';
   ALTER LOGIN miracollook_reader WITH PASSWORD = '[NEW_COMPLEX_PASSWORD]';
   ```

2. **Remove credentials from files**
   ```bash
   # Edit CREDENZIALI_ERICSOFT_S315.md
   # Replace actual credentials with:
   Password: [stored in .env as ERICSOFT_SA_PASSWORD]
   ```

3. **Create .env file** (NOT committed to git)
   ```bash
   # miracollogeminifocus/.env
   ERICSOFT_DB_HOST=192.168.200.5
   ERICSOFT_DB_INSTANCE=NLTERMINAL01\SQLERICSOFT22
   ERICSOFT_DB_NAME=PRA
   ERICSOFT_DB_USER=miracollook_reader
   ERICSOFT_DB_PASSWORD=[actual_password_here]

   BEDZZLE_PUBLIC_KEY=[actual_key]
   BEDZZLE_PRIVATE_KEY=[actual_key]
   BEDZZLE_PRODUCT_KEY=[actual_uuid]
   ```

4. **Update .gitignore**
   ```bash
   # Add to miracollogeminifocus/.gitignore
   .env
   .env.*
   !.env.example
   ```

5. **Clean git history** (OPTIONAL but recommended)
   ```bash
   # Use BFG Repo-Cleaner
   bfg --replace-text passwords.txt CervellaSwarm/.git
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```

---

### Long-Term Prevention (WEEK 6)

#### 1. Pre-commit Hook

**File:** `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Run secrets audit before every commit
./scripts/sncp/audit-secrets.sh .sncp/progetti/

if [ $? -ne 0 ]; then
    echo "❌ Commit blocked: Secrets detected in memory files!"
    echo "Remove credentials before committing."
    exit 1
fi
```

**Installation:**
```bash
chmod +x .git/hooks/pre-commit
```

#### 2. Audit Script (Automated)

**File:** `scripts/sncp/audit-secrets.sh`
**Status:** DRAFT created at `.swarm/security/audit-secrets-draft.sh`

**Features:**
- Regex patterns for common secret types
- Severity levels (CRITICAL/HIGH/MEDIUM)
- File exclusions (research docs, examples)
- Line number reporting (content hidden)

**Usage:**
```bash
# Manual scan
./scripts/sncp/audit-secrets.sh .sncp/progetti/

# CI/CD integration
- name: Scan for secrets
  run: ./scripts/sncp/audit-secrets.sh
```

#### 3. Documentation Update

**File:** `~/.claude/docs/BEST_PRACTICES_SECURITY.md` (NEW)

**Content:**
```markdown
# Security Best Practices - Memory Files

## NEVER Store in Memory Files

❌ API keys
❌ Passwords
❌ Database connection strings with credentials
❌ Private keys
❌ Tokens (OAuth, JWT, etc)
❌ Secret environment variables

## ALWAYS Store Instead

✅ Reference to where secret is stored
   Example: "Password stored in .env as DB_PASSWORD"

✅ System architecture (WITHOUT credentials)
   Example: "Connects to server X with user Y (credentials in .env)"

✅ What credentials are NEEDED (not the actual values)
   Example: "Requires: SQL Server login with SELECT permissions"
```

#### 4. Worker Education

**Add to all Worker DNA files:**

```markdown
## SECURITY RULE: NO SECRETS IN MEMORY

When documenting systems:
- NEVER write actual passwords/keys/tokens
- ALWAYS reference .env or credential store
- Example: "API_KEY: [stored in .env]"
```

---

## Best Practices Going Forward

### Documentation Pattern

**❌ WRONG:**
```markdown
## Database Connection

Server: 192.168.200.5
User: sa
Password: [REDACTED-PASSWORD]
```

**✅ CORRECT:**
```markdown
## Database Connection

Server: [stored in .env as DB_HOST]
User: [stored in .env as DB_USER]
Password: [stored in .env as DB_PASSWORD]

Connection string: Available in miracollogeminifocus/.env
```

### Code Pattern

**❌ WRONG:**
```python
connection = pymssql.connect(
    server="192.168.200.5",
    user="sa",
    password="[REDACTED-PASSWORD]",
    database="PRA"
)
```

**✅ CORRECT:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

connection = pymssql.connect(
    server=os.getenv("ERICSOFT_DB_HOST"),
    user=os.getenv("ERICSOFT_DB_USER"),
    password=os.getenv("ERICSOFT_DB_PASSWORD"),
    database=os.getenv("ERICSOFT_DB_NAME")
)
```

---

## Testing Validation

### Test 1: Script Detection

```bash
# Create test file with fake credentials
echo "password: test123" > /tmp/test.md

# Run audit script
./scripts/sncp/audit-secrets.sh /tmp/

# Expected: HIGH finding detected
```

### Test 2: Pre-commit Hook

```bash
# Stage file with credentials
git add .sncp/test_with_secret.md

# Try to commit
git commit -m "test"

# Expected: Commit BLOCKED
```

### Test 3: False Positive Check

```bash
# Research doc about encryption (legitimate keyword usage)
cat .sncp/progetti/miracollo/RICERCA_ENCRYPTION_TOKENS_SQLITE.md

# Run audit
./scripts/sncp/audit-secrets.sh

# Expected: File excluded from scan (in EXCLUDE_FILES list)
```

---

## Severity Assessment

### CRITICAL-001 Breakdown

| Metric | Score | Reasoning |
|--------|-------|-----------|
| **Exploitability** | HIGH | Credentials in plaintext, easy to find |
| **Impact** | CRITICAL | Full database access (sa user) |
| **Affected Systems** | 1 | Ericsoft PRA database (452 tables) |
| **Data at Risk** | Guest PII | Names, emails, bookings, payments |
| **GDPR Impact** | HIGH | Breach notification required if exploited |
| **Business Impact** | HIGH | Reputational damage, legal liability |

**CVSS Score (estimated):** 8.1/10 (High)

---

## Timeline

| Date | Event |
|------|-------|
| 2026-01-29 S315 | Credentials documented in CREDENZIALI_ERICSOFT_S315.md |
| 2026-01-29 S315 | File committed to git (private repo) |
| 2026-01-29 S320 | Security audit discovers plaintext credentials |
| 2026-01-29 S320 | Escalation to Regina (this report) |
| **TBD** | Credentials rotated |
| **TBD** | Files sanitized |
| **TBD** | Pre-commit hook installed |

---

## Lessons Learned

### What Went Right

✅ Private repository (not public)
✅ Limited access (only Rafa + Cervelle)
✅ Quick detection (audit triggered by Moltbot research)
✅ No evidence of exploitation (credentials not used in production yet)

### What Went Wrong

❌ No automated detection before commit
❌ Documentation culture allowed plaintext credentials
❌ No warning in SNCP guidelines about secrets
❌ Convenient to "document everything" without filtering

### Systemic Fix Required

This is NOT a one-time mistake. This is a **systemic gap** in our process.

**Fix:** Automated prevention (pre-commit hook) + cultural change (documentation patterns).

---

## Related Documentation

| Document | Relevance |
|----------|-----------|
| `reports/RICERCA_MEMORIA_PERSISTENTE_MOLTBOT.md` | Trigger for this audit |
| `.sncp/progetti/miracollo/bracci/miracallook/SUBROADMAP_CONNETTORE_ERICSOFT.md` | Context for credential usage |
| `.sncp/progetti/miracollo/RICERCA_ENCRYPTION_TOKENS_SQLITE.md` | Research on encryption (legitimate keyword usage) |

---

## Next Steps (Prioritized)

| Priority | Task | Owner | ETA |
|----------|------|-------|-----|
| 🚨 P0 | Rotate Ericsoft credentials | Rafa (business) | TODAY |
| 🚨 P0 | Remove credentials from files | Cervella Backend | TODAY |
| 🔴 P1 | Install audit script to `scripts/sncp/` | Cervella Security | S321 |
| 🔴 P1 | Add pre-commit hook | Cervella Ops | S321 |
| 🟡 P2 | Create BEST_PRACTICES_SECURITY.md | Cervella Security | Week 6 |
| 🟡 P2 | Update Worker DNA files | Cervella Regina | Week 6 |
| 🟢 P3 | Git history cleanup (optional) | Cervella Ops | Future |

---

## Conclusion

**We caught this BEFORE production.**
**No evidence of exploitation.**
**Fix is straightforward.**

But this reveals a **systemic gap**: We need automated prevention, not just reactive detection.

**Mantra:**
*"Secrets in .env, references in docs."*
*"Automate prevention, assume human error."*
*"Defense in depth - no single point of trust."*

---

**Cervella Security**
*"La miglior difesa è prevenire, non reagire."*

29 Gennaio 2026 - S320
