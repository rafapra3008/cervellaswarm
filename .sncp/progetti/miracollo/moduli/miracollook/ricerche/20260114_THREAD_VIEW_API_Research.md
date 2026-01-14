# Gmail API Thread Management - Ricerca Tecnica

**Data**: 14 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Obiettivo**: Implementare Thread View in Miracollook

---

## Executive Summary

Gmail API gestisce i thread come **conversazioni** che raggruppano messaggi correlati. La chiave è:
- **threadId** univoco per utente che raggruppa messaggi
- `threads.list()` per ottenere lista thread
- `threads.get()` per espandere un singolo thread con tutti i messaggi
- **historyId** per caching incrementale
- **Format options** per ottimizzare le richieste (minimal/metadata/full)

---

## 1. Come Gmail Organizza i Thread

### Concetto Base

> *"The Gmail API uses Thread resources to group email replies with their original message into a single conversation or thread, allowing you to retrieve all messages in a conversation in order."*

**Thread = Conversazione**
- 1 Thread contiene N Messaggi (ordinati cronologicamente)
- Thread non si creano manualmente via API
- Thread si creano automaticamente quando un messaggio rispetta criteri RFC 2822

### Criteri per Appartenenza a Thread

Per aggiungere un messaggio a un thread esistente:
1. `threadId` deve essere specificato nel Message object
2. Headers `References` e `In-Reply-To` devono essere RFC 2822 compliant
3. Header `Subject` deve matchare (stesso subject = stesso thread)

### Thread ID: User-Specific

⚠️ **IMPORTANTE**: Thread ID è user-specific!
- Lo stesso thread ha ID diverso per mittente/destinatario
- Ogni utente ha il suo thread ID per la stessa conversazione

---

## 2. API Endpoints

### A. `threads.list` - Lista Thread

**Endpoint:**
```
GET https://gmail.googleapis.com/gmail/v1/users/{userId}/threads
```

**Scopo:** Ottenere lista di thread IDs (come inbox list)

**Query Parameters:**
- `q` - Query string (stessi filtri di messages.list)
- `maxResults` - Numero risultati per pagina
- `pageToken` - Paginazione
- `labelIds` - Filtra per label (es. INBOX, SENT)

**Response Minimal:**
```json
{
  "threads": [
    {
      "id": "thread_id_123",
      "snippet": "Breve preview del thread...",
      "historyId": "12345"
    }
  ],
  "nextPageToken": "...",
  "resultSizeEstimate": 42
}
```

**⚠️ NOTA IMPORTANTE:**
> "Each thread resource from threads.list does NOT contain a list of messages - the list of messages for a given thread can be fetched using the threads.get method."

threads.list NON restituisce i messaggi! Solo metadati del thread.

### B. `threads.get` - Espandi Thread

**Endpoint:**
```
GET https://gmail.googleapis.com/gmail/v1/users/{userId}/threads/{id}
```

**Scopo:** Ottenere TUTTI i messaggi di un thread specifico

**Query Parameters:**

| Parameter | Tipo | Descrizione |
|-----------|------|-------------|
| `format` | enum | minimal, metadata, full (vedi sotto) |
| `metadataHeaders[]` | string | Se format=metadata, quali headers includere |

**Format Options:**

1. **minimal**
   - Solo message IDs e labels
   - NON restituisce headers, body, payload
   - Usa quando: Serve solo sapere quanti messaggi ci sono

2. **metadata**
   - Message IDs, labels, e headers selezionati
   - NON restituisce body content
   - Usa quando: Serve subject, from, date ma non body

3. **full** (DEFAULT)
   - Tutto: headers, body parsed nel payload
   - Field `raw` NON usato
   - Usa quando: Serve visualizzare il contenuto

**Response Structure (format=full):**
```json
{
  "id": "thread_id_123",
  "snippet": "Preview del thread...",
  "historyId": "12345",
  "messages": [
    {
      "id": "msg_1",
      "threadId": "thread_id_123",
      "labelIds": ["INBOX", "UNREAD"],
      "snippet": "Preview messaggio...",
      "historyId": "12340",
      "internalDate": "1705234567890",
      "payload": {
        "headers": [
          {"name": "Subject", "value": "Re: Discussione"},
          {"name": "From", "value": "sender@example.com"},
          {"name": "Date", "value": "..."}
        ],
        "body": {
          "size": 1234,
          "data": "base64_encoded_content"
        }
      }
    },
    {
      "id": "msg_2",
      "threadId": "thread_id_123",
      ...
    }
  ]
}
```

---

## 3. Struttura Dati Thread

### Thread Object

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | string | Thread ID univoco (user-specific) |
| `snippet` | string | Preview breve del thread (da ultimo msg) |
| `historyId` | string | ID dell'ultimo cambio al thread |
| `messages` | array | Lista di Message objects (ordinati) |

### Message Object (dentro Thread)

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | string | Message ID univoco |
| `threadId` | string | Thread di appartenenza |
| `labelIds` | array | Labels applicate (INBOX, SENT, ecc.) |
| `snippet` | string | Preview del singolo messaggio |
| `historyId` | string | ID cambio specifico a questo msg |
| `internalDate` | string | Timestamp (epoch ms) per ordinamento |
| `payload` | object | Headers + Body parsed (se format=full) |

---

## 4. Caching e Sincronizzazione

### historyId - Il Cuore del Caching

**Cos'è historyId:**
- Numero che cresce cronologicamente (NON contiguo, ha gaps)
- Identifica un "punto nel tempo" della mailbox
- Validità: minimo 1 settimana, massimo poche ore (raro)

### Strategia: Full Sync vs Partial Sync

#### Full Synchronization

**Quando:**
- Prima connessione dell'utente
- Errore HTTP 404 su partial sync (historyId troppo vecchio)

**Come:**
1. Chiama `threads.list` (o `messages.list`) per ottenere IDs
2. Usa `format=full` su `threads.get` per caching completo
3. **SALVA** il `historyId` del messaggio più recente (primo in lista)
4. Questo historyId sarà il `startHistoryId` per future partial sync

#### Partial Synchronization (Incremental)

**Quando:**
- Aggiornamenti dopo first sync
- Intervalli regolari (polling) o push notification

**Come:**
1. Chiama `history.list` con `startHistoryId` salvato
2. Ottieni solo i **cambiamenti** da quel punto
3. Response contiene:
   - `messagesAdded` - Nuovi messaggi
   - `messagesDeleted` - Messaggi cancellati
   - `labelsAdded` / `labelsRemoved` - Cambi label
4. **AGGIORNA** cache locale solo per quei messaggi
5. Usa `format=minimal` se hai già cached il contenuto (solo labels cambiano)
6. **SALVA** nuovo `historyId` per prossima sync

**Vantaggi Partial Sync:**
- Molto più leggera (solo delta changes)
- Risparmio banda e API quota
- Più veloce per utente

### Error Handling

**HTTP 404 su partial sync:**
```
historyId troppo vecchio o invalido
→ Fallback a Full Sync
→ Riprova con nuovo historyId
```

**Best Practice:**
- Catchare 404
- Log per monitoraggio frequenza
- Full sync automatico come fallback

### Caching Best Practices

| Scenario | Format | Perché |
|----------|--------|--------|
| First load | `full` | Serve tutto, cache completo |
| Update labels | `minimal` | Hai già body cached, serve solo labelIds |
| Espandi thread | Leggi da cache | Evita API call se già hai full |
| Nuovo messaggio | `full` | Devi cacharlo completo |

---

## 5. Thread Expansion - UI Pattern

### Come Funziona Gmail UI

**Collapsed View (Default):**
- Mostra solo l'ultimo messaggio del thread
- Snippet indica "3 older messages"
- Click per espandere

**Expanded View:**
- Mostra tutti i messaggi in ordine cronologico
- Ogni messaggio collapsable individualmente
- Bottone "Expand all" / "Collapse all"

### Implementazione per Miracollook

**Opzione 1: Lazy Loading (Raccomandato)**
```
1. threads.list → mostra lista thread con snippet
2. User click su thread → threads.get(format=metadata)
3. Mostra headers (Subject, From, Date) di tutti messaggi
4. User click su singolo messaggio → fetch body (o da cache)
```

**Opzione 2: Eager Loading**
```
1. threads.list → mostra lista thread
2. User click → threads.get(format=full)
3. Carica TUTTO subito
4. Mostra tutto espanso (o collassato con toggle)
```

**Opzione 3: Hybrid (Intelligente)**
```
1. threads.list → snippet
2. Se thread ha 1-2 messaggi → format=full (piccolo)
3. Se thread ha 3+ messaggi → format=metadata, lazy body
4. Balance tra UX e performance
```

### Pattern UI Consigliato

```
ThreadList Component
├── ThreadItem (collapsed)
│   ├── Subject
│   ├── Participants (count)
│   ├── Snippet (last message)
│   ├── Message count badge (es: "5")
│   └── Click → Espandi
│
└── ThreadExpanded
    ├── Message 1 (collapsed)
    │   ├── From, Date
    │   └── Click → Show body
    ├── Message 2 (collapsed)
    ├── Message 3 (expanded) ← ultimo/selezionato
    │   ├── Full headers
    │   └── Full body
    └── "Show all" / "Collapse all" button
```

---

## 6. Query e Filtering

### Thread Filtering

**⚠️ IMPORTANTE:**
> "If any message in a thread matches the query, that thread is returned in the result."

Thread supporta gli stessi filtri di messages.list!

**Esempi:**
```
q=from:john@example.com     → Thread con almeno 1 msg da John
q=subject:invoice           → Thread il cui subject contiene "invoice"
q=is:unread                 → Thread con almeno 1 msg unread
q=label:important           → Thread con label IMPORTANT
```

### Combinare Filtri

```
threads.list?q=is:unread label:INBOX&maxResults=50
→ Primi 50 thread unread nella inbox
```

---

## 7. Performance e Best Practices

### Do's ✅

1. **Usa Batch Requests**
   - Se devi fare threads.get su 10 thread → batch request
   - Risparmio latenza e quota

2. **Cache Aggressivo**
   - Format=full alla prima fetch
   - Partial sync per aggiornamenti
   - Evita re-fetch di body se non necessario

3. **Format Appropriato**
   - Lista thread → non serve nemmeno chiamare threads.get
   - Preview → format=metadata
   - Full view → format=full (solo quando serve)

4. **historyId Strategy**
   - Salva SEMPRE dopo ogni sync
   - Usa partial sync come default
   - Fallback graceful a full sync su errori

5. **Push Notifications**
   - Combina con partial sync
   - Update in real-time solo quando serve
   - Evita polling continuo

### Don'ts ❌

1. **Non usare threads.get per ogni thread in lista**
   - threads.list già da snippet
   - Chiamare get solo quando user espande

2. **Non usare format=full se non serve body**
   - Spreco banda e quota
   - metadata è sufficiente per headers

3. **Non ignorare historyId**
   - Senza partial sync, sempre full sync
   - API quota si esaurisce velocemente

4. **Non assumere thread ordering**
   - API può restituire in ordine non cronologico
   - Ordina client-side per internalDate

---

## 8. Implementazione Raccomandata per Miracollook

### Step 1: Thread List View

**API Call:**
```javascript
threads.list({
  userId: 'me',
  labelIds: ['INBOX'],
  maxResults: 50
})
```

**UI Component:**
```jsx
<ThreadListItem>
  <ThreadSubject>{snippet da ultimo msg}</ThreadSubject>
  <ThreadMeta>
    {participants} · {messageCount} messages · {date}
  </ThreadMeta>
  <ThreadSnippet>{snippet}</ThreadSnippet>
</ThreadListItem>
```

**NON chiamare threads.get ancora!**

### Step 2: User Clicks Thread → Expand

**API Call:**
```javascript
threads.get({
  userId: 'me',
  id: threadId,
  format: 'metadata',  // Solo headers, non body ancora
  metadataHeaders: ['Subject', 'From', 'Date', 'To']
})
```

**UI Component:**
```jsx
<ThreadExpanded>
  {messages.map(msg => (
    <MessageCollapsed key={msg.id}>
      <MsgHeader>
        <From>{from}</From>
        <Date>{date}</Date>
      </MsgHeader>
      <MsgSnippet>{msg.snippet}</MsgSnippet>
      <ExpandButton onClick={() => loadMessageBody(msg.id)} />
    </MessageCollapsed>
  ))}
</ThreadExpanded>
```

### Step 3: User Clicks Message → Show Body

**Opzione A: Se hai già cached (format=full alla step 2):**
```javascript
// Leggi da state/cache
const body = cachedMessages[msgId].payload.body
```

**Opzione B: Se hai usato metadata:**
```javascript
// Fetch singolo messaggio
messages.get({
  userId: 'me',
  id: msgId,
  format: 'full'
})
```

### Step 4: Caching Layer

**Database/Store Structure:**
```javascript
{
  threads: {
    [threadId]: {
      id: 'thread_123',
      snippet: '...',
      historyId: '12345',
      messageIds: ['msg1', 'msg2', 'msg3'],
      lastFetched: timestamp,
      format: 'metadata' // o 'full'
    }
  },
  messages: {
    [msgId]: {
      id: 'msg1',
      threadId: 'thread_123',
      headers: {...},
      body: '...',  // null se format=metadata
      labelIds: [...],
      historyId: '12340'
    }
  },
  syncState: {
    lastHistoryId: '12345',
    lastSync: timestamp
  }
}
```

### Step 5: Incremental Sync

**Ogni 30-60 secondi (o push notification):**
```javascript
history.list({
  userId: 'me',
  startHistoryId: lastHistoryId
})

// Response: { messagesAdded, labelsAdded, etc. }
// Aggiorna solo quei messaggi
// Salva nuovo historyId
```

---

## 9. Confronto Approcci

### Approccio A: Eager (Full Upfront)

**Pro:**
- UX veloce dopo first load
- Nessun loading quando user espande

**Contro:**
- First load lento
- Spreco banda se user non espande tutto
- API quota più alta

**Quando:**
- Thread con pochi messaggi (1-3)
- App desktop con cache persistente

### Approccio B: Lazy (On-Demand)

**Pro:**
- First load veloce
- Spreco minimo (fetch solo what's needed)
- API quota ottimizzata

**Contro:**
- Loading spinner quando user espande
- Più API calls nel tempo

**Quando:**
- Thread lunghi (4+ messaggi)
- App mobile/web con connessione lenta

### Approccio C: Hybrid (Raccomandato per Miracollook)

**Strategia:**
```javascript
if (threadMessageCount <= 2) {
  // Small thread → eager full
  threads.get({format: 'full'})
} else {
  // Large thread → lazy metadata + body on-demand
  threads.get({format: 'metadata'})
  // Body fetch quando user click su message
}
```

**Pro:**
- Best of both worlds
- Intelligente per caso d'uso
- Performance ottimale

---

## 10. Code Examples

### Example 1: Lista Thread

```python
from googleapiclient.discovery import build

service = build('gmail', 'v1', credentials=creds)

# Get threads from inbox
results = service.users().threads().list(
    userId='me',
    labelIds=['INBOX'],
    maxResults=50
).execute()

threads = results.get('threads', [])

for thread in threads:
    print(f"Thread ID: {thread['id']}")
    print(f"Snippet: {thread['snippet']}")
    print(f"History ID: {thread['historyId']}")
    print('---')
```

### Example 2: Espandi Thread (Metadata)

```python
def get_thread_metadata(thread_id):
    thread = service.users().threads().get(
        userId='me',
        id=thread_id,
        format='metadata',
        metadataHeaders=['Subject', 'From', 'Date', 'To']
    ).execute()

    messages = thread.get('messages', [])

    for msg in messages:
        headers = {h['name']: h['value']
                   for h in msg['payload']['headers']}

        print(f"Message ID: {msg['id']}")
        print(f"From: {headers.get('From')}")
        print(f"Date: {headers.get('Date')}")
        print(f"Subject: {headers.get('Subject')}")
        print('---')

    return thread
```

### Example 3: Full Thread con Body

```python
def get_thread_full(thread_id):
    thread = service.users().threads().get(
        userId='me',
        id=thread_id,
        format='full'
    ).execute()

    messages = thread.get('messages', [])

    for msg in messages:
        # Headers
        headers = {h['name']: h['value']
                   for h in msg['payload']['headers']}

        # Body (base64 decoded)
        body_data = msg['payload']['body'].get('data', '')
        if body_data:
            import base64
            body = base64.urlsafe_b64decode(body_data).decode('utf-8')
        else:
            body = '[No body]'

        print(f"From: {headers.get('From')}")
        print(f"Body: {body[:100]}...")  # First 100 chars
        print('---')

    return thread
```

### Example 4: Incremental Sync

```python
def incremental_sync(last_history_id):
    try:
        history = service.users().history().list(
            userId='me',
            startHistoryId=last_history_id
        ).execute()

        changes = history.get('history', [])

        for change in changes:
            # Messages added
            if 'messagesAdded' in change:
                for msg_added in change['messagesAdded']:
                    msg_id = msg_added['message']['id']
                    print(f"New message: {msg_id}")
                    # Fetch and cache

            # Labels changed
            if 'labelsAdded' in change:
                for label_change in change['labelsAdded']:
                    msg_id = label_change['message']['id']
                    labels = label_change['labelIds']
                    print(f"Labels added to {msg_id}: {labels}")
                    # Update cache

        # Save new historyId
        new_history_id = history.get('historyId')
        return new_history_id

    except HttpError as e:
        if e.resp.status == 404:
            print("History ID too old, performing full sync")
            return perform_full_sync()
        raise
```

---

## 11. Errori Comuni da Evitare

### ❌ Errore 1: Chiamare threads.get per Ogni Thread in Lista

```python
# BAD
threads = threads_list()
for thread in threads:
    full_thread = threads.get(thread['id'])  # 50 API calls!
```

**Soluzione:** Usa snippet da threads.list, chiama get solo quando user espande.

### ❌ Errore 2: Non Gestire Pagination

```python
# BAD
results = threads.list(maxResults=50)
# Se ci sono 200 thread, ne vedi solo 50!
```

**Soluzione:**
```python
# GOOD
all_threads = []
results = threads.list(maxResults=50)
all_threads.extend(results.get('threads', []))

while 'nextPageToken' in results:
    results = threads.list(
        maxResults=50,
        pageToken=results['nextPageToken']
    )
    all_threads.extend(results.get('threads', []))
```

### ❌ Errore 3: Non Salvare historyId

```python
# BAD
def sync():
    threads = threads.list()
    # Nessun save di historyId → sempre full sync!
```

**Soluzione:** Salva historyId dopo ogni sync, usa per partial sync.

### ❌ Errore 4: Usare format=full Sempre

```python
# BAD - troppo pesante per anteprima
thread = threads.get(id, format='full')  # Carica TUTTO
# User vede solo headers, body sprecato!
```

**Soluzione:** format=metadata per preview, full solo quando serve body.

---

## 12. Quota e Limiti

### Gmail API Quotas (Default)

- **Queries per day**: 1,000,000,000
- **Queries per 100 seconds per user**: 250
- **Queries per second per user**: 25

### Best Practices per Quota

1. **Batch requests** quando possibile
2. **Cache aggressivo** per ridurre API calls
3. **Partial sync** invece di full sync continuo
4. **Push notifications** invece di polling frequente

### Exponential Backoff

```python
import time
from googleapiclient.errors import HttpError

def api_call_with_backoff(func, max_retries=5):
    for retry in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status == 429:  # Rate limit
                wait_time = 2 ** retry  # Exponential
                print(f"Rate limited, waiting {wait_time}s")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## 13. Raccomandazioni Finali per Miracollook

### Architettura Consigliata

```
Frontend (React)
├── ThreadList Component
│   ├── Fetch: threads.list (maxResults=50)
│   ├── Display: snippet, participants, date
│   └── Cache: thread IDs, snippets
│
├── ThreadView Component (on click)
│   ├── Check cache: esiste thread full?
│   ├── Se NO: threads.get(format=metadata)
│   ├── Display: collapsed messages (headers only)
│   └── Cache: metadata per ogni message
│
├── MessageView Component (on click singolo msg)
│   ├── Check cache: esiste body?
│   ├── Se NO: messages.get(format=full)
│   ├── Display: full body
│   └── Cache: body completo
│
└── SyncManager Service (background)
    ├── Salva: lastHistoryId dopo ogni operazione
    ├── Ogni 60s: history.list(startHistoryId)
    ├── Update cache: solo messaggi cambiati
    └── Error handling: fallback a full sync su 404
```

### Database Schema (IndexedDB/LocalStorage)

```javascript
// Threads collection
{
  threadId: {
    id: 'thread_123',
    snippet: '...',
    historyId: '12345',
    messageCount: 3,
    participants: ['user1@', 'user2@'],
    lastMessageDate: timestamp,
    messageIds: ['msg1', 'msg2', 'msg3'],
    labels: ['INBOX', 'UNREAD'],
    fetchedAt: timestamp,
    format: 'metadata'  // o 'full'
  }
}

// Messages collection
{
  messageId: {
    id: 'msg1',
    threadId: 'thread_123',
    from: 'sender@example.com',
    to: ['recipient@example.com'],
    subject: 'Re: Discussion',
    date: timestamp,
    snippet: '...',
    body: 'full body text' | null,  // null se format=metadata
    labelIds: ['INBOX', 'UNREAD'],
    historyId: '12340',
    fetchedAt: timestamp
  }
}

// Sync state
{
  lastHistoryId: '12345',
  lastSyncAt: timestamp,
  syncStrategy: 'partial' | 'full'
}
```

### API Layer (Service)

```typescript
class GmailThreadService {
  // Lista thread (inbox view)
  async listThreads(params: {
    maxResults?: number,
    labelIds?: string[],
    query?: string,
    pageToken?: string
  }): Promise<Thread[]>

  // Espandi thread (metadata only, veloce)
  async getThreadMetadata(threadId: string): Promise<ThreadDetail>

  // Ottieni thread completo (con body)
  async getThreadFull(threadId: string): Promise<ThreadDetail>

  // Strategia ibrida (intelligente)
  async getThread(threadId: string): Promise<ThreadDetail> {
    const thread = await this.getThreadMetadata(threadId)

    // Se thread piccolo, fetch full subito
    if (thread.messages.length <= 2) {
      return await this.getThreadFull(threadId)
    }

    // Se thread grande, lazy load body
    return thread
  }

  // Sync incrementale
  async syncUpdates(): Promise<void> {
    const lastHistoryId = await this.getLastHistoryId()

    try {
      const history = await this.historyList(lastHistoryId)
      await this.applyChanges(history)
      await this.saveHistoryId(history.historyId)
    } catch (error) {
      if (error.status === 404) {
        // historyId troppo vecchio, full sync
        await this.fullSync()
      }
    }
  }
}
```

### Performance Targets

| Operazione | Target | Strategia |
|------------|--------|-----------|
| Load inbox (50 threads) | < 1s | threads.list cached |
| Espandi thread (5 msgs) | < 500ms | metadata cached o fetch |
| Mostra body singolo msg | < 300ms | Cache o fetch on-demand |
| Sync incrementale | < 2s | history.list + update cache |

---

## 14. Next Steps per Implementazione

### Fase 1: POC (Proof of Concept)
- [ ] Implementa threads.list per inbox view
- [ ] Test con thread reale (2-3 messaggi)
- [ ] Verifica format options (metadata vs full)
- [ ] Valida performance

### Fase 2: Caching Layer
- [ ] Design database schema (IndexedDB)
- [ ] Implementa cache per threads
- [ ] Implementa cache per messages
- [ ] Test invalidation strategy

### Fase 3: Incremental Sync
- [ ] Implementa history.list
- [ ] Salva/recupera historyId
- [ ] Gestisci errori (404 fallback)
- [ ] Test con sync reale

### Fase 4: UI Components
- [ ] ThreadList component
- [ ] ThreadExpanded component
- [ ] MessageCollapsed component
- [ ] MessageBody component (lazy)

### Fase 5: Optimization
- [ ] Batch requests per thread.get multipli
- [ ] Lazy loading per body grandi
- [ ] Exponential backoff per rate limiting
- [ ] Performance monitoring

---

## Sources

**Documentazione Ufficiale:**
- [Managing Threads | Gmail API Guide](https://developers.google.com/workspace/gmail/api/guides/threads)
- [Method: users.threads.get](https://developers.google.com/gmail/api/reference/rest/v1/users.threads/get)
- [Method: users.threads.list](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.threads/list)
- [REST Resource: users.threads](https://developers.google.com/gmail/api/reference/rest/v1/users.threads)
- [Synchronizing Clients with Gmail](https://developers.google.com/workspace/gmail/api/guides/sync)

**Riferimenti Aggiuntivi:**
- [Gmail API Python Client - threads()](https://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.users.threads.html)
- [Gmail API Developer Intro: Spotting Chatty Threads](https://dev.to/googleworkspace/gmail-api-developer-intro-spotting-chatty-threads-jnp)

---

## Conclusione

**La mia raccomandazione per Miracollook:**

1. **Approccio Hybrid** - Metadata per preview, full on-demand
2. **Cache Aggressivo** - IndexedDB per persistenza
3. **Partial Sync** - history.list ogni 60s o push notification
4. **UI Pattern** - Collapsed by default, expand on click

**Perché:**
- Balance perfetto tra UX e performance
- API quota ottimizzata (critical per scale)
- Cache intelligente riduce latenza
- Pattern testato da Gmail stesso

**Effort Estimate:**
- POC: 2-3 giorni
- Full implementation: 1-2 settimane
- Optimization: 3-5 giorni

**Risk Level:** BASSO - API ben documentata, pattern collaudato

---

*Ricerca completata da Cervella Researcher - 14 Gennaio 2026*
*"Non reinventiamo la ruota - la miglioriamo!"*
