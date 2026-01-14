# Thread View UX Research - Email Client Best Practices

**Data ricerca:** 14 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Progetto:** Miracollook (Miracollo v2.3.0)
**Obiettivo:** Analizzare come i migliori email client mostrano le conversazioni raggruppate (thread view)

---

## Executive Summary

Ho analizzato i 4 principali email client (Gmail, Superhuman, Apple Mail, Outlook) per capire come gestiscono la thread view. Ecco le **best practices comuni**:

1. **Visual Hierarchy** - Indentazione, colori, e indicatori visivi chiari
2. **Collapse/Expand Controls** - Chevron/Triangle icons per espandere thread
3. **Message Counter** - Badge numerico che mostra quanti messaggi nel thread
4. **Keyboard Navigation** - Shortcut per navigare velocemente tra messaggi
5. **AI Summaries** - Riassunti automatici per thread lunghi (trend 2026)

**Raccomandazione finale a fine documento.**

---

## 1. Gmail - Lo Standard di Mercato

### Thread View nella Lista (Collapsed)

**Visual Indicators:**
- **Message Counter**: Mostra numero messaggi tipo "(3)" accanto al subject
- **Expand Indicator**: Click su "x older messages" per espandere gruppo
- **Avatar**: Single avatar del mittente principale
- **Preview Text**: Snippet del messaggio più recente

**Comportamento di Default:**
- Thread collapsed di default nella inbox
- Newest message preview visible
- Click sul thread per aprirlo

### Thread View Espanso

**Layout:**
- Messaggi in ordine cronologico (vecchi in alto, nuovi in basso)
- Ogni messaggio può essere collapsed/expanded individualmente
- Header minimale con sender name + timestamp

**Expand/Collapse Controls:**
- **Icon**: Expand/collapse icon in alto a destra
- **Keyboard**: `;` per expand all, `:` (shift+;) per collapse all
- **Click behavior**: Click su singolo messaggio per expand/collapse

**Nuove Feature 2026 (AI-Powered):**
- **AI Overview Card**: Riassunto automatico thread lunghi (apparso inizio 2026)
- **AI Summaries**: Sintesi key points in conversazioni con molte reply
- **Suggested Replies**: Risposte contestuali che matchano lo stile
- **Personalized AI Inbox**: View opzionale con "Suggested to-dos" e "Topics to catch up on"

### Keyboard Shortcuts
- `;` = Expand all messages in thread
- `:` = Collapse all messages
- `j/k` = Next/previous conversation
- `o` = Open conversation

**Fonti:**
- [Gmail Gemini Era Features](https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/)
- [Gmail Thread Feature - Medium](https://medium.com/@bindu.mohile/gmails-email-threading-feature-5e5676d7cf24)
- [Understanding Gmail Conversation View](https://it.stonybrook.edu/help/kb/understanding-conversation-view-in-google-mail)

---

## 2. Superhuman - The Speed Champion

### Philosophy

**Conversation View Only** - Non c'è opzione per disattivare threading. Superhuman enforce thread view sempre.

### Thread View Design

**Minimal UI:**
- Full message displayed chiaramente formatted
- Stripped of header clutter - appare come "typed business letter"
- Focus on readability e speed

**Split Inbox Feature:**
- Categorizza mail per tipo (bills, team, notifications)
- Reduce context switching costs
- Ogni categoria è una view separata

**Inline Comments:**
- Team può "commentare" direttamente nel thread
- Cleaner than forwarding
- Chi commenta vede automaticamente nuove reply

### Keyboard Navigation (Il Cuore di Superhuman)

Superhuman è **keyboard-first**. 105 shortcuts totali!

**Core Thread Shortcuts:**
- `e` = Archive
- `l` = Label
- `h` = Snooze
- `/` = Search
- `shift+/` = AI-powered search
- `cmd+k` = Command palette (command center)
- `j/k` = Navigate messages

**Design Philosophy:**
- "Dozens of emails in few minutes without touching mouse"
- Command bar per ogni azione
- Predefined keystrokes per archive, delete, snooze

### Inbox Zero Enforcement

- Archived emails hidden unless reply or snoozed back
- Inbox = Task list, non read/unread status
- Systematic approach: action-based organization

**Fonti:**
- [Superhuman Keyboard Shortcuts PDF](https://download.superhuman.com/Superhuman%20Keyboard%20Shortcuts.pdf)
- [How to Use Superhuman](https://writing.arman.do/p/superhuman)
- [Superhuman Shortcuts Guide](https://nickgray.net/superhuman/)

---

## 3. Apple Mail - The Problematic One

### Conversation View Toggle

**Settings:**
- Menu: View > Organize by Conversation (checkmark = ON)
- Ogni mailbox può avere setting separato
- Si può disattivare globally o per mailbox

### Thread View Collapsed

**Visual Indicator:**
- **Message count** nel top message header
- Click sul count per expand conversation

### Thread View Espanso

**Layout Options:**
- Setting: "Show most recent message at the top" (toggle)
- Default: chronological order (oldest first)
- Can include related messages from other mailboxes

**Expand Controls:**
- Click message count in top message
- View > Expand All Conversations (per tutti i thread)

### UX Problems Reportati dagli Utenti

⚠️ Apple Mail ha **problemi noti** con thread view:

1. **Incorrect Grouping** - Thread non correlati vengono raggruppati insieme
2. **Setting Persistence** - "Organize by Conversation" si riattiva random
3. **Missed Emails** - Email nascoste dentro conversation di altro thread
4. **Poor Matching Logic** - Subject line matching troppo aggressivo

**User Sentiment:** Molto negativo. Tanti user disattivano la feature.

**Fonti:**
- [Apple Mail Conversation View Support](https://support.apple.com/guide/mail/view-email-conversations-mail35700/mac)
- [MacRumors Forum - Conversation Issues](https://forums.macrumors.com/threads/apple-mail-keeps-reselecting-organize-by-conversation-and-im-sick-of-it.2327001/)
- [How to Work with Conversations](https://www.idownloadblog.com/2020/02/20/conversations-in-mail-mac/)

---

## 4. Outlook - The Enterprise Choice

### Conversation View Settings

**Enable/Disable:**
- View tab > Messages group > "Show as Conversations"
- Settings > Mail > Layout > "Group messages by conversations"
- Default: **ON** in modern versions (Microsoft 365, Outlook 2024-2016)

### Thread View nella Lista

**Visual Indicator:**
- **Triangle icon** (small) accanto a thread con multiple messages
- White triangle = collapsed
- Black down-pointing triangle = expanded
- Double chevron mark = email part of thread

**Behavior:**
- Click triangle to expand/collapse
- Tapping double chevron opens full thread

### Thread View Espanso

**Layout:**
- All messages with same subject grouped
- Reading pane shows message order:
  - **Newest on top** = most recent first
  - **Newest on bottom** = chronological order

**Navigation:**
- Small arrows close to threaded emails
- Click arrows to reveal all grouped messages

### Clean Up Conversations

**Feature unica di Outlook:**
- "Clean Up Conversations" tool
- Remove redundant messages (già citati in reply successive)
- Mantiene solo last message con full history

**Fonti:**
- [Outlook Conversation View - Microsoft Support](https://support.microsoft.com/en-us/office/view-email-messages-by-conversation-in-outlook-0eeec76c-f59b-4834-98e6-05cfdfa9fb07)
- [Outlook Conversation View Guide](https://www.ablebits.com/office-addins-blog/outlook-conversation-view/)
- [Organize Outlook by Thread](https://www.wisestamp.com/blog/organize-outlook-by-thread/)

---

## Cross-Client Best Practices Analysis

### 1. Visual Indicators Comuni

| Indicatore | Gmail | Superhuman | Apple Mail | Outlook |
|-----------|-------|------------|------------|---------|
| **Message Counter** | ✅ (3) | ❌ Minimal | ✅ Count | ✅ Number |
| **Chevron/Triangle** | ✅ Link text | ❌ | ✅ Count click | ✅ Triangle icon |
| **Avatar** | ✅ Single | ✅ Clean | ✅ Single | ✅ Single |
| **Preview Text** | ✅ Latest | ✅ Formatted | ✅ Latest | ✅ Latest |

**Pattern Comune:** Tutti mostrano un indicatore numerico o visuale per thread con multiple messages.

### 2. Expand/Collapse Patterns

| Pattern | Implementato da |
|---------|-----------------|
| **Click on counter/icon** | Gmail, Apple Mail, Outlook |
| **Keyboard shortcuts** | Gmail, Superhuman |
| **Expand all/Collapse all** | Gmail, Apple Mail |
| **Individual message expand** | Gmail |
| **Triangle icon toggle** | Outlook |

**Best Practice:** Offrire **multiple ways** per expand/collapse:
- Click visual indicator
- Keyboard shortcut
- Bulk actions (expand all/collapse all)

### 3. Keyboard Navigation

| Client | Shortcuts | Philosophy |
|--------|-----------|-----------|
| **Gmail** | 10+ shortcuts | Optional, helpful |
| **Superhuman** | 105 shortcuts | **Core feature**, required for speed |
| **Apple Mail** | Basic | Secondary |
| **Outlook** | Standard | Standard office suite |

**Best Practice:** Keyboard navigation è **essenziale** per power users.
- `j/k` per navigate = de facto standard
- `;/:` per expand/collapse = Gmail convention
- `cmd+k` command palette = modern pattern

### 4. Thread Grouping Logic

**Come viene determinato che email appartengono allo stesso thread?**

| Client | Matching Logic |
|--------|---------------|
| **Gmail** | Subject + References/In-Reply-To headers |
| **Outlook** | Same subject line |
| **Apple Mail** | Subject + headers (problematic!) |
| **Superhuman** | Standard email threading (References header) |

⚠️ **Problema comune:** Subject-only matching crea **false positives** (es: "Re: Thanks" raggruppa thread non correlati).

**Best Practice:** Usare **email headers** (Message-ID, In-Reply-To, References) per threading accurato, non solo subject.

### 5. Message Order in Expanded Thread

**Due approcci principali:**

1. **Chronological (Oldest First)** - Gmail, Apple Mail default
   - PRO: Natural conversation flow
   - CONTRO: Scroll to see latest

2. **Newest First** - Outlook option, Apple Mail option
   - PRO: Latest message immediately visible
   - CONTRO: Reverse conversation flow

**Best Practice:** Offrire **user choice** con default = **Newest First** per inbox triage rapida.

---

## UI/UX Design Principles da Ricerca

### Principi Fondamentali (da Housing Arizona Study)

1. **Clear Conversation Hierarchy**
   - Visual organization (indentation, color-coding)
   - Help users follow discussion flow
   - Reduce cognitive burden

2. **Easy-to-Use Navigation**
   - Intuitive controls
   - Keyboard shortcuts
   - Navigation aids for rapid movement

3. **Contextual Information**
   - Sender names visible
   - Timestamps clear
   - Support appropriate responses

**Research Finding:** "American Psychological Association study found that cluttered and disorganized email interfaces lead to increased stress and decreased productivity."

### Avatar Stacking Pattern (Multi-Participant Threads)

**Design System Examples:** Primer (GitHub), Atlassian, Procore

**Pattern:**
- Display multiple avatars overlapped
- Active users grouped at top
- Inactive users at bottom
- Overflow indicator ("+3") for many participants
- Hover reveal: name popover + avatar shifts above stack

**Interactive Behavior:**
- Hover = popover with name
- Active/inactive grouping
- Max visible: 3-4 avatars + overflow
- "View All" link for complete list

**Best Practice for Miracollook:** Se thread ha multiple participants, mostra **stacked avatars** invece di single avatar.

### Expand/Collapse UI Patterns

**Icon Choices:**
- **Chevron** (>, <, ∨, ∧) - Most common
- **Plus/Minus** (+, -) - Alternative
- **Triangle** (▸, ▾) - Outlook style
- **Caret** (^, v) - Minimal style

**Animation Best Practices:**
- Smooth transitions (200-300ms)
- Icon rotation on toggle
- Content fade-in on expand
- Height animation for smooth reveal

**Accessibility:**
- Sufficient color contrast
- Clear hover/focus states
- Screen reader labels
- Keyboard accessible

---

## Thread Management Best Practices (Missive/Industry)

### Per UI Design

1. **Chronological Organization** - First to most recent, easy tracking
2. **Internal/External Separation** - Visual distinction (prevent accidental external share)
3. **Assignment Visualization** - Visual indicators for task assignment
4. **One-Click Actions** - Move email to separate conversation if needed

### Per User Behavior (influisce sul design)

1. **Clear Subject Lines** - UI deve show subject prominently
2. **Stay On Topic** - Threading logic deve essere accurato
3. **Selective Participants** - Show who's in conversation clearly
4. **Reference Context** - Quote/reply indicators visible

### Problemi da Evitare

❌ **Irrelevant Recipients** - When using reply-all
❌ **Buried Messages** - Deep nesting hard to find
❌ **Subject Drift** - Thread diverts to new topic but same subject
❌ **Confidential Mixing** - Sensitive info in group thread

---

## Visual Design Specifications

### Message Counter Badge

**Not found official Gmail specs**, ma da osservazione:

- **Position:** Right side of subject line or after sender name
- **Format:** "(N)" in parentheses or pill badge with number
- **Color:** Usually muted (gray) or primary brand color
- **Size:** Small, non-intrusive but readable
- **Behavior:** Clickable to expand

### Triangle/Chevron Icon

**Specifications from search:**

**Outlook Style:**
- White triangle when collapsed (▷)
- Black down-pointing triangle when expanded (▼)
- Small size (12-16px typically)
- Position: Left of message/subject

**Technical Implementation:**
- Chevron: Two visible borders on rotated square (outline style)
- Triangle: Solid filled using CSS border technique
- Animation: Rotate 90° on toggle (0.2s ease)

### Thread Row Height

**Not specific data found**, but common patterns:

- **Collapsed thread:** Same height as single email (~60-80px)
- **Expanded thread:** Dynamic height based on content
- **Individual messages:** ~40-60px per message header in expanded view

### Color Coding

**Gmail approach:**
- Unread: Bold text + subtle background
- Read: Normal weight text
- Important: Star/marker icon
- Labels: Color-coded pills

**Superhuman approach:**
- Minimal color use
- Focus on typography and whitespace
- Split inbox uses subtle background colors per category

---

## 2026 AI Trend - Thread Summarization

### Gmail Leading the Way

**New in January 2026:**
- AI Overview card at top of long threads
- Bulleted summary of key points
- Natural language Q&A about thread
- Free for all users (powered by Gemini 3)

**UX Impact:**
- Reduce time to understand context
- Avoid reading dozens of messages
- Quick catch-up on long conversations

### Design Implications for Miracollook

**Consideration:** Se implementiamo AI features in futuro, thread view è **perfect spot** per:
- Summary card at top
- Key action items extraction
- Participant involvement breakdown
- Sentiment analysis

**But:** Start with solid basic thread view first! AI is enhancement, not foundation.

---

## Raccomandazione per Miracollook Thread View

### Core Features (Must Have)

1. **Visual Thread Indicator**
   - Message counter badge tipo "(3)"
   - Position: Right of subject line
   - Show in collapsed state in lista eventi

2. **Expand/Collapse Control**
   - Chevron icon (∨) preferibile a triangle
   - Click anywhere on thread row to expand
   - Individual messages collapsible when expanded
   - Keyboard: `;` expand all, `:` collapse all

3. **Thread View Espanso**
   - Chronological order (newest at bottom - natural flow)
   - Option to toggle "newest first"
   - Each message shows:
     - Avatar + Name
     - Timestamp
     - Message content (full or preview)
     - Action buttons (Reply, Forward, etc)

4. **Keyboard Navigation**
   - `j/k` for navigate between threads
   - `;/:` for expand/collapse
   - `Enter` to open thread
   - `Esc` to close thread

5. **Avatar Handling**
   - Single avatar if 1-2 participants
   - Stacked avatars if 3+ participants (max 3 visible + overflow)
   - Hover for participant list popover

### Nice to Have (Phase 2)

1. **Thread Summary** (se aggiungiamo AI)
   - Card at top with key points
   - Participant activity summary
   - Action items extraction

2. **Smart Grouping**
   - Use email headers (In-Reply-To, References) not just subject
   - Avoid Apple Mail mistake of over-aggressive grouping

3. **Thread Actions**
   - "Clean up thread" (remove redundant messages)
   - "Split thread" (if conversation diverges)
   - "Merge threads" (if related but separate)

### Design Specs Suggeriti

**Collapsed Thread Row:**
```
[Avatar/Stack] [Subject] [(N)]         [Date] [Actions]
               [Preview text...]

Height: 72px (same as single event)
Counter: Gray pill badge, 16px height, "(N)" format
Chevron: 16px, right side or left of counter
```

**Expanded Thread:**
```
Thread Header
├─ [Subject]
├─ [N messages, N participants]
├─ [Expand All | Collapse All]

Message 1 (Collapsed)
├─ [Avatar] [Name] [Date]
├─ [Preview line...]
└─ [Click to expand]

Message 2 (Expanded)
├─ [Avatar] [Name] [Date]
├─ [Full message content]
└─ [Reply] [Forward] [Actions]

...
```

**Keyboard Shortcuts Mapping:**
```javascript
const THREAD_SHORTCUTS = {
  'j': 'nextThread',
  'k': 'previousThread',
  ';': 'expandAllMessages',
  ':': 'collapseAllMessages',
  'Enter': 'openThread',
  'Escape': 'closeThread',
  'r': 'reply',
  'f': 'forward'
}
```

### Architecture Considerations

**Threading Logic:**
- Use email `Message-ID`, `In-Reply-To`, `References` headers
- Fallback to subject matching ONLY if headers missing
- Subject matching: normalize (remove "Re:", "Fwd:", extra spaces)
- Group by conversation ID (generated from headers)

**Performance:**
- Lazy load thread messages (don't load all on inbox open)
- Expand thread → fetch full messages
- Cache expanded threads for session
- Virtualize long thread lists

**State Management:**
```typescript
interface ThreadState {
  threadId: string;
  isExpanded: boolean;
  messages: Message[];
  participants: Participant[];
  messageCount: number;
  expandedMessageIds: string[];
}
```

---

## Competitor Comparison Matrix

| Feature | Gmail | Superhuman | Apple Mail | Outlook | **Miracollook** |
|---------|-------|------------|------------|---------|-----------------|
| **Default View** | Threaded | Threaded only | Optional | Threaded | **Threaded** ✅ |
| **Message Counter** | ✅ (3) | ❌ | ✅ | ✅ | **✅ (N)** |
| **Expand Icon** | ✅ Link | ❌ | ✅ Count | ✅ Triangle | **✅ Chevron** |
| **Keyboard Nav** | ✅ Good | ✅ Excellent | ❌ Basic | ✅ Standard | **✅ Standard** |
| **AI Summary** | ✅ 2026 | ✅ AI search | ❌ | ❌ | *Phase 2* |
| **Avatar Stack** | ❌ Single | ❌ | ❌ | ❌ | **✅ Multi** |
| **Split View** | ❌ | ✅ Categories | ❌ | ❌ | *Consider* |
| **Threading Logic** | ✅ Headers | ✅ Standard | ⚠️ Buggy | ⚠️ Subject only | **✅ Headers** |
| **Expand All** | ✅ | ❌ | ✅ | ❌ | **✅** |
| **Message Order** | ⬆️ Old→New | ⬆️ | ⚙️ Toggle | ⚙️ Toggle | **⚙️ Toggle** |

**Miracollook Target:** Combinare best of Gmail (solid threading) + Superhuman (keyboard speed) + unique multi-avatar design.

---

## Technical Implementation Notes

### Email Header Analysis for Threading

**Standard email headers per threading:**

```
Message-ID: <unique-id@domain.com>
In-Reply-To: <parent-message-id@domain.com>
References: <thread-root@domain.com> <parent@domain.com>
```

**Threading Algorithm:**
1. Check if `In-Reply-To` or `References` present
2. If yes: Group by conversation based on headers
3. If no: Fallback to normalized subject matching
4. Store conversation ID for future messages

**Subject Normalization:**
```javascript
function normalizeSubject(subject) {
  return subject
    .replace(/^(Re:|Fwd:|Fw:)\s*/gi, '')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}
```

### Database Schema Suggestion

```sql
-- Thread/Conversation table
CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  subject TEXT NOT NULL,
  normalized_subject TEXT,
  message_count INTEGER DEFAULT 1,
  participant_count INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Messages linked to conversation
CREATE TABLE messages (
  id UUID PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id),
  message_id TEXT UNIQUE, -- Email Message-ID header
  in_reply_to TEXT, -- In-Reply-To header
  references TEXT[], -- References header (array)
  -- ... other message fields
);

-- Index for fast threading queries
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_references ON messages USING GIN(references);
```

### UI Component Structure

```typescript
// Thread List Item Component
<ThreadListItem
  thread={thread}
  collapsed={!expandedThreads.includes(thread.id)}
  onExpand={() => handleExpandThread(thread.id)}
  onCollapse={() => handleCollapseThread(thread.id)}
  showAvatarStack={thread.participantCount > 2}
  messagePreview={thread.latestMessage.preview}
/>

// Expanded Thread View Component
<ThreadView
  threadId={threadId}
  messages={messages}
  expandedMessages={expandedMessageIds}
  onExpandMessage={(id) => toggleMessage(id)}
  onExpandAll={() => expandAllMessages()}
  onCollapseAll={() => collapseAllMessages()}
  participants={participants}
/>
```

---

## Key Learnings Summary

### ✅ DO - Best Practices

1. **Use email headers** for threading (Message-ID, References) - not just subject
2. **Show message counter** prominently when thread has multiple messages
3. **Provide keyboard shortcuts** - essential for power users (`j/k`, `;/:`)
4. **Offer expand/collapse** at both thread level and individual message level
5. **Stack avatars** when multiple participants (max 3 visible + overflow)
6. **Keep UI minimal** in collapsed state - show only essential info
7. **Animate transitions** smoothly (200-300ms) for expand/collapse
8. **Allow message order toggle** - newest first vs chronological
9. **Make entire row clickable** for expand (not just small icon)
10. **Cache expanded state** during session for better UX

### ❌ DON'T - Anti-Patterns

1. **Don't use subject-only matching** - creates false positives (Apple Mail mistake)
2. **Don't hide the expand control** - make it obvious (unlike Superhuman's minimal approach)
3. **Don't over-nest** - keep visual hierarchy max 2-3 levels
4. **Don't auto-expand all** on inbox load - performance killer
5. **Don't force thread view** - let users toggle if they want (unlike Superhuman)
6. **Don't show all participants inline** - use avatar stack with overflow
7. **Don't ignore keyboard users** - shortcuts are critical
8. **Don't make expand icon too small** - minimum 16px touch target
9. **Don't forget loading states** - lazy loading needs spinners
10. **Don't mix unrelated threads** - accuracy over aggressive grouping

---

## Next Steps per Implementazione

### Phase 1 - Basic Thread View (MVP)
1. Implement threading logic using email headers
2. Add message counter badge to thread rows
3. Chevron icon + click to expand/collapse
4. Expanded view: chronological message list
5. Basic keyboard shortcuts (j/k, Enter, Esc)

### Phase 2 - Enhanced Navigation
1. Individual message collapse in expanded thread
2. Expand all / Collapse all buttons
3. Full keyboard shortcut suite (`;/:`, `r`, `f`)
4. Message order toggle (newest first option)
5. Thread action menu (split, merge, clean)

### Phase 3 - Visual Polish
1. Avatar stacking for multi-participant threads
2. Smooth animations for expand/collapse
3. Hover states and tooltips
4. Loading skeletons for lazy-loaded messages
5. Accessibility improvements (ARIA labels, focus management)

### Phase 4 - Advanced Features (Future)
1. AI thread summarization
2. Smart grouping improvements
3. Thread insights (participant activity, sentiment)
4. Thread search within conversation
5. Inline reply/compose

---

## Fonti Complete

### Gmail
- [Gmail Gemini Era Features](https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/)
- [Gmail AI Features Free](https://www.macrumors.com/2026/01/08/gmail-ai-features-now-free-to-use/)
- [Gmail Thread Feature - Medium](https://medium.com/@bindu.mohile/gmails-email-threading-feature-5e5676d7cf24)
- [Gmail Conversation View Benefits](https://support.cloudhq.net/what-are-the-benefits-of-gmail-conversation-view-being-turned-on-or-off/)
- [Understanding Gmail Conversation View](https://it.stonybrook.edu/help/kb/understanding-conversation-view-in-google-mail)
- [Gmail Expand All Feature](https://internetmarketingteam.com/gmails-expand-all-feature-can-help-you-find-messages-quickly/)

### Superhuman
- [Superhuman Keyboard Shortcuts PDF](https://download.superhuman.com/Superhuman%20Keyboard%20Shortcuts.pdf)
- [How to Use Superhuman](https://writing.arman.do/p/superhuman)
- [Superhuman Shortcuts Guide](https://nickgray.net/superhuman/)
- [Superhuman Email Guide Part II](https://bakerontech.com/superhuman-email-a-refreshing-new-way-to-deal-with-email-part-ii/)
- [Superhuman AI Email Management](https://blog.superhuman.com/the-best-ai-email-management-tool/)

### Apple Mail
- [Apple Mail Conversation View Support](https://support.apple.com/guide/mail/view-email-conversations-mail35700/mac)
- [MacRumors Forum - Conversation Issues](https://forums.macrumors.com/threads/apple-mail-keeps-reselecting-organize-by-conversation-and-im-sick-of-it.2327001/)
- [How to Organize Threads - iGeeksBlog](https://www.igeeksblog.com/how-to-organize-threads-in-mail-app-on-iphone-ipad/)
- [How to Work with Conversations](https://www.idownloadblog.com/2020/02/20/conversations-in-mail-mac/)
- [How to Stop Threading](https://www.thewebernets.com/2011/11/09/how-to-stop-osx-mac-mail-threadinggrouping-emails-and-conversations-together/)

### Outlook
- [Outlook Conversation View - Microsoft Support](https://support.microsoft.com/en-us/office/view-email-messages-by-conversation-in-outlook-0eeec76c-f59b-4834-98e6-05cfdfa9fb07)
- [Outlook Conversation View Guide](https://www.ablebits.com/office-addins-blog/outlook-conversation-view/)
- [Organize Outlook by Thread](https://www.wisestamp.com/blog/organize-outlook-by-thread/)
- [How to View All Messages as Conversation](https://lookeen.com/blog/how-to-view-all-messages-as-conversation-in-outlook)
- [Clean Up Conversations](https://finance.uw.edu/recmgt/resources/clean-conversations-outlook)

### UX Research & Best Practices
- [Email Threading UI Design - Housing Innovations](https://dev.housing.arizona.edu/email-threading-ui)
- [Email Thread Best Practices - Missive](https://missiveapp.com/blog/email-thread)
- [Email Thread Best Practices - Mailercloud](https://www.mailercloud.com/blog/email-thread)
- [Email Threading Best Practices - Mailmodo](https://www.mailmodo.com/guides/email-thread/)
- [Email Thread Best Practices - Zoho](https://www.zoho.com/blog/mail/email-thread-best-practices.html)
- [Email Threads - Hiver](https://hiverhq.com/blog/email-thread)

### Visual Design Patterns
- [Email Thread Visualization - Relativity](https://help.relativity.com/RelativityOne/Content/Relativity/Analytics/Email_thread_visualization.htm)
- [Thread Arcs Research](https://www.researchgate.net/publication/221005997_Thread_arcs_An_email_thread_visualization)
- [Expand/Collapse UI Design](https://pixso.net/expand-collapse-ui-design/)
- [Avatar Stack - Primer](https://primer.style/design/components/avatar-stack/)
- [Avatar Stack - Procore](https://design.procore.com/avatar-stack)
- [Avatar Group - Atlassian](https://atlassian.design/components/avatar-group/)
- [Mastering Stacking Contexts CSS](https://medium.com/@nahidswe/mastering-stacking-contexts-in-css-a-stacked-avatar-case-study-80c8d23789ec)

### Visual Indicators
- [Gmail Arrow Indicators](https://gmail.googleblog.com/2008/03/arrow-indicators-reveal-who-actually.html)
- [Outlook Triangle Explanation](https://learn.microsoft.com/en-us/answers/questions/4522039/triangle-next-to-mails)
- [Email Thread Visual Indicators](https://help.relativity.com/10.3/Content/Relativity/Analytics/Email_thread_visualization.htm)

---

## Conclusione

I migliori email client convergono su **pattern comuni** per thread view:

1. **Visual hierarchy** chiara con counter e chevron
2. **Keyboard shortcuts** per power users
3. **Expand/collapse** a multiple livelli
4. **Header-based threading** (non solo subject!)
5. **AI enhancement** sta arrivando (2026 trend)

**Per Miracollook**, raccomando di:
- Partire con solid MVP (counter, chevron, expand/collapse)
- Focus on keyboard navigation (differenziatore)
- Usare avatar stacking (unique feature)
- Lasciare spazio per AI features future

**La mia raccomandazione forte:** NON copiare Apple Mail! Il loro threading è problematico. Seguire approccio Gmail (accurato) + keyboard shortcuts Superhuman (veloce) + avatar stack innovativo.

---

*Fine ricerca. Pronta per domande o next steps!* 🔬
