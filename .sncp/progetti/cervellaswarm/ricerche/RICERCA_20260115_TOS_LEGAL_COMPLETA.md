# RICERCA COMPLETA: Terms of Service, Privacy Policy e Legal Requirements per CervellaSwarm CLI

> **Data:** 15 Gennaio 2026
> **Ricercatrice:** cervella-researcher
> **Scope:** Legal compliance completo per CLI tool con AI
> **Status:** COMPLETATA

---

## EXECUTIVE SUMMARY

**RACCOMANDAZIONE STRATEGICA (TL;DR):**

```
APPROCCIO CONSIGLIATO: "Legal-Ready MVP" - Compliance ESSENZIALE ora, Pro features dopo

FASE 1 - MVP (PRIMA DEL LAUNCH):
✅ ToS base con anti-reverse engineering
✅ Privacy Policy GDPR-compliant minima
✅ Telemetry OPT-IN (OBBLIGATORIO GDPR!)
✅ Disclaimer AI liability chiaro
✅ P.IVA Italia (forfettario se < €65k)

FASE 2 - Pro Tier (dopo traction):
⏸ DPA completo per enterprise
⏸ Insurance professional liability
⏸ Legal audit con avvocato
⏸ Cookie policy (se web dashboard)

PERCHÉ: Bilanciare velocità vs compliance reale
TEMPO: 5-7 giorni per FASE 1 (usando templates + personalizzazione)
COSTI: €0-€300 per FASE 1, €2k-€5k per FASE 2
```

**DECISIONI CHIARE:**

| Aspetto | MVP Launch | Pro Tier | Rationale |
|---------|-----------|----------|-----------|
| **ToS Base** | ✅ ORA | Revisione | Obbligatorio sempre |
| **Privacy Policy GDPR** | ✅ ORA | Espanso | Obbligo Italia/EU |
| **Telemetry Opt-In** | ✅ ORA | Enhanced | GDPR non negoziabile |
| **AI Disclaimer** | ✅ ORA | Enhanced | Italia Law Oct 2025 |
| **P.IVA/Business** | ✅ ORA | Upgrade | Necessario per vendere |
| **DPA Enterprise** | ❌ DOPO | ✅ ORA | Solo se Pro B2B |
| **Professional Insurance** | ❌ DOPO | ✅ ORA | Non urgente MVP |
| **Legal Audit** | ❌ DOPO | ✅ ORA | Dopo primi €10k revenue |

---

## 1. TERMS OF SERVICE PER CLI TOOL

### 1.1 Cosa Deve Contenere (Analisi Cursor + Best Practices)

**CLAUSOLE ESSENZIALI (ordine standard):**

1. **Service Description**
   - Cosa offre CervellaSwarm (AI orchestration CLI)
   - Differenza tra Free e Pro tier
   - Limiti tecnici (rate limiting, API quotas)

2. **Acceptable Use Policy**
   - Divieto di reverse engineering
   - Divieto di uso per attività illegali
   - Divieto di abuso risorse (DDoS, scraping massiccio)
   - Divieto di sviluppare competitor usando il servizio

3. **Intellectual Property**
   - Copyright CervellaSwarm (codice + documentazione)
   - Licenza open source (Apache 2.0) vs componenti proprietari
   - User content ownership (loro input/output rimane loro)

4. **Account & Payments**
   - Creazione account (email, autenticazione)
   - Billing per Pro tier (mensile/annuale)
   - Metodi di pagamento (Stripe)
   - Fatturazione Italia/EU

5. **Limitation of Liability**
   - "AS IS" disclaimer
   - Liability cap (esempio: 6 mesi di fees pagati o $100)
   - No consequential damages
   - AI output disclaimer specifico

6. **Warranty Disclaimer**
   - No uptime guarantee (best effort)
   - AI output può contenere errori
   - User responsabile per validare output

7. **Termination**
   - Diritto di terminare per violazioni
   - Account inattivi > 1 anno
   - Procedura cancellazione dati
   - Refund policy su termination

8. **Dispute Resolution**
   - Foro competente (Italia - Milano/Firenze)
   - Legge applicabile (italiana)
   - Arbitrato opzionale
   - EU Consumer Rights preserved

9. **Changes to Terms**
   - Diritto di modificare ToS
   - Notifica 30 giorni prima
   - Continued use = acceptance

10. **Miscellaneous**
    - Severability clause
    - No waiver clause
    - Entire agreement
    - Contact information

### 1.2 Clausole Specifiche per CLI Tool

**DIFFERENZA CLI vs WEB APP:**

```
CLI Tool = SOFTWARE INSTALLATO LOCALMENTE
Web App = SOFTWARE FORNITO COME SERVIZIO

Implicazioni legali:
1. Licenza software (non solo service agreement)
2. Diritto recesso Italia 14gg limitato*
3. Reverse engineering: clausola più forte
4. No cookie consent (CLI non usa cookies)
5. Telemetry opt-in ESPLICITO (GDPR!)

*Limitato = Si perde se utente inizia utilizzo con consenso esplicito
```

**CLAUSOLA ANTI-REVERSE ENGINEERING (da Cursor):**

```
"Users may not reverse engineer, disassemble, decompile, decode,
or otherwise attempt to derive or gain access to the source code."

PER CERVELLASWARM:
"You may not reverse engineer, decompile, disassemble, or attempt
to discover the source code of the CervellaSwarm orchestration logic,
agent coordination algorithms, or proprietary components, except as
permitted by applicable law. Open source components remain subject
to their respective licenses."
```

### 1.3 Template ToS per CervellaSwarm (Struttura Base)

```markdown
# Terms of Service - CervellaSwarm

**Effective Date:** [Data Launch]
**Last Updated:** [Data]

These Terms of Service ("Terms") govern your use of CervellaSwarm
("Service"), an AI-powered development orchestration CLI tool
provided by [Nome Legale Società] ("we," "us," "our").

## 1. SERVICE DESCRIPTION

CervellaSwarm is a command-line interface (CLI) tool that provides:
- AI-powered development orchestration
- 16 specialized AI agents for coding tasks
- Local and cloud-based workflow management

Free tier includes [specifiche].
Pro tier includes [specifiche].

## 2. ACCEPTABLE USE

You agree NOT to:
- Use the Service for illegal activities
- Reverse engineer, decompile, or disassemble the software
- Develop competing products using the Service
- Abuse API limits or infrastructure resources
- Share your account credentials
- Circumvent usage limitations or security measures

## 3. AI GENERATED CONTENT

**IMPORTANT DISCLAIMER:**
- AI-generated code may contain errors or security vulnerabilities
- You are solely responsible for reviewing, testing, and validating output
- We do not guarantee accuracy, completeness, or fitness for purpose
- Output may inadvertently reference copyrighted material
- You retain ownership of your inputs and outputs

As per Italian Law No. 132/2025 (effective October 10, 2025),
AI-assisted works require significant human intellectual contribution
for copyright protection.

## 4. INTELLECTUAL PROPERTY

### Our IP
CervellaSwarm's orchestration logic, agent coordination, and proprietary
components are protected by copyright and trade secret law.

### Open Source Components
Certain components are licensed under Apache 2.0. See LICENSE file.

### Your Content
You retain all rights to your inputs and outputs. We do not claim
ownership of content you create using the Service.

## 5. ACCOUNTS & PAYMENTS

### Account Creation
- Valid email address required
- You are responsible for account security
- One account per user (no account sharing)

### Pro Tier Billing
- Monthly or annual subscription
- Charged via Stripe
- Prices in EUR (Italy/EU) or USD (rest of world)
- Automatic renewal unless cancelled

### Italian VAT
- B2C transactions: 22% IVA included
- B2B EU: reverse charge (VAT ID required)
- B2B non-EU: no VAT

## 6. REFUND POLICY

### Free Tier
No refunds (free service).

### Pro Tier
- **EU Consumers (Italy):** 14-day right of withdrawal BEFORE first use
- Once you begin using Pro features, right of withdrawal is waived
- Pro-rated refunds ONLY if we terminate for non-violation reasons
- All other payments are non-refundable except as required by law

### Cancellation
You may cancel anytime. Access continues until end of billing period.

## 7. TELEMETRY & PRIVACY

See our Privacy Policy for details. Key points:
- Telemetry is OPT-IN (disabled by default)
- We collect only essential operational data
- No training on your code without explicit consent
- Privacy Mode available for zero data retention

## 8. DATA PROCESSING (GDPR)

For Pro tier customers acting as Data Controllers:
- We act as Data Processor when processing EU personal data
- Standard DPA available on request for enterprise customers
- Data retention: [specify periods]
- Data deletion: Available via CLI command or support request

## 9. LIMITATION OF LIABILITY

TO THE MAXIMUM EXTENT PERMITTED BY LAW:

**Service Provided "AS IS":**
- No warranty of uptime, availability, or specific results
- No warranty AI output will be error-free or secure
- No warranty against third-party IP infringement

**Liability Cap:**
Our total liability is limited to the GREATER of:
- (A) Amounts paid to us in the 6 months prior to the claim, OR
- (B) €100

**Excluded Damages:**
We are not liable for indirect, incidental, consequential, or
special damages, including lost profits, data loss, or business
interruption.

**EU Consumer Rights:**
This limitation does not affect statutory rights of EU consumers
for personal injury or damages caused by willful misconduct or
gross negligence.

## 10. WARRANTY DISCLAIMER

THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.

**AI OUTPUT DISCLAIMER:**
AI-generated code may be incorrect, insecure, or infringe third-party
rights. You assume all risk for use of AI outputs.

## 11. TERMINATION

### By You
Cancel anytime via CLI or account settings.

### By Us
We may suspend or terminate your account if:
- You violate these Terms
- Account inactive > 12 months without payment
- Required by law
- We cease operations (30 days notice)

### Effect of Termination
- Pro subscription ends immediately (no refund unless we terminate)
- You must cease using the Service
- We may delete your data after [30/90] days

## 12. DISPUTE RESOLUTION

### Governing Law
These Terms are governed by Italian law.

### Jurisdiction
Exclusive jurisdiction: Courts of [Milano/Città Rafa].

**EU Consumers:** You may also bring proceedings in your country
of residence. This clause does not affect EU consumer protection rights.

### Informal Resolution
Before filing a claim, contact us at legal@cervellaswarm.com to
attempt informal resolution.

## 13. MODIFICATIONS TO TERMS

We may modify these Terms at any time. Changes effective:
- Immediately for new users
- 30 days after notice for existing users

Continued use after changes constitutes acceptance.

You may reject changes by cancelling your account.

## 14. GENERAL

### Severability
If any provision is unenforceable, remaining provisions continue.

### No Waiver
Failure to enforce a provision is not a waiver of future enforcement.

### Entire Agreement
These Terms, plus Privacy Policy, constitute the entire agreement.

### Assignment
We may assign these Terms. You may not without our consent.

### Contact
Email: support@cervellaswarm.com
Legal: legal@cervellaswarm.com
Address: [Indirizzo Italia]

---

**For EU Consumers:** You have a 14-day right to withdraw from
purchase of digital content before performance begins. By explicitly
requesting immediate access to Pro features, you waive this right
as permitted under EU Consumer Rights Directive 2011/83/EU.

**Last Updated:** [Data]
```

---

## 2. PRIVACY POLICY GDPR-COMPLIANT

### 2.1 GDPR Requirements per CLI Tool

**PRINCIPI GDPR FONDAMENTALI:**

1. **Lawfulness, Fairness, Transparency**
   - Spiegare CHIARAMENTE cosa raccogli e perché
   - Linguaggio semplice (no legalese puro)
   - Disponibile prima di raccolta dati

2. **Purpose Limitation**
   - Raccogliere solo per scopi dichiarati
   - No "catch-all" generici
   - Specificare: telemetry, analytics, support, billing

3. **Data Minimization**
   - Solo dati strettamente necessari
   - CLI tool = MINIMO dati rispetto a web app
   - No tracking aggressivo

4. **Accuracy**
   - Permettere correzione dati
   - Email verification
   - Update profile

5. **Storage Limitation**
   - Specificare retention periods
   - Session data: 90 giorni
   - Account data: finché attivo + 30gg dopo cancellazione
   - Logs: 6-12 mesi massimo

6. **Integrity & Confidentiality**
   - Encryption in transit (TLS)
   - Encryption at rest (database)
   - Access controls

7. **Accountability**
   - Documentare compliance
   - Privacy by design
   - DPIA se high-risk (probabilmente NO per MVP)

### 2.2 Cosa Conta Come "Personal Data" in CLI Tool

**DATI PERSONALI TIPICI:**

```
RACCOLTI:
✅ Email address (account creation)
✅ Name (opzionale, per fattura)
✅ Payment info (via Stripe - non direttamente)
✅ IP address (logs server-side)
✅ Usage data (quali comandi, frequency)
✅ Error logs (se contengono file paths con username)
✅ Session identifiers

NON PERSONALI (se anonimizzati):
❌ Aggregated statistics (no individual identification)
❌ Hashed identifiers (se non reversibili)
❌ Generic error codes (no user-specific info)

ATTENZIONE:
⚠️ File paths possono contenere username (/Users/rafapra/...)
⚠️ Git commits possono avere email/nome
⚠️ Telemetry deve essere AGGREGATA e ANONYMIZED
```

### 2.3 Telemetry Opt-In/Opt-Out Requirements

**REGOLA ORO GDPR:**

```
CLI TOOL TELEMETRY = OPT-IN OBBLIGATORIO!

❌ SBAGLIATO (violazione GDPR):
   - Telemetry ON di default
   - "Opt-out se vuoi" dopo primo run
   - Raccolta prima del consenso

✅ CORRETTO:
   - Telemetry OFF di default
   - Primo run: "Abilita telemetry? [y/N]"
   - Consenso PRIMA di qualsiasi invio
   - Facilità di revoca uguale a consenso
```

**IMPLEMENTATION FLOW:**

```bash
# PRIMO RUN del CLI
$ cervellaswarm init

Welcome to CervellaSwarm! 🐝

Help us improve by sharing anonymous usage data?
- What we collect: command usage, error rates, performance metrics
- What we DON'T collect: your code, file contents, API keys
- You can change this anytime: cervellaswarm telemetry [on|off]
- Privacy Policy: https://cervellaswarm.com/privacy

Enable telemetry? [y/N]: _

# SE N o blank → telemetry.enabled = false
# SE y → telemetry.enabled = true + timestamp consent

# Stored in: ~/.cervellaswarm/config.json
{
  "telemetry": {
    "enabled": false,
    "consentDate": null,
    "consentVersion": "1.0"
  }
}
```

**REQUIREMENTS TECNICI:**

1. **Transparency (Art. 13 GDPR)**
   - Link a Privacy Policy durante prompt
   - Descrizione breve ma completa

2. **Freely Given (Art. 7 GDPR)**
   - No pre-checked boxes
   - Default = NO
   - Uso CLI funziona anche con telemetry OFF

3. **Specific & Informed**
   - Dire ESATTAMENTE cosa si raccoglie
   - No "may collect various data"

4. **Easy Revocation (Art. 7.3 GDPR)**
   ```bash
   cervellaswarm telemetry off
   cervellaswarm telemetry status
   cervellaswarm telemetry delete  # richiede conferma server-side
   ```

### 2.4 Data Retention Policy Best Practices

**RETENTION PERIODS RACCOMANDATI:**

| Data Type | Retention | Rationale |
|-----------|-----------|-----------|
| **Account Info** | Active + 30 days post-deletion | Allow recovery, then purge |
| **Session Logs** | 90 days | Debug, fraud detection |
| **Server Logs (IP)** | 6-12 months | Security, legal (max 72 months Italia telecom law) |
| **Telemetry Data** | 12 months aggregated | Product improvement |
| **Payment Records** | 7-10 years | Tax law Italia (7 anni fatture) |
| **Support Tickets** | 3 years | Business need |
| **Crash Reports** | 12 months | Bug fixing |

**ITALIA-SPECIFIC:**

```
TAX LAW (Codice Civile Art. 2220):
- Fatture: 10 anni
- Contabilità: 10 anni
- Corrispondenza commerciale: 10 anni

GDPR LIMITATION:
- Conservare solo lo stretto necessario
- Tax records OK per 10 anni (legal obligation)
- Altri dati: minimo indispensabile
```

**AUTO-DELETION POLICY:**

```javascript
// Esempio policy tecnica
const RETENTION_POLICY = {
  sessionLogs: { days: 90, action: 'delete' },
  telemetry: { days: 365, action: 'anonymize' },
  accountInactive: { days: 365, action: 'warn', thenDays: 30, thenAction: 'delete' },
  crashReports: { days: 365, action: 'delete' },
  supportTickets: { years: 3, action: 'archive' }
};

// Cron job giornaliero
// Automatico, documentato, compliance-ready
```

### 2.5 Template Privacy Policy per CervellaSwarm

```markdown
# Privacy Policy - CervellaSwarm

**Effective Date:** [Data]
**Last Updated:** [Data]
**Data Controller:** [Nome Società], [Indirizzo Italia]
**Contact:** privacy@cervellaswarm.com

---

## 1. INTRODUCTION

This Privacy Policy explains how CervellaSwarm ("we," "us," "our")
collects, uses, and protects your personal data when you use our
command-line interface (CLI) tool and related services.

We are committed to protecting your privacy and complying with:
- EU General Data Protection Regulation (GDPR)
- Italian Personal Data Protection Code (D.Lgs. 196/2003)
- Italian AI Law No. 132/2025

**If you are an EU resident, you have specific rights under GDPR.
See Section 8 for details.**

---

## 2. DATA WE COLLECT

### 2.1 Account Information
When you create an account:
- **Email address** (required) - for authentication and communication
- **Name** (optional) - for invoices and personalization
- **Password** (hashed) - for account security

### 2.2 Payment Information
For Pro tier subscriptions:
- **Payment details** - processed by Stripe (we do NOT store card numbers)
- **Billing address** - for invoicing and tax compliance
- **VAT/Tax ID** (if provided) - for B2B invoicing

### 2.3 Usage Data (Telemetry)
**ONLY if you opt-in:**
- Commands executed (no arguments, no file paths)
- Error rates and crash reports
- Performance metrics (execution time, memory usage)
- CLI version and OS information

**What we DON'T collect:**
- Your code or file contents
- API keys or credentials
- Specific file names or paths
- Git repository contents

### 2.4 Server Logs
For security and technical operations:
- **IP address** - retained for 6 months
- **Request timestamps**
- **API endpoints accessed**
- **Authentication attempts**

### 2.5 AI Interaction Data
When using AI features:
- **Prompts/queries** (ONLY with your explicit consent)
- **AI responses** (for service improvement, opt-in only)
- **Privacy Mode:** If enabled, ZERO data retained on our servers

---

## 3. HOW WE USE YOUR DATA

### 3.1 Legal Basis for Processing

| Purpose | Legal Basis | Data Used |
|---------|-------------|-----------|
| Provide CLI service | Contract | Account info, authentication |
| Process payments | Contract | Payment info (via Stripe) |
| Telemetry | Consent (opt-in) | Usage data |
| Security/fraud prevention | Legitimate interest | IP logs, access patterns |
| Legal compliance | Legal obligation | Tax records, invoices |
| Customer support | Legitimate interest | Support tickets, account info |

### 3.2 Specific Purposes

**To provide the service:**
- Authenticate your account
- Execute AI-powered commands
- Store your preferences and configurations

**To improve CervellaSwarm:**
- Analyze aggregated usage patterns (ONLY if you opt-in)
- Identify and fix bugs
- Develop new features

**To communicate with you:**
- Service updates and maintenance notices
- Billing and payment confirmations
- Respond to support requests
- Marketing (ONLY with separate consent, easy opt-out)

**For security:**
- Detect and prevent fraud
- Protect against abuse and attacks
- Ensure system integrity

**For legal compliance:**
- Fulfill tax and accounting obligations (Italy: 10-year record retention)
- Respond to legal requests
- Enforce our Terms of Service

---

## 4. DATA SHARING

We do NOT sell your personal data. We share data only as follows:

### 4.1 Service Providers
- **Stripe** - Payment processing (PCI DSS compliant)
- **Anthropic/OpenAI** - AI model APIs (see Section 4.2)
- **Cloud hosting** - AWS/GCP (EU region, GDPR-compliant)

### 4.2 AI Model Providers
When you use AI features:
- **Anthropic (Claude API)**
  - Your prompts are sent to Anthropic
  - NOT used for training (Anthropic policy)
  - Privacy Mode: Zero data retention option

- **OpenAI (GPT API)**
  - Your prompts are sent to OpenAI
  - NOT used for training (as of [date], per OpenAI policy)
  - Optional: Use Azure OpenAI for EU data residency

### 4.3 Legal Requirements
We may disclose data if required by:
- Court orders or legal processes
- Italian or EU law enforcement
- Protection of our rights or safety

---

## 5. DATA RETENTION

| Data Type | Retention Period | Reason |
|-----------|------------------|--------|
| Account info | Active account + 30 days | Account recovery |
| Payment records | 10 years | Italian tax law |
| Usage logs | 90 days | Technical support |
| Server logs (IP) | 6 months | Security |
| Telemetry data | 12 months (aggregated) | Product improvement |
| Support tickets | 3 years | Business records |

**Automated Deletion:**
We automatically delete or anonymize data when retention periods expire.

**Your Right to Deletion:**
You can request immediate deletion (see Section 8.5).

---

## 6. DATA SECURITY

We implement technical and organizational measures:

**Technical Measures:**
- Encryption in transit (TLS 1.3)
- Encryption at rest (AES-256)
- Secure password hashing (bcrypt)
- API key rotation and secure storage

**Organizational Measures:**
- Access control (least privilege principle)
- Regular security audits
- Employee confidentiality agreements
- Incident response plan

**No system is 100% secure.** You are responsible for:
- Keeping your password confidential
- Securing your local ~/.cervellaswarm/ configuration
- Protecting your API keys

---

## 7. INTERNATIONAL DATA TRANSFERS

### 7.1 EU Data Protection
If you are in the EU/EEA:
- Primary data storage: EU region (AWS Frankfurt or GCP Belgium)
- AI API calls may go to US (Anthropic, OpenAI)
  - Protected by Standard Contractual Clauses (SCCs)
  - Or use Azure OpenAI (EU-based) option

### 7.2 Your Options
- **Privacy Mode:** Keep all data local, zero cloud retention
- **EU-Only Mode:** Use only EU-based AI providers (Azure OpenAI)

---

## 8. YOUR RIGHTS (GDPR)

If you are an EU resident, you have the following rights:

### 8.1 Right of Access (Art. 15 GDPR)
Request a copy of your personal data:
```bash
cervellaswarm data export
# or email: privacy@cervellaswarm.com
```

### 8.2 Right to Rectification (Art. 16 GDPR)
Correct inaccurate data:
```bash
cervellaswarm account update
```

### 8.3 Right to Erasure (Art. 17 GDPR)
Delete your account and data:
```bash
cervellaswarm account delete
# Confirmation required. Data deleted within 30 days.
# Exception: Payment records (tax law requires 10-year retention)
```

### 8.4 Right to Restrict Processing (Art. 18 GDPR)
Limit how we use your data (contact privacy@cervellaswarm.com).

### 8.5 Right to Data Portability (Art. 20 GDPR)
Receive your data in machine-readable format:
```bash
cervellaswarm data export --format json
```

### 8.6 Right to Object (Art. 21 GDPR)
Object to data processing based on legitimate interest (contact us).

### 8.7 Right to Withdraw Consent
For telemetry and marketing:
```bash
cervellaswarm telemetry off
cervellaswarm marketing unsubscribe
```

### 8.8 Right to Lodge a Complaint
If you believe we violate GDPR, contact:
**Garante per la Protezione dei Dati Personali (Italy)**
- Website: https://www.garanteprivacy.it
- Email: garante@gpdp.it

---

## 9. COOKIES & TRACKING

**CLI Tool:**
- We do NOT use cookies (CLI has no browser context)
- No web tracking scripts

**Website (if applicable):**
- Essential cookies only (authentication, preferences)
- No advertising or analytics cookies without consent
- Cookie banner with opt-in for non-essential cookies

---

## 10. CHILDREN'S PRIVACY

CervellaSwarm is not intended for users under 16 (GDPR age).
We do not knowingly collect data from children.

If you are a parent and believe your child provided data,
contact us immediately at privacy@cervellaswarm.com.

---

## 11. AI-SPECIFIC PROVISIONS (Italian Law No. 132/2025)

### 11.1 AI-Assisted Content
Code generated using CervellaSwarm's AI features:
- May require human intellectual contribution for copyright protection
- You are responsible for reviewing and validating output
- We do not claim ownership of AI-generated content

### 11.2 Training Data
Your prompts and code are NOT used to train AI models unless:
- You explicitly opt-in to a training data program (future feature)
- You report a bug or provide feedback (only that specific data)

### 11.3 Transparency
AI features clearly labeled. We disclose when AI is used.

---

## 12. CHANGES TO THIS POLICY

We may update this Privacy Policy to reflect:
- Legal or regulatory changes
- New features or data practices
- Feedback and best practices

**Notification:**
- Email to registered users (30 days before changes)
- CLI notification on next run
- Updated "Last Updated" date at top

**Your Options:**
- Continue using = acceptance of changes
- Disagree? Delete your account before changes take effect

---

## 13. CONTACT US

**Data Controller:** [Nome Società Legale]
**Address:** [Indirizzo completo Italia]
**Email:** privacy@cervellaswarm.com
**DPO (if appointed):** dpo@cervellaswarm.com

**For GDPR requests:**
- Email privacy@cervellaswarm.com with subject "GDPR Request"
- Include proof of identity
- We respond within 30 days (GDPR requirement)

---

**Last Updated:** [Data]

---

## APPENDIX: DATA PROCESSING DETAILS (Technical)

### Data Storage Locations
- **EU users:** AWS Frankfurt (eu-central-1) or GCP Belgium
- **Non-EU users:** AWS US-East or GCP US-Central
- **Backups:** Encrypted, same region as primary

### Third-Party Subprocessors
- Stripe, Inc. (USA) - Payment processing
- Anthropic PBC (USA) - AI models
- OpenAI, LP (USA) - AI models
- Amazon Web Services (Ireland) - Hosting
- [Add others as needed]

### Data Processing Agreement (DPA)
For enterprise customers processing EU personal data,
a Standard DPA is available upon request: legal@cervellaswarm.com
```

---

## 3. AI-SPECIFIC LEGAL REQUIREMENTS (2025-2026)

### 3.1 EU AI Act Implications (August 2, 2026)

**STATUS PER CERVELLASWARM:**

```
CLASSIFICATION: DEVELOPER TOOL CON AI GENERATIVO

RISK LEVEL: LOW-RISK (probabilmente)
- Non è sistema educativo/HR (high-risk)
- Non è critical infrastructure (high-risk)
- È tool per developer professionisti
- Output richiede validazione umana

REQUIREMENTS APPLICABILI:
✅ Transparency rules (Aug 2, 2026)
✅ AI-generated content marking
✅ Copyright policy (training data)
⏸ GPAI model requirements (solo se facciamo fine-tuning nostro)
❌ Conformity assessment (solo high-risk)
```

**TRANSPARENCY REQUIREMENTS (Art. 50):**

1. **Labeling AI Outputs**
   ```bash
   # Nel CLI, quando AI genera codice:
   ✨ [AI Generated] Using Claude Sonnet 4.5

   ⚠️ Warning: AI-generated code requires review
   - Validate for correctness and security
   - Check for licensing compliance
   - Test thoroughly before production use
   ```

2. **User Disclosure**
   - Deve essere CHIARO che stanno interagendo con AI
   - Probabilmente già evidente (comando "ask AI")
   - Docs must state "AI-powered" prominently

3. **Copyright Policy**
   - Dichiarare che usiamo API third-party (Anthropic, OpenAI)
   - Non facciamo training su user code (policy)
   - User retains IP rights su output

**IMPLEMENTATION CHECKLIST:**

| Requirement | Status | Action |
|-------------|--------|--------|
| Disclose AI use | ✅ | CLI help text + docs |
| Label AI outputs | ⏸ | Add prefixes to AI responses |
| Copyright policy | ⏸ | Add to ToS + docs |
| Training data transparency | ✅ | We don't train, state policy |
| Technical documentation | ⏸ | For Pro tier audit |

### 3.2 Italia AI Law (October 10, 2025)

**LAW NO. 132/2025 - KEY PROVISIONS:**

1. **Copyright Protection for AI-Assisted Works**
   ```
   RULE: AI-generated work HAS copyright protection ONLY IF:
   - Significant human intellectual contribution
   - Author's creative input evident

   FOR CERVELLASWARM USERS:
   - Code generated by AI alone = NO copyright (public domain?)
   - Code with significant user modification = HAS copyright
   - User must ADD creative input for protection
   ```

2. **Text and Data Mining (TDM) Exception**
   - Italia allows TDM for AI training
   - BUT scope unclear (narrow vs broad interpretation)
   - Criminal penalties for violations

3. **DISCLAIMER NECESSARIO:**
   ```
   "AI-generated code may not qualify for copyright protection
   under Italian Law No. 132/2025 unless significantly modified
   with human intellectual contribution. You are responsible for
   determining copyright status and ensuring compliance with
   applicable laws."
   ```

### 3.3 Liability per AI Output

**SCENARIO PROBLEMATICI:**

1. **AI genera codice con bug → app dell'utente crashes**
   - CHI È RESPONSABILE? Utente! (warranty disclaimer)

2. **AI copia codice copyrighted → utente viene citato**
   - CHI È RESPONSABILE? Ancora utente! (see Copilot litigation)

3. **AI suggerisce codice insicuro → data breach**
   - CHI È RESPONSABILE? Utente! (must validate)

**DISCLAIMER OBBLIGATORIO (nel ToS):**

```markdown
## AI OUTPUT LIABILITY

**YOU ASSUME ALL RISK FOR AI-GENERATED CONTENT.**

CervellaSwarm uses third-party AI models (Anthropic Claude, OpenAI GPT)
to generate code and suggestions. While we strive for quality:

1. **No Accuracy Guarantee**
   AI output may contain errors, bugs, or security vulnerabilities.

2. **No IP Indemnity**
   AI may inadvertently reference copyrighted material. You are
   responsible for ensuring your use complies with copyright law.

3. **No Fitness Guarantee**
   AI-generated code may not meet your specific requirements or
   industry standards.

4. **Your Responsibilities**
   - Review all AI outputs carefully
   - Test code thoroughly before production use
   - Verify compliance with licenses and copyrights
   - Validate security and performance

5. **Limitation of Liability**
   We are not liable for any damages arising from use of AI outputs,
   including but not limited to data loss, security breaches,
   copyright infringement claims, or business interruption.

**Canadian Case Law (Moffatt v. Air Canada):**
Even if misinformation comes from AI, the SERVICE PROVIDER is liable.
However, CervellaSwarm is a TOOL (not decision-maker). User retains
editorial control and responsibility for all outputs.

**Italian Law No. 132/2025:**
AI-assisted works require significant human intellectual contribution
for copyright protection. You must substantially modify and validate
AI outputs to claim authorship.
```

**BEST PRACTICES PER RIDURRE LIABILITY:**

1. ✅ Clear disclaimers (in ToS, CLI warnings, docs)
2. ✅ User acceptance of AI risks before first use
3. ✅ Prominent labeling of AI-generated content
4. ✅ Educational content (docs on validating AI output)
5. ⏸ Professional liability insurance (Fase 2 - Pro tier)

### 3.4 Training Data Disclosure

**EU AI ACT REQUIREMENT (GPAI models):**

Se facciamo fine-tuning o training custom:
- Disclose training data sources
- Public summary required
- Copyright compliance

**PER CERVELLASWARM MVP:**

```
NON APPLICABILE - Usiamo solo API third-party!

STATEMENT NEL ToS:
"CervellaSwarm does not train AI models. We use third-party APIs:
- Anthropic Claude (via API)
- OpenAI GPT (via API)

Training data and model details: See respective providers' policies:
- Anthropic: https://www.anthropic.com/legal/...
- OpenAI: https://openai.com/policies/...

Your code and prompts are NOT used for training unless you
explicitly opt-in to a future training program (not yet available)."
```

---

## 4. DATA RETENTION POLICIES

### 4.1 GDPR Best Practices

**PRINCIPLE: Storage Limitation (Art. 5.1.e GDPR)**

```
Personal data shall be kept in a form which permits identification
of data subjects for no longer than is necessary for the purposes
for which the personal data are processed.
```

**PER CERVELLASWARM:**

| Data Category | Retention | Legal Basis | Auto-Delete |
|---------------|-----------|-------------|-------------|
| **Account Data** | Active + 30 days | Legitimate interest | ✅ |
| **Payment Records** | 10 years | Legal obligation (Italy tax) | ❌ |
| **Session Logs** | 90 days | Legitimate interest | ✅ |
| **Server Logs (IP)** | 6-12 months | Legitimate interest | ✅ |
| **Telemetry (aggregated)** | 12 months | Consent | ✅ |
| **Crash Reports** | 12 months | Legitimate interest | ✅ |
| **Support Tickets** | 3 years | Contract, legitimate interest | ✅ |
| **Marketing Consent** | Active + 2 years | Consent | ✅ |

### 4.2 Italia-Specific Requirements

**TAX LAW (DPR 633/1972):**

```
FATTURE E REGISTRI CONTABILI: 10 ANNI

Documentazione da conservare:
- Fatture emesse e ricevute
- Registri IVA
- Libro giornale
- Libro inventari
- Dichiarazioni fiscali

FORMATO: Cartaceo o digitale (con firma digitale)
```

**GDPR vs TAX LAW:**

```
DOMANDA: GDPR dice "minimo necessario", tax law dice "10 anni"
RISPOSTA: Legal obligation prevails!

SOLUTION:
- Fatture: conserva 10 anni (legal obligation)
- Altri account data: minimo necessario (30-90 giorni)
- Separate storage: tax records vs operational data
```

### 4.3 Implementation Tecnica

**AUTOMATED DELETION SCRIPT:**

```javascript
// Daily cron job: data-retention-cleanup.js

const RETENTION_POLICIES = {
  // Account data
  deletedAccounts: {
    table: 'users',
    condition: 'deleted_at IS NOT NULL AND deleted_at < NOW() - INTERVAL 30 DAY',
    action: 'HARD_DELETE',
    notifyDPO: true
  },

  // Session logs
  sessionLogs: {
    table: 'session_logs',
    condition: 'created_at < NOW() - INTERVAL 90 DAY',
    action: 'DELETE',
  },

  // Server logs (IP addresses)
  serverLogs: {
    table: 'api_logs',
    condition: 'created_at < NOW() - INTERVAL 6 MONTH',
    action: 'ANONYMIZE', // Remove IP, keep aggregates
  },

  // Telemetry (anonymize after aggregation)
  telemetry: {
    table: 'telemetry_events',
    condition: 'created_at < NOW() - INTERVAL 12 MONTH',
    action: 'DELETE', // After aggregation to reports table
  },

  // Crash reports
  crashReports: {
    table: 'crash_reports',
    condition: 'created_at < NOW() - INTERVAL 12 MONTH',
    action: 'DELETE',
  },

  // EXCEPTION: Payment records (Italian tax law)
  paymentRecords: {
    table: 'invoices',
    condition: 'created_at < NOW() - INTERVAL 10 YEAR',
    action: 'ARCHIVE', // Move to cold storage, not delete
    reason: 'Italian tax law (DPR 633/1972) requires 10-year retention'
  }
};

// Execute cleanup
async function runRetentionCleanup() {
  for (const [policy, config] of Object.entries(RETENTION_POLICIES)) {
    console.log(`Running retention policy: ${policy}`);

    const rowsAffected = await executeRetentionAction(config);

    // Log for GDPR accountability
    await logRetentionAction({
      policy,
      rowsAffected,
      timestamp: new Date(),
      action: config.action
    });

    if (config.notifyDPO && rowsAffected > 0) {
      await notifyDPO(`${policy}: ${rowsAffected} rows processed`);
    }
  }
}

// Schedule: Daily at 2 AM UTC
schedule.scheduleJob('0 2 * * *', runRetentionCleanup);
```

**DOCUMENTATION (for GDPR accountability):**

```
FILE: docs/data-retention-policy.md

# Data Retention Policy - CervellaSwarm

## Purpose
This policy ensures compliance with GDPR Art. 5.1.e (storage limitation)
and Italian tax law requirements.

## Retention Periods
[Table from Section 4.1]

## Automated Processes
- Daily cron job: data-retention-cleanup.js
- Logs: /var/log/retention-cleanup.log
- DPO notifications: On deletedAccounts actions

## Manual Processes
- Tax records archival: Annual (December)
- Audit: Quarterly by DPO or compliance officer

## User Rights
Users can request immediate deletion (GDPR Art. 17) via:
- CLI: cervellaswarm account delete
- Email: privacy@cervellaswarm.com

Exception: Payment records retained 10 years per Italian law.

## Review Schedule
This policy is reviewed annually or upon legal changes.

Last reviewed: [Date]
Next review: [Date + 1 year]
```

---

[CONTINUA NELLA PARTE 2...]
