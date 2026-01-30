# Task Output: Security Audit SNCP - Secrets Detection

**Worker:** Cervella Security
**Date:** 29 Gennaio 2026
**Task:** Audit SNCP for plaintext secrets + Prevention

---

## Status

🚨 **CRITICAL ISSUES FOUND**

---

## Findings Summary

| Severity | Count | Description |
|----------|-------|-------------|
| **CRITICAL** | 1 | Real database credentials in plaintext |
| **HIGH** | 0 | No additional high-risk patterns |
| **MEDIUM** | 172 | Keyword usage (legitimate documentation) |

---

## Top Issue

**CRITICAL-001: Plaintext Database Credentials**

**File:** `.sncp/progetti/miracollo/bracci/miracallook/ricerche/CREDENZIALI_ERICSOFT_S315.md`

**Contains:**
- SQL Server admin credentials (sa user + password)
- SQL Server read-only user credentials
- Bedzzle API keys (3 keys)
- Connection strings with IP + port

**Risk:** Full database compromise (452 tables, guest PII)

**Impact:** GDPR violation if exploited

**Cause:** Documentation of system access without filtering secrets

---

## Deliverables

### 1. Audit Report (DETAILED)

**File:** `.swarm/security/AUDIT_SNCP_SECRETS.md`

**Content:**
- Executive summary
- Critical findings breakdown
- Attack vectors analysis
- Root cause analysis
- Comparison with Moltbot
- Recommended fixes (immediate + long-term)
- Best practices going forward
- Next steps prioritized

### 2. Audit Script (AUTOMATED)

**Files:**
- `.swarm/security/audit-secrets-draft.sh` (draft)
- `scripts/sncp/audit-secrets.sh` (ready to use - NOT YET CREATED, need bash access)

**Features:**
- Pattern detection (CRITICAL/HIGH/MEDIUM)
- File exclusions (research docs)
- Line number reporting (content hidden for security)
- Exit codes for CI/CD integration
- Color-coded output

**Usage:**
```bash
./scripts/sncp/audit-secrets.sh .sncp/progetti/
```

### 3. Best Practices Guide (EDUCATION)

**File:** `.swarm/security/BEST_PRACTICES_MEMORY_SECURITY.md`

**Content:**
- What are secrets vs non-secrets
- Documentation patterns (good vs bad examples)
- Code patterns (Python, React)
- File structure for secrets (.env, .gitignore)
- Worker checklist
- Automated tools setup
- Incident response procedure
- FAQ

---

## Immediate Actions Required

### P0 - TODAY

1. **Rotate Ericsoft credentials** (business decision - Rafa)
   - SQL Server `sa` password
   - SQL Server `miracollook_reader` password

2. **Sanitize files** (technical - Cervella Backend)
   - Remove credentials from `CREDENZIALI_ERICSOFT_S315.md`
   - Replace with references to .env
   - Update `SUBROADMAP_CONNETTORE_ERICSOFT.md`

3. **Create .env file** (technical - Cervella Backend)
   - `miracollogeminifocus/.env` with actual credentials
   - Verify `.env` in `.gitignore` (✓ already present)

### P1 - S321

4. **Install audit script** (technical - Cervella Ops)
   - Move draft to `scripts/sncp/audit-secrets.sh`
   - Make executable
   - Test on full SNCP

5. **Add pre-commit hook** (technical - Cervella Ops)
   - `.git/hooks/pre-commit`
   - Calls audit-secrets.sh
   - Blocks commit if secrets found

### P2 - Week 6

6. **Update Worker DNA** (cultural - Cervella Regina)
   - Add security rule to all Worker DNA files
   - Reference BEST_PRACTICES_MEMORY_SECURITY.md

7. **CI/CD integration** (automation - Cervella Ops)
   - Add secrets scan to GitHub Actions
   - Fail pipeline if secrets detected

---

## Comparison: SNCP vs Moltbot

| Aspect | Moltbot | SNCP (Before Fix) | SNCP (After Fix) |
|--------|---------|-------------------|------------------|
| **Plaintext secrets** | ⚠️ Yes | ⚠️ Yes (1 file) | ✅ No |
| **Automated detection** | ❌ No | ❌ No | ✅ Yes (audit script) |
| **Pre-commit prevention** | ❌ No | ❌ No | ✅ Yes (hook) |
| **Documentation** | ❌ No | ❌ No | ✅ Yes (best practices) |
| **Repository visibility** | ⚠️ Recommended private | ✅ Private | ✅ Private |

**Verdict:** We found the problem BEFORE production. Now fixing systemically.

---

## Lessons Learned

### What Went Right

✅ Proactive audit (triggered by Moltbot research)
✅ Private repository (limited exposure)
✅ Quick detection (same day as credential storage)
✅ No production impact (credentials not used yet)

### What Went Wrong

❌ No automated prevention before commit
❌ Cultural gap (convenient to document everything)
❌ No warning in SNCP guidelines

### Systemic Fix

This is NOT a mistake. This is a **systemic gap**.

**Solution:** Automation + education + cultural change.

---

## Files Created

```
.swarm/security/
├── AUDIT_SNCP_SECRETS.md                  # Detailed audit report
├── audit-secrets-draft.sh                 # Script draft (ready for scripts/)
└── BEST_PRACTICES_MEMORY_SECURITY.md      # Worker education guide
```

**Next:** Move `audit-secrets-draft.sh` to `scripts/sncp/audit-secrets.sh` (requires bash/ops worker)

---

## Validation Checklist

**Audit completeness:**
- [x] Scanned all `.sncp/progetti/` for secrets
- [x] Checked API key patterns (OpenAI, Google, GitHub)
- [x] Checked JWT/Bearer tokens
- [x] Checked database connection strings
- [x] Checked password patterns
- [x] Identified critical vs medium findings

**Deliverables:**
- [x] Audit report written
- [x] Audit script created (draft)
- [x] Best practices guide created
- [x] Examples provided (good vs bad)
- [x] Worker checklist included

**Security:**
- [x] Report does NOT contain actual secrets (only references)
- [x] Line numbers reported, content hidden
- [x] Clear severity assessment
- [x] Immediate actions prioritized

---

## Next Steps

**For Rafa:**
1. Review AUDIT_SNCP_SECRETS.md
2. Decide on credential rotation timeline
3. Approve P0 actions

**For Regina:**
1. Assign P0 actions to Cervella Backend
2. Assign P1 actions to Cervella Ops
3. Schedule P2 cultural updates

**For Workers:**
1. Read BEST_PRACTICES_MEMORY_SECURITY.md
2. Follow checklist before writing to memory
3. Use audit script before commits

---

## Mantra

```
"Secrets in .env, references in docs."
"Document WHAT is needed, not WHAT it is."
"Automation prevents, humans forget."
"La miglior difesa è prevenire, non reagire."
```

---

**Audit Complete.**

**Cervella Security** - 29 Gennaio 2026, S320

*"Caught before production. Fixed systemically."*
