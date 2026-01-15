# SECURITY AUDIT - CI/CD Pipeline Proposal

**Data:** 15 Gennaio 2026
**Auditor:** Cervella Security
**Progetto:** CervellaSwarm CLI v0.1.0
**Target:** Proposta CI/CD con Trusted Publishing (OIDC)
**Severità:** MEDIUM (pre-production audit, no critical issues)

---

## EXECUTIVE SUMMARY

**Status:** ✅ APPROVED con raccomandazioni

**Verdetto:**
- Trusted Publishing è sicuro e raccomandato per 2026
- Proposta workflow è solida
- 7 raccomandazioni di hardening identificate
- Nessun blocco critico trovato

**Prossimo step:** Implementare con checklist sicurezza OBBLIGATORIA inclusa

---

## AUDIT PUNTO PER PUNTO

### 1. Trusted Publishing (OIDC) - È sicuro?

**✅ VERDICT: SI - Più sicuro di NPM_TOKEN**

**Vantaggi confermati:**
- Token ephemeral (< 1 ora, auto-expires)
- Zero rischio token leak (no secrets da gestire)
- Provenance automatica (supply chain transparency)
- Token valido SOLO per workflow specifico
- Delegazione autenticazione a GitHub (trust chain verificabile)

**Rischi identificati:**

| Rischio | Severità | Mitigazione |
|---------|----------|-------------|
| **1.1 Configuration Error** | MEDIUM | ⚠️ Radio button "Require OIDC" facile da perdere |
| **1.2 Downgrade Attack** | LOW | ⚠️ Maintainer compromesso può disabilitare OIDC |
| **1.3 Malware in node_modules** | MEDIUM | ⚠️ Post-publish malware può fare commit+tag |

**RACCOMANDAZIONI MITIGAZIONI:**

```
1.1 REQUIRE OIDC:
    - Setup npm.com: Trusted Publisher → "Require OIDC and disable tokens"
    - VERIFICARE radio button attivo!
    - Screenshot del setting per documentazione

1.2 DOWNGRADE PROTECTION:
    - Branch protection su main (required reviews)
    - CODEOWNERS file per workflow changes
    - Alert se settings npm cambiano (manual check mensile)

1.3 NODE_MODULES SECURITY:
    - npm audit PRIMA di ogni publish
    - lock file integrity (npm ci, not npm install)
    - Audit supply chain (Socket.dev raccomandato)
```

**Fonti:**
- [npm Trusted Publishing Docs](https://docs.npmjs.com/trusted-publishers/)
- [Socket.dev npm Trusted Publishing](https://socket.dev/blog/npm-trusted-publishing)
- [Speakeasy npm Security](https://www.speakeasy.com/blog/npm-trusted-publishing-security)

---

### 2. Permissions Workflow - `id-token: write` sicuro?

**✅ VERDICT: SI - Configurazione corretta**

**Analisi proposta:**
```yaml
permissions:
  id-token: write  # OIDC authentication
  contents: read   # Read-only repo access
```

**Validazione:**
- ✅ Principle of Least Privilege rispettato
- ✅ `id-token: write` usato SOLO per OIDC (uso legittimo)
- ✅ `contents: read` (no write su repo)
- ✅ No GITHUB_TOKEN abuse possibile
- ✅ Explicit permission declaration (good practice)

**RACCOMANDAZIONE IMPROVEMENT:**

```yaml
# PROPOSTA HARDENED (da implementare)
permissions:
  id-token: write      # Required for OIDC
  contents: read       # Read repo
  packages: none       # Explicit deny
  actions: none        # Explicit deny
  security-events: none # Explicit deny
```

**Rationale:** Explicit deny di permission non necessari (defense in depth).

**Fonti:**
- [GitHub Actions Secure Use](https://docs.github.com/en/actions/reference/security/secure-use)
- [StepSecurity GITHUB_TOKEN Best Practices](https://www.stepsecurity.io/blog/github-token-how-it-works-and-how-to-secure-automatic-github-action-tokens)

---

### 3. Branch Protection - Quali regole servono?

**⚠️ VERDICT: MANDATORY - Setup richiesto**

**Regole OBBLIGATORIE per main:**

| Rule | Setting | Rationale |
|------|---------|-----------|
| **Require PR** | ✅ Enabled | No direct push su main |
| **Require review** | 1 approver | Rafa DEVE approvare |
| **Dismiss stale reviews** | ✅ Enabled | Force re-review dopo push |
| **Require status checks** | CI workflow | Publish solo se CI verde |
| **Require up-to-date** | ✅ Enabled | No merge stale branch |
| **Require signed commits** | ⚠️ Optional | Nice-to-have (vedi sotto) |
| **Include administrators** | ✅ Enabled | Regole per tutti (no bypass) |
| **Restrict who can push** | Main only | Solo bot + Rafa |

**CODEOWNERS raccomandato:**
```
# .github/CODEOWNERS
.github/workflows/* @rafapra
packages/cli/package.json @rafapra
```

**Protezione workflow changes:**
- ⚠️ Workflow changes = security-critical
- ✅ Require approval per `.github/workflows/*.yml`
- ✅ CODEOWNERS enforcement

**Setup command:**
```
GitHub repo → Settings → Branches → Branch protection rules
→ Add rule: main
→ Apply settings sopra
```

---

### 4. Tag Signing - Serve GPG?

**✅ VERDICT: Optional per MVP, raccomandato per v1.0.0**

**Pro GPG signing:**
- ✅ Proof of authorship (non-repudiation)
- ✅ Tag integrity (no tampering)
- ✅ Industry best practice

**Contro GPG signing:**
- ⚠️ Setup overhead (GPG keys, CI secrets)
- ⚠️ Key rotation management
- ⚠️ Not strictly required per OIDC

**RACCOMANDAZIONE:**

```
FASE MVP (v0.x.x):
- Tag unsigned OK (Trusted Publishing già fornisce provenance)
- Focus su process, non overhead

FASE PRODUCTION (v1.0.0+):
- Setup GPG signing (Rafa keys)
- Workflow: git tag -s v1.0.0 -m "Release 1.0.0"
- Verify: git tag -v v1.0.0

RATIONALE:
- Trusted Publishing fornisce publish authenticity
- GPG fornisce tag authenticity
- Layered security (defense in depth)
```

**Alternative a GPG:**
- GitHub commit signature verification (built-in)
- Cosign (Sigstore) per container/artifact signing

---

### 5. Supply Chain - Flag `--provenance` sufficiente?

**✅ VERDICT: SI - Buona baseline, audit periodico necessario**

**Provenance fornisce:**
- ✅ Build metadata (repo, commit SHA, workflow)
- ✅ SLSA Level 3 compliance potential
- ✅ Verifiable publish origin
- ✅ npm displays provenance badge

**GAPS identificati:**

| Gap | Rischio | Mitigazione |
|-----|---------|-------------|
| **Dependencies audit** | HIGH | npm audit in CI + pre-publish |
| **SBOM generation** | MEDIUM | Considerare CycloneDX SBOM |
| **Vulnerability scanning** | MEDIUM | Socket.dev o Snyk integration |
| **License compliance** | LOW | license-checker npm package |

**RACCOMANDAZIONE SUPPLY CHAIN SECURITY:**

```yaml
# Aggiungere a CI workflow (prima di test)
- name: Security Audit
  run: |
    npm audit --audit-level=high
    # Fail se vulnerabilità HIGH o CRITICAL
    if [ $? -ne 0 ]; then
      echo "❌ Security vulnerabilities found!"
      exit 1
    fi

- name: License Check
  run: npx license-checker --summary

# Aggiungere a publish workflow (prima di npm publish)
- name: Final Security Scan
  run: |
    npm audit --production --audit-level=critical
    npm outdated --long
```

**Tools raccomandati (post-MVP):**
- Socket.dev (free tier) - dependency analysis
- Snyk (free open source) - vulnerability database
- OSSF Scorecard - repo security posture

**Provenance verification (users):**
```bash
npm view cervellaswarm --json | jq .provenance
```

---

### 6. Secrets - Quali servono con OIDC?

**✅ VERDICT: ZERO secrets necessari per publish!**

**Con Trusted Publishing (OIDC):**
- ✅ No NPM_TOKEN secret
- ✅ No API keys
- ✅ GITHUB_TOKEN automatico (built-in)

**Secrets ATTUALI nel repo:**
```bash
# Check esistenti
gh secret list
```

**RACCOMANDAZIONE SECRETS HYGIENE:**

```
VERIFY:
[ ] Zero NPM_TOKEN in GitHub Secrets
[ ] Zero NPM_TOKEN in Environment Secrets
[ ] GITHUB_TOKEN mai hardcoded (sempre ${{ secrets.GITHUB_TOKEN }})

FUTURE SECRETS (se necessari):
- Store in Environment secrets (not repo secrets)
- Use environment protection (reviewer required)
- Rotation policy (90 giorni max)
- Never log secrets (add to .gitignore)

AUDIT TRAIL:
- GitHub Audit Log monitora secret access
- Review mensile: Settings → Security → Audit log
```

**Se Trusted Publishing fallisce:**
- Fallback: NPM_TOKEN (granular, 90 giorni max)
- Store in: Settings → Environments → production → Secrets
- Rotation reminder: Calendar every 60 giorni

---

### 7. Environment Protection - Serve "production"?

**✅ VERDICT: SI - OBBLIGATORIO per fase MVP**

**Perché serve environment protection:**
- ✅ Manual approval gate (Rafa DEVE approvare publish)
- ✅ Audit trail (chi ha approvato quando)
- ✅ Secret isolation (se servono in futuro)
- ✅ Deployment history tracking
- ✅ Rollback point-of-reference

**Setup OBBLIGATORIO:**

```yaml
# In publish.yml workflow
jobs:
  publish:
    environment:
      name: production
      url: https://www.npmjs.com/package/cervellaswarm
    permissions:
      id-token: write
      contents: read
    # ... rest of job
```

**GitHub Settings:**
```
1. Settings → Environments → New environment: "production"

2. Deployment protection rules:
   ✅ Required reviewers: rafapra
   ⚠️ Wait timer: 0 minutes (no delay, solo approval)
   ✅ Deployment branches: Protected branches only

3. Environment secrets (se necessari):
   - Solo reviewer possono vedere
   - Separate da repo secrets

4. Save environment
```

**Workflow con environment:**
- Push tag → Workflow starts → Paused (waiting approval)
- Rafa riceve notifica GitHub
- Rafa review: Checks → Review deployments → Approve
- Workflow continua → npm publish

**Benefit aggiuntivo:**
- Deployment history: Environment → Deployments (audit trail)
- Rollback info: Quale tag, quando, chi ha approvato

---

## CHECKLIST SICUREZZA OBBLIGATORIA

Prima del **PRIMO PUBLISH** su npm (v0.1.0):

### Setup npm.com
- [ ] Account npm creato
- [ ] 2FA attivo (Authenticator app o hardware key)
- [ ] Trusted Publisher configurato:
  - Owner: cervellaswarm (o org GitHub corretta)
  - Repo: cli (o repo name corretto)
  - Workflow: .github/workflows/publish.yml
- [ ] **"Require OIDC and disable tokens"** ATTIVO (screenshot!)
- [ ] Package name "cervellaswarm" disponibile (npm search)

### Setup GitHub Repository
- [ ] Branch protection su main configurata (vedi sezione 3)
- [ ] CODEOWNERS file creato (workflow protection)
- [ ] Environment "production" creato
- [ ] Rafa aggiunto come required reviewer
- [ ] CI workflow funziona e passa (badge verde)

### Code Security
- [ ] npm audit passa (zero HIGH/CRITICAL)
- [ ] ESLint configurato e passa
- [ ] prepublishOnly hook funziona
- [ ] files[] field limita publish (no test/, no .env)
- [ ] .gitignore corretto (no secrets, no node_modules)
- [ ] License file presente (Apache-2.0)

### Workflow Security
- [ ] Permissions explicit (id-token: write, contents: read)
- [ ] Tag trigger pattern corretto (v[0-9]+.[0-9]+.[0-9]+)
- [ ] npm publish con --provenance flag
- [ ] npm publish con --access public flag
- [ ] Timeout configurato (10 min max)
- [ ] Working directory corretto (packages/cli)

### Documentation
- [ ] README.md completo (badges, install, usage)
- [ ] SECURITY.md con disclosure policy
- [ ] CONTRIBUTING.md con release process
- [ ] package.json fields completi (author, repository, bugs, homepage)
- [ ] .env.example incluso in files[]

### Verification
- [ ] npm pack locale funziona
- [ ] Package installabile: npm install -g ./cervellaswarm-*.tgz
- [ ] CLI funziona: cervellaswarm --version && cervellaswarm --help
- [ ] CI passa su main (ultimo commit verde)
- [ ] Test 134/134 passano

---

## RISCHI RESIDUI

Dopo implementazione con tutte le raccomandazioni, rimangono:

| Rischio | Probabilità | Impatto | Mitigazione Residua |
|---------|-------------|---------|---------------------|
| **Maintainer account compromise** | LOW | HIGH | 2FA obbligatorio, monitoraggio accessi |
| **Malware in dependencies** | MEDIUM | MEDIUM | npm audit, review mensile dipendenze |
| **Supply chain attack (post-publish)** | LOW | HIGH | Provenance + monitoring npm activity |
| **Misconfiguration OIDC** | MEDIUM | HIGH | Checklist pre-publish, screenshot settings |
| **Tag tampering (no GPG)** | LOW | MEDIUM | Trusted Publishing mitiga, GPG v1.0.0+ |

**Acceptance:** Tutti i rischi sono LOW-MEDIUM, mitigabili con process.

**Action plan ONGOING:**
- Audit mensile: npm audit + dipendenze
- Review trimestrale: GitHub security alerts
- Update annuale: Node versions, dependencies major bump

---

## RACCOMANDAZIONI FINALI

### IMMEDIATE (Pre-publish v0.1.0)

1. **Setup Branch Protection** (Priority: CRITICAL)
   - Configure rules su main (sezione 3)
   - Add CODEOWNERS file
   - Test: Tentare push diretto (deve fallire)

2. **Setup Environment Protection** (Priority: HIGH)
   - Create "production" environment
   - Add Rafa as reviewer
   - Test: Workflow pauses per approval

3. **Setup npm Trusted Publishing** (Priority: CRITICAL)
   - Configure su npmjs.com
   - **Verificare "Require OIDC" attivo!**
   - Screenshot per documentation

4. **Add Security Audit to CI** (Priority: MEDIUM)
   - npm audit step in workflow
   - Fail on HIGH/CRITICAL vulnerabilities

### SHORT-TERM (Post v0.1.0, pre v1.0.0)

5. **SECURITY.md** (Priority: MEDIUM)
   - Vulnerability disclosure policy
   - Security contact: security@cervellaswarm.dev (?)
   - Security advisories monitoring

6. **Supply Chain Tools** (Priority: LOW)
   - Evaluate Socket.dev free tier
   - Consider OSSF Scorecard badge
   - SBOM generation (optional)

### LONG-TERM (v1.0.0+)

7. **GPG Tag Signing** (Priority: LOW)
   - Setup GPG keys (Rafa)
   - Workflow: signed tags only
   - Documentation: Verify signatures

8. **Advanced Monitoring** (Priority: LOW)
   - npm package downloads tracking
   - Security advisories automation
   - Dependency update automation (Dependabot)

---

## CONCLUSIONE

**AUDIT STATUS:** ✅ PASS

La proposta CI/CD con Trusted Publishing è **sicura e pronta per implementazione**.

**Key takeaways:**
- Trusted Publishing (OIDC) è il metodo raccomandato 2026
- Zero secrets necessari
- Branch + Environment protection OBBLIGATORI
- Checklist pre-publish deve essere seguita 100%
- Rischi residui sono accettabili con process corretto

**Security posture:** STRONG per fase MVP

**Green light:** SI - Procedere con implementazione

---

**POST-FLIGHT - COSTITUZIONE CHECK**

**COSTITUZIONE-APPLIED:** SI

**Principio usato:** "PROTEGGERE il progetto e Rafa" (Partner strategico)

**Come applicato:**
- Analisi COMPLETA (non solo "SI, va bene")
- Identificati 7 punti di hardening (non solo conferma proposta)
- Checklist OBBLIGATORIA (no scorciatoie)
- Rischi residui COMUNICATI (transparency)
- Raccomandazioni prioritizzate (fatto BENE > fatto VELOCE)

**Altro principio:**
- "I dettagli fanno SEMPRE la differenza" - 7 gap identificati con fix
- "Fatto BENE > Fatto VELOCE" - Audit approfondito, non superficiale

---

**AUDIT COMPLETATO** ✅

*Cervella Security - 15 Gennaio 2026*

*"La sicurezza non è un optional. La miglior difesa è prevenire, non reagire."*

---

## FONTI CONSULTATE

### npm Trusted Publishing
1. [npm Trusted Publishing Docs](https://docs.npmjs.com/trusted-publishers/)
2. [Socket.dev - npm Adopts OIDC](https://socket.dev/blog/npm-trusted-publishing)
3. [Speakeasy - npm Trusted Publishing Security](https://www.speakeasy.com/blog/npm-trusted-publishing-security)
4. [DEV Community - OIDC Troubleshooting Journey](https://dev.to/zhangjintao/from-deprecated-npm-classic-tokens-to-oidc-trusted-publishing-a-cicd-troubleshooting-journey-4h8b)

### GitHub Actions Security
5. [GitHub Docs - Secure Use](https://docs.github.com/en/actions/reference/security/secure-use)
6. [StepSecurity - GITHUB_TOKEN Best Practices](https://www.stepsecurity.io/blog/github-token-how-it-works-and-how-to-secure-automatic-github-action-tokens)
7. [StatusNeo - Securing GitHub Actions Workflows](https://statusneo.com/best-practices-for-securing-github-actions-workflows/)

### Supply Chain Security
8. [OWASP - NPM Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html)
9. [GitHub - npm Security Best Practices](https://github.com/lirantal/npm-security-best-practices)
10. [GitHub Community - npm Supply Chain Security](https://github.com/orgs/community/discussions/174507)
