# Baseline Email Features - Industry Standard 2026

**Data Ricerca:** 13 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Scopo:** Definire le features BASE che ogni client email DEVE avere per essere competitivo

---

## Executive Summary

Questa ricerca analizza le funzionalità standard presenti nei principali client email (Gmail, Outlook, Apple Mail, Superhuman) per identificare:

1. **Must-Have Features** - Funzionalità obbligatorie, senza le quali un client email è considerato incompleto
2. **Expected Features** - Funzionalità che gli utenti si aspettano di trovare (standard del 2026)
3. **Differentiating Features** - Funzionalità che distinguono i client premium

**Metodologia:** Web research su documentazione ufficiale, guide utente, e analisi comparative dei player più grossi.

---

## 1. FEATURES OBBLIGATORIE (Must-Have)

### 1.1 Gestione Messaggi Base

- [ ] **Compose/Reply/Forward**
  - Compose nuovo messaggio
  - Reply (rispondi al mittente)
  - Reply All (rispondi a tutti)
  - Forward (inoltra)

- [ ] **Thread/Conversation View**
  - Raggruppamento messaggi per conversazione
  - Ordinamento cronologico
  - Subject line come chiave di raggruppamento
  - Indicatore numero messaggi nel thread
  - *Best Practice:* Subject line chiaro, stay on topic, trim excess content

- [ ] **Azioni Base Messaggi**
  - Archive (rimuovi da inbox senza cancellare)
  - Delete (cancella definitivamente)
  - Mark as Read/Unread
  - Star/Flag (segnala come importante)

### 1.2 Labels/Folders (Organizzazione)

- [ ] **Sistema Labels (Gmail approach) o Folders (Outlook approach)**
  - Creazione/modifica/eliminazione labels
  - Applicazione multipla labels per messaggio (Gmail)
  - Nesting/hierarchy labels (sub-labels)
  - Color coding per visual organization
  - *Standard Gmail:* Un messaggio può avere N labels
  - *Standard Outlook:* Un messaggio in una sola cartella

- [ ] **Filtri/Rules Automatici**
  - Criteri: from, to, subject, body keywords, attachment, size
  - Azioni: apply label, archive, delete, forward, star
  - Gestione filtri esistenti
  - *Gmail:* chiamati "Filters", più flessibili
  - *Outlook:* chiamati "Rules", limiti su account terze parti

### 1.3 Search (Ricerca)

- [ ] **Search Base**
  - Full-text search in subject/body
  - Search in From/To
  - Date range search

- [ ] **Search Operators Standard** (CRITICAL!)
  ```
  from:email@example.com      # Da mittente specifico
  to:email@example.com        # A destinatario specifico
  subject:keyword             # Nel subject
  has:attachment              # Con allegati
  filename:pdf                # Tipo allegato specifico
  larger:5M                   # Dimensione > 5MB
  smaller:1M                  # Dimensione < 1MB
  after:YYYY/MM/DD            # Dopo data
  before:YYYY/MM/DD           # Prima di data
  is:unread                   # Non letti
  is:read                     # Letti
  is:starred                  # Con stella
  label:labelname             # Con label specifica (Gmail)
  in:folder                   # In cartella specifica (Outlook)

  # Boolean Operators
  AND, OR, NOT                # Operatori booleani (uppercase!)
  "exact phrase"              # Frase esatta
  -exclude                    # Escludi termine
  ```

- [ ] **Saved Searches / Smart Mailboxes**
  - Salvare ricerche complesse per riuso
  - *Apple Mail:* Smart Mailboxes (solo locale, non sync)

### 1.4 Attachments

- [ ] **Attachment Handling**
  - Upload file (drag-and-drop + file picker)
  - Preview inline (PDF, immagini, docs)
  - Download singolo file
  - Download tutti allegati (zip)
  - Indicatore tipo file e dimensione

- [ ] **Attachment Size Limits**
  - **Gmail:** 25 MB per email, auto-upgrade a Google Drive per file > 25MB
  - **Outlook:** 20 MB (consumer), 10 MB default (corporate), 150 MB con OneDrive (M365)
  - **Apple Mail:** Variabile, dipende da provider
  - *Best Practice:* Auto-convert a cloud link per file grandi

### 1.5 Contacts Autocomplete

- [ ] **To/Cc/Bcc Autocomplete**
  - Autocomplete da address book
  - Autocomplete da email recenti
  - Keyboard navigation (Up/Down arrows, Enter to select)
  - Display: nome + email
  - Multiple recipients support

- [ ] **UX Best Practices**
  - Show suggestions after 2-3 characters
  - Max 5-7 suggestions visible
  - Highlight matching text
  - Support keyboard-only navigation
  - Accessibility: screen reader support

### 1.6 Draft Management

- [ ] **Auto-Save Drafts**
  - **Industry Standard:** Auto-save ogni 3 minuti (web)
  - **Outlook Desktop:** Configurabile 1-99 minuti
  - Auto-save on window close
  - Draft recovery su crash browser

- [ ] **Draft Folder**
  - Lista drafts salvati
  - Edit/Resume draft
  - Delete draft

---

## 2. FEATURES ATTESE (Expected - Standard 2026)

### 2.1 Productivity Features

- [ ] **Snooze**
  - Nasconde email temporaneamente
  - Ritorna come unread all'orario scelto
  - Preset comuni: Later Today, Tomorrow, This Weekend, Next Week, Custom
  - *Gmail:* Snoozed folder dedicata
  - *Outlook:* Snoozed folder + reminder icon

- [ ] **Send Later / Schedule Send**
  - Componi ora, invia dopo
  - Scheduling preciso (data + ora)
  - Batch composition workflow

- [ ] **Reminders**
  - Reminder per follow-up
  - Reminder se no reply entro X giorni
  - Integration con calendario

- [ ] **Undo Send**
  - Cancel invio entro 5-30 secondi (configurabile)
  - *Gmail:* Default 5 sec, max 30 sec

### 2.2 Bulk Operations

- [ ] **Multi-Select**
  - Checkbox select
  - Select All (in current view)
  - Select All + Search filter combo
  - Shift-click range select
  - Ctrl/Cmd-click multi-select

- [ ] **Bulk Actions**
  - Archive selected
  - Delete selected
  - Mark as read/unread
  - Apply label (Gmail) / Move to folder (Outlook)
  - Star/Unstar

- [ ] **Search → Select All → Bulk Action Pattern**
  - *Example:* Search "from:amazon.com older_than:6m" → Select All → Archive
  - Precision bulk management

### 2.3 Keyboard Shortcuts

**Standard Shortcuts (Gmail-style, de-facto standard):**

```
# Navigation
j                  # Next email
k                  # Previous email
o / Enter          # Open email
u                  # Back to inbox

# Actions
e                  # Archive
#                  # Delete
r                  # Reply
a                  # Reply all
f                  # Forward
s                  # Star
x                  # Select email (for bulk ops)

# Composition
c                  # Compose
/                  # Search
Cmd/Ctrl + Enter   # Send email

# Advanced
[                  # Archive + go to previous
]                  # Archive + go to next
z                  # Undo last action
```

**Best Practice:**
- Cmd/Ctrl + K = Command palette (Superhuman approach)
- 80+ shortcuts per power users
- Onboarding per keyboard shortcuts essenziali

### 2.4 Mobile UX Patterns

- [ ] **Swipe Gestures**
  - **Swipe Right:** Archive (default Gmail)
  - **Swipe Left:** Delete/Trash or More options
  - Customizable swipe actions
  - Alternative actions: Move to, Mark as read/unread, Snooze

- [ ] **Swipe-to-Reveal**
  - Swipe parziale: mostra action buttons
  - Swipe completo: esegui azione default

- [ ] **Accessibility**
  - Always provide visible controls (no gesture-only)
  - Haptic feedback
  - Animation feedback

### 2.5 AI-Powered Features (2026 Standard)

- [ ] **Smart Compose**
  - Autocomplete frasi mentre scrivi
  - Neural network predictions
  - Tab to accept suggestion

- [ ] **Smart Reply**
  - 3 suggested quick replies
  - Context-aware (personalized to writing style)
  - One-click to send

- [ ] **AI Thread Summaries** (NEW 2026)
  - Auto-summarize long threads
  - Key points extraction
  - *Gmail Gemini 3:* Free per tutti (US only al momento)

- [ ] **AI Proofreading**
  - Grammar check
  - Tone adjustment
  - Style suggestions
  - *Gmail:* Solo Google AI Pro/Ultra

- [ ] **Help Me Write**
  - Draft from scratch con prompt
  - Polish existing text
  - *Gmail:* Free per tutti

**Privacy Note:**
- Smart features richiedono analisi del contenuto
- Controversia 2024: training AI su email utenti?
- GDPR compliance obbligatorio
- Opt-in/Opt-out trasparente

### 2.6 Unsubscribe (Compliance 2026)

- [ ] **One-Click Unsubscribe**
  - RFC 8058 standard (dal 2017)
  - List-Unsubscribe header + List-Unsubscribe-Post header
  - HTTPS URI required
  - DKIM signature validation

- [ ] **Sender Requirements (Google/Yahoo 2024+)**
  - Obbligatorio per senders > 5000 emails/day
  - Visible unsubscribe link in body
  - Processing entro 2 giorni
  - *2026:* Grace period FINITO - enforcement attivo

- [ ] **UI Pattern**
  - "Unsubscribe" button in header email
  - Confirmation dialog
  - Success message

### 2.7 Security Features

- [ ] **Spam Filtering**
  - Machine Learning detection
  - > 99.9% spam blocked (industry standard)
  - ~15 billion spam/day processati (Gmail)
  - Auto-move to Spam folder

- [ ] **Phishing Detection**
  - AI-powered detection (LLM-based analysis - Microsoft 2024+)
  - Warning banners per sospetti phishing
  - Sender verification
  - Link safety check

- [ ] **Malware Protection**
  - Attachment scanning
  - Quarantine files sospetti
  - Safe preview (sandboxed)

- [ ] **Business Email Compromise (BEC) Detection**
  - Intent analysis (LLM)
  - Behavioral patterns
  - *Critical for 2026:* AI vs AI (attacker AI vs detection AI)

### 2.8 Email Authentication (2026 Mandatory)

- [ ] **SPF, DKIM, DMARC**
  - Sender verification
  - *2026:* Non opzionale - Google/Yahoo/Microsoft enforcement attivo
  - SMB compliance obbligatoria

---

## 3. FEATURES DIFFERENZIANTI (Premium/Nice-to-Have)

### 3.1 Superhuman-Style Features

- [ ] **Speed-First UX**
  - Sub-100ms load time
  - Instant search
  - Zero lag keyboard shortcuts

- [ ] **Split Inbox**
  - Multiple inbox views side-by-side
  - Gmail filters → separate inboxes
  - Custom categorization

- [ ] **Email Tracking**
  - Read receipts
  - Link click tracking
  - Time-based analytics

- [ ] **Snippets/Templates**
  - Text expansion shortcuts
  - Reusable email templates
  - Variables support

- [ ] **Calendar Integration**
  - Auto-show calendar on invite email
  - Availability sharing (Cmd+Shift+A)
  - Inline scheduling

### 3.2 Advanced Collaboration

- [ ] **Shared Inboxes**
  - Team access
  - Assignment/ownership
  - Internal notes/comments

- [ ] **Email Delegation**
  - "Send as" another user
  - Delegate access permissions

### 3.3 Advanced Analytics

- [ ] **Email Stats**
  - Response time metrics
  - Inbox zero tracking
  - Productivity insights

- [ ] **Sender Insights**
  - Email frequency per sender
  - Auto-suggest unsubscribe per low-value senders

---

## 4. MOBILE-SPECIFIC FEATURES

### 4.1 Must-Have Mobile

- [ ] **Pull-to-Refresh**
- [ ] **Swipe Actions** (configurabili)
- [ ] **Push Notifications** (configurabili per VIP/labels)
- [ ] **Offline Access**
- [ ] **Responsive Design** (tablet + phone)

### 4.2 Mobile Best Practices

- [ ] Max 3-4 swipe actions (choice paralysis)
- [ ] Visual feedback (animations, haptic)
- [ ] All-in-viewport suggestions (no scroll per autocomplete)
- [ ] Bottom navigation (thumb-friendly)

---

## 5. COMPETITOR ANALYSIS SUMMARY

| Feature Category | Gmail | Outlook | Apple Mail | Superhuman |
|------------------|-------|---------|------------|------------|
| **Labels/Folders** | Labels (multi) | Folders (single) | Mailboxes | Labels + Split Inbox |
| **Search Operators** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Keyboard Shortcuts** | ⭐⭐⭐⭐ (enable req) | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (80+) |
| **AI Features** | ⭐⭐⭐⭐⭐ (Gemini 3) | ⭐⭐⭐⭐ (Copilot) | ⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Attachment Limit** | 25 MB → Drive | 20 MB → OneDrive | Variabile | 25 MB → Drive |
| **Price** | Free | Free / M365 | Free | $30-40/mo |

**Key Insight:**
- **Gmail** = Standard de-facto per search operators e AI features
- **Superhuman** = Gold standard per speed e keyboard-first UX
- **Outlook** = Dominante in corporate, rules/automation
- **Apple Mail** = Semplice, integrato, ma search limitato

---

## 6. RECOMMENDED PRIORITY FOR MIRACOLLOOK

### Phase 1: MINIMUM VIABLE EMAIL CLIENT (MVP)

**Obiettivo:** Parità funzionale con client base.

1. ✅ Compose/Reply/Forward
2. ✅ Thread view
3. ✅ Archive/Delete/Star
4. ✅ Labels con color coding
5. ✅ Search con operatori base (from, to, subject, has:attachment)
6. ✅ Attachments (upload, preview, download)
7. ✅ Contacts autocomplete
8. ✅ Draft auto-save (3 min)
9. ✅ Keyboard shortcuts essenziali (j/k navigation, e archive, r reply)
10. ✅ Mobile: swipe actions base

### Phase 2: EXPECTED FEATURES (Competitive Parity)

**Obiettivo:** Parità con Gmail/Outlook 2026.

11. Filters/Rules automatici
12. Search operators completi (full Gmail search syntax)
13. Bulk operations (multi-select + bulk actions)
14. Snooze
15. Send Later
16. Undo Send
17. Smart Compose/Reply (AI)
18. Unsubscribe one-click
19. Spam/Phishing detection
20. Keyboard shortcuts full set (80+)

### Phase 3: DIFFERENTIATING FEATURES (Competitive Edge)

**Obiettivo:** Superare la baseline, creare valore unico.

21. Speed-first architecture (< 100ms load)
22. Split Inbox (Superhuman approach)
23. Email tracking
24. Advanced AI (thread summaries, help me write)
25. Shared inboxes (team collaboration)
26. Email analytics/insights

---

## 7. TECHNICAL IMPLEMENTATION NOTES

### 7.1 Search Operators Implementation

**Backend:**
- Parse query string → AST (Abstract Syntax Tree)
- Support boolean operators (AND, OR, NOT)
- Date range parsing
- Size comparison operators
- Label/folder filtering

**Frontend:**
- Autocomplete search operators
- Syntax highlighting in search box
- "Search chips" (Gmail approach) per visual filter building

### 7.2 Attachment Handling

**Upload:**
- Drag-and-drop API
- File input fallback
- Multi-file support
- Progress indicators

**Preview:**
- PDF.js per PDF
- Image preview inline
- Google Docs/Office viewer fallback

**Large Files:**
- Detect size > limit
- Auto-prompt "Upload to cloud?"
- Generate shareable link
- Insert link in email body

### 7.3 Draft Auto-Save

**Strategy:**
- Debounce 3 minuti dopo ultimo input
- onbeforeunload listener (save on tab close)
- LocalStorage backup (offline resilience)
- Conflict resolution (multiple devices)

### 7.4 AI Features (Future-Proofing)

**Options:**
- OpenAI GPT-4 API per Smart Compose/Reply
- Google Gemini API
- Self-hosted LLM (privacy-first approach)

**Privacy:**
- Opt-in esplicito
- Data processing transparency
- GDPR compliance
- No training on user data (contractual guarantee)

---

## 8. SOURCES & REFERENCES

### Gmail Documentation
- [Gmail Search Operators - Google Support](https://support.google.com/mail/answer/7190?hl=en)
- [Gmail Keyboard Shortcuts - Google Support](https://support.google.com/mail/answer/6594?hl=en)
- [Gmail Labels Guide](https://support.google.com/mail/answer/118708?hl=en)
- [20 Gmail Search Operators | Kinsta](https://kinsta.com/blog/gmail-search-operators/)
- [How to Organize Gmail (2026) | HubSpot](https://www.hubspot.com/email-signature-generator/organize-email-gmail)
- [Gmail Attachment Size Limit | EmailAnalytics](https://emailanalytics.com/gmail-attachment-size-limit/)
- [How to Use Gmail Keyboard Shortcuts | Clean Email](https://clean.email/blog/email-providers/gmail-keyboard-shortcuts)
- [Gmail launches AI features with Gemini 3 | Google Blog](https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/)
- [6 ways Gmail uses AI features | Google Blog](https://blog.google/products-and-platforms/products/gmail/gmail-ai-features/)

### Superhuman Analysis
- [Superhuman Keyboard Shortcuts | Superhuman Help](https://help.superhuman.com/hc/en-us/articles/45191759067411-Speed-Up-With-Shortcuts)
- [Updated List of Superhuman Shortcuts (2025) | Nick Gray](https://nickgray.net/superhuman/)
- [How to use Superhuman like a semi-pro | Arman](https://writing.arman.do/p/superhuman)
- [Superhuman Pricing, Alternatives | Capterra](https://www.capterra.com/p/199278/Superhuman/)

### Outlook/Apple Mail
- [Outlook Attachment Size Limit | SmartReach](https://smartreach.io/blog/outlook-attachment-size-limit/)
- [Manage email with rules in Outlook | Microsoft Support](https://support.microsoft.com/en-us/office/manage-email-messages-by-using-rules-in-outlook-c24f5dea-9465-4df4-ad17-a50704d66c59)
- [How To Search Apple Mail Effectively | Clean Email](https://clean.email/blog/email-providers/search-apple-mail)
- [Search for emails in Mail on Mac | Apple Support](https://support.apple.com/guide/mail/search-for-emails-mlhlp1003/mac)

### UX Best Practices
- [Autocomplete UX Best Practices | Fresh Consulting](https://www.freshconsulting.com/insights/blog/autocomplete-benefits-ux-best-practices/)
- [9 UX Design Patterns for Autocomplete | Baymard](https://baymard.com/blog/autocomplete-design)
- [Designing Swipe-to-Delete Interactions | LogRocket](https://blog.logrocket.com/ux-design/accessible-swipe-contextual-action-triggers/)
- [Mobile Navigation UX Best Practices (2026) | DesignStudio](https://www.designstudiouiux.com/blog/mobile-navigation-ux/)
- [Gesture Navigation in Mobile Apps | Sidekick Interactive](https://www.sidekickinteractive.com/designing-your-app/gesture-navigation-in-mobile-apps-best-practices/)

### Email Threading
- [Email Thread Best Practices | Missive](https://missiveapp.com/blog/email-thread)
- [What Is an Email Thread | Clean Email](https://clean.email/blog/email-etiquette/email-thread)
- [How to manage email threads | Superhuman Blog](https://blog.superhuman.com/email-thread/)

### Compliance & Security
- [List-Unsubscribe Header Guide | MailerLite](https://www.mailerlite.com/help/a-simple-guide-list-unsubscribe-header-and-one-click-unsubscribe)
- [What Is RFC 8058 | Mailgun](https://www.mailgun.com/blog/deliverability/what-is-rfc-8058/)
- [One-click Unsubscribe | Valimail](https://www.valimail.com/blog/one-click-unsubscribe/)
- [Email Security Features 2026 | Guardian Digital](https://guardiandigital.com/resources/blog/what-is-a-spam-filter-how-does-it-work)
- [AI-Powered Phishing Detection 2026 | USCS Institute](https://www.uscsinstitute.org/cybersecurity-insights/blog/ai-powered-phishing-detection-and-prevention-strategies-for-2026)
- [Microsoft Exchange Spam Filtering Update | Mailbird](https://www.getmailbird.com/microsoft-exchange-spam-filtering-update/)

### Email Automation
- [Create rules to filter emails | Gmail Help](https://support.google.com/mail/answer/6579?hl=en)
- [Guide to Automating Email Processing | Sobot](https://www.sobot.io/article/automate-email-processing-gmail-outlook-rules-filters-templates/)
- [Ways to use Outlook Rules and Gmail Filters | Kelly Nolan](https://kellynolan.com/ways-to-use-outlook-rules-and-or-gmail-filters-to-process-email-more-efficiently/)

### Productivity Features
- [Boomerang for Gmail](https://www.boomeranggmail.com/)
- [Snooze email or reminders | Google Workspace](https://support.google.com/a/users/answer/9308663?hl=en)
- [How to Use Outlook Snooze | Clean Email](https://clean.email/blog/email-providers/outlook-snooze-email-feature)
- [Time-Saving Email Habits for 2026 | Mailbird](https://www.getmailbird.com/time-saving-email-habits-master-inbox/)

### Industry Trends
- [Email Trends and Predictions for 2026 | Clean Email](https://clean.email/blog/insights/email-trends-and-predictions-2026)
- [Why Email Isn't Going Anywhere in 2026 | Hive](https://hive.com/blog/why-email-isnt-going-anywhere-2026/)

---

## 9. CONCLUSIONI

### Key Takeaways

1. **Search è CRITICO**: Gli utenti si aspettano Gmail-level search operators. Non negoziabile.

2. **Keyboard-First = Speed**: Superhuman insegna che velocity matters. 80+ shortcuts = power users.

3. **AI è il NEW NORMAL**: Smart Compose/Reply non sono più "premium features". Gmail li ha resi free (Gemini 3). Dobbiamo essere al passo.

4. **Mobile = Swipe Gestures**: Gli utenti si aspettano swipe customizzabili. No swipe = frustrazione.

5. **Security = Table Stakes**: Spam/phishing detection > 99.9% è lo standard. Compliance SPF/DKIM/DMARC obbligatoria.

6. **One-Click Unsubscribe è LAW**: Non opzionale. RFC 8058 enforcement attivo 2026.

### Raccomandazione Finale

**Per competere in 2026, Miracollook deve:**

✅ Parità funzionale con Gmail su search operators (Phase 1)
✅ Speed-first architecture (Superhuman inspiration)
✅ AI features baseline (Smart Compose/Reply) entro Phase 2
✅ Keyboard shortcuts completi (80+) per power users
✅ Mobile UX con swipe customizzabili

**Differenziazione:** Non reinventiamo la ruota. Studiamo cosa fanno i migliori, implementiamo con ECCELLENZA, e aggiungiamo il nostro twist unico (es: privacy-first AI, team collaboration, advanced analytics).

---

**Fine Report**

*"Non reinventiamo la ruota - studiamo chi l'ha già fatta!"*
*— Cervella Researcher, CervellaSwarm*
