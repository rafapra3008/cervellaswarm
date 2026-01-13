# MIRACOLLOOK - Strategie di Prefetch Email

**Data Ricerca**: 13 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Scope**: Ottimizzare percezione di velocità tramite prefetch intelligente

---

## SINTESI ESECUTIVA

Il prefetch strategico è la tecnica chiave usata dai big player (Gmail, Superhuman) per creare la percezione di "istantaneità". L'obiettivo NON è pre-caricare tutto, ma **anticipare le azioni più probabili dell'utente** minimizzando il bandwidth waste.

### Raccomandazione Primaria

**APPROCCIO IBRIDO**: Combinare prefetch on hover (alta probabilità apertura) + top N unread (priorità inbox) + viewport-based (scroll naturale).

### Metriche Target Superhuman
- **< 50ms** tempo percepito di apertura email (con cache hit)
- **< 100ms** per sentirsi "istantaneo"
- **Risparmio utente**: ~3 ore/settimana su gestione email

---

## STRATEGIE COMPETITOR

### 1. Gmail - Image Prefetch Aggressivo

**Come Funziona**:
- Gmail pre-fetcha immagini email **prima** che l'utente apra il messaggio
- Attivazione: quando Gmail è aperto E utente loggato E email arriva
- User-Agent specifico: Chrome/42.0.2311.135 (identificabile)
- Security scan integrato nel prefetch

**Impatto Misurato**:
- False opens: 1-6% delle aperture Gmail (~2pp inflazione open rate)
- Prefetch da Google IP ranges specifici

**Pro**:
- Rendering istantaneo immagini
- Security check preventivo

**Contro**:
- Inflazione metriche tracking
- Bandwidth overhead su connessioni lente

**Fonti**:
- [Gmail Prefetching Impact - Mailmodo](https://www.mailmodo.com/guides/gmail-prefetching/)
- [Gmail Prefetching Images - Litmus](https://www.litmus.com/blog/gmail-prefetching-images)

---

### 2. Superhuman - Cache Locale + Predictive Preload

**La "100ms Rule"**:
> Ogni interazione digitale deve essere < 100ms per sentirsi istantanea.
> Target reale Superhuman: **< 50ms** (1-2 Chrome frames)

**Implementazione**:
1. **Local Database**: Email accessibili offline, cache persistente
2. **Predictive Preloading**: "Preloads threads you're most likely to view soon"
3. **Zero Animations**: Eliminano overhead rendering
4. **Keyboard-First**: Più veloce del mouse

**Architettura Cache**:
- Priorità cache locale su API calls
- Server-side optimizations + advanced indexing
- Background sync continuo

**Risultati**:
- Email opening: Near-instantaneous
- Search: < 100ms
- Utenti risparmiano 3h/settimana

**Fonti**:
- [Superhuman Speed Philosophy](https://blog.superhuman.com/superhuman-is-built-for-speed/)

---

### 3. Outlook Web - Approccio Non Documentato

**Strategia Inferita**:
- Focus su Office 365 integration
- Pre-rendering parziale su lista email
- Meno aggressivo di Gmail su prefetch

---

## STRATEGIE TECNICHE CONFRONTO

| Strategia | Probabilità Hit | Bandwidth Cost | Complessità | UX Impact |
|-----------|----------------|----------------|-------------|-----------|
| **Prefetch on Hover** | ⭐⭐⭐⭐⭐ Alta | 💰 Basso | ⚙️ Medio | 🚀 Altissimo |
| **Top N Unread** | ⭐⭐⭐⭐ Alta | 💰💰 Medio | ⚙️ Basso | 🚀🚀 Alto |
| **Viewport Scroll** | ⭐⭐⭐ Media | 💰 Basso | ⚙️ Basso | 🚀 Medio |
| **Predictive ML** | ⭐⭐⭐⭐⭐ Altissima | 💰💰💰 Alto | ⚙️⚙️⚙️ Molto Alto | 🚀🚀🚀 Massimo |
| **Prefetch All** | ⭐⭐⭐⭐⭐ Certezza | 💰💰💰💰 Altissimo | ⚙️ Basso | ❌ Negativo |

### Dettaglio Strategie

#### A. Prefetch on Hover

**Quando**: Mouse sopra email row per > N millisecondi

**Best Practices 2026**:
- **Delay ottimale**: 500ms collettivi (intent detection)
- **Mobile**: Usare `touchstart` invece di `mouseover`
- **Abort**: Cancellare se utente si sposta via

**Timing Patterns**:
```
65ms   = Start prefetch aggressivo (Google)
200ms  = Bilanciato intent detection
500ms  = Conservative, alta confidence
1000ms = Troppo lento, percezione ritardo
```

**Pro**:
- Alta probabilità apertura (hover = intent)
- Bandwidth limitato (1 email alla volta)
- UX impact massimo

**Contro**:
- Desktop-only (mobile no hover naturale)
- Richiede abort logic solida

**Fonti**:
- [Hover Prefetch Best Practices - Alex MacArthur](https://macarthur.me/posts/best-ish-practices-for-dynamically-prefetching-and-prerendering-with-javascript/)
- [Webperf Tips - Hover Preloading](https://webperf.tips/tip/hover-preloading/)

---

#### B. Top N Unread (Priority Prefetch)

**Quando**: All'apertura inbox, pre-caricare prime 3-5 email unread

**Logica**:
```
Priority Score = (
  isUnread * 10 +
  isFromImportantSender * 5 +
  recencyScore * 3 +
  threadSize * 1
)
```

**Configurazione Suggerita**:
- Desktop: Top 5
- Mobile: Top 3
- Tablet: Top 4

**Pro**:
- Predictable bandwidth usage
- Alta probabilità apertura (inbox scan pattern)
- Background silenzioso

**Contro**:
- Spreco se utente salta alle vecchie
- Overhead iniziale caricamento inbox

---

#### C. Viewport-Based (Intersection Observer)

**Quando**: Email entra nel viewport durante scroll

**Implementazione**:
```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        prefetchEmail(entry.target.dataset.emailId);
      }
    });
  },
  {
    root: null, // viewport
    rootMargin: '200px', // prefetch 200px before visible
    threshold: 0 // trigger as soon as 1px visible
  }
);
```

**Configurazione Ottimale**:
- `rootMargin`: 200px (prefetch prima visibilità)
- `threshold`: 0 (appena entra in viewport)
- Observer singolo per lista completa (performance)

**Pro**:
- Natural scroll behavior
- Low waste (utente sta scorrendo verso email)
- Mobile-friendly

**Contro**:
- Timing imperfetto (ritardo scroll → prefetch → load)
- Richiede scroll (prime email sempre visibili)

**Fonti**:
- [Intersection Observer API 2026 Guide](https://future.forem.com/sherry_walker_bba406fb339/mastering-the-intersection-observer-api-2026-a-complete-guide-561k)
- [Next.js Viewport Prefetch PR](https://github.com/vercel/next.js/pull/7196/files)

---

#### D. Predictive ML-Based

**Quando**: Modello ML predice prossima email aperta

**Signals per Training**:
- Sender frequency
- Time patterns (orari apertura)
- Subject patterns
- Thread engagement history
- Keyboard shortcuts usage

**Implementazione**:
```
User Pattern → TensorFlow.js Model → Confidence Score → Prefetch Top 3
```

**Pro**:
- Massima efficienza bandwidth/hit ratio
- Personalizzato per utente
- Migliora nel tempo

**Contro**:
- Complessità altissima
- Richiede dati training
- Privacy concerns
- Overhead computazionale client-side

**Fonti**:
- [TensorFlow.js Predictive Prefetch](https://www.tensorflow.org/js/tutorials/applications/predictive_prefetching)
- [ML-Based Prefetch Optimization](https://dl.acm.org/doi/10.1145/1654059.1654116)

---

## IMPLEMENTAZIONE REACT QUERY

### Setup Base

```typescript
import { useQueryClient } from '@tanstack/react-query';

const queryClient = useQueryClient();

// Prefetch email content
const prefetchEmail = async (emailId: string) => {
  await queryClient.prefetchQuery({
    queryKey: ['email', emailId],
    queryFn: () => fetchEmailContent(emailId),
    staleTime: 60000, // 1 min cache
  });
};
```

### Pattern 1: Hover Prefetch

```typescript
const EmailRow = ({ email }) => {
  const [hoverTimer, setHoverTimer] = useState<number | null>(null);
  const queryClient = useQueryClient();

  const handleMouseEnter = () => {
    // Delay 300ms per intent detection
    const timer = window.setTimeout(() => {
      queryClient.prefetchQuery({
        queryKey: ['email', email.id],
        queryFn: () => fetchEmailContent(email.id),
        staleTime: 60000,
      });
    }, 300);

    setHoverTimer(timer);
  };

  const handleMouseLeave = () => {
    // Abort prefetch se utente si sposta
    if (hoverTimer) {
      clearTimeout(hoverTimer);
      setHoverTimer(null);
    }
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {/* Email row UI */}
    </div>
  );
};
```

### Pattern 2: Top N Prefetch (requestIdleCallback)

```typescript
const EmailList = ({ emails }) => {
  const queryClient = useQueryClient();

  useEffect(() => {
    // Prefetch in idle time per non bloccare UI
    const prefetchTopEmails = () => {
      const unreadEmails = emails
        .filter(e => !e.isRead)
        .slice(0, 5);

      unreadEmails.forEach((email, index) => {
        // Stagger prefetch per evitare spike
        requestIdleCallback(() => {
          queryClient.prefetchQuery({
            queryKey: ['email', email.id],
            queryFn: () => fetchEmailContent(email.id),
            staleTime: 300000, // 5 min cache
          });
        }, { timeout: 2000 + (index * 500) }); // fallback timeout incrementale
      });
    };

    prefetchTopEmails();
  }, [emails, queryClient]);

  return <>{/* Lista email */}</>;
};
```

**Fonti**:
- [React Query Prefetching Docs](https://tanstack.com/query/latest/docs/framework/react/guides/prefetching)
- [requestIdleCallback Guide](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback)

### Pattern 3: Intersection Observer Prefetch

```typescript
const EmailRow = ({ email }) => {
  const ref = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();
  const [hasPrefetched, setHasPrefetched] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !hasPrefetched) {
            queryClient.prefetchQuery({
              queryKey: ['email', email.id],
              queryFn: () => fetchEmailContent(email.id),
              staleTime: 60000,
            });
            setHasPrefetched(true);
          }
        });
      },
      {
        root: null,
        rootMargin: '200px', // prefetch before visible
        threshold: 0,
      }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [email.id, hasPrefetched, queryClient]);

  return <div ref={ref}>{/* Email row */}</div>;
};
```

### Pattern 4: Abort Prefetch on Navigation

```typescript
const prefetchEmail = (emailId: string) => {
  const abortController = new AbortController();

  queryClient.prefetchQuery({
    queryKey: ['email', emailId],
    queryFn: async ({ signal }) => {
      // Pass signal to fetch
      return fetchEmailContent(emailId, { signal });
    },
  });

  return abortController;
};

// Usage in component
const handleMouseEnter = () => {
  const controller = prefetchEmail(email.id);

  // Store controller per abort later
  setActiveController(controller);
};

const handleMouseLeave = () => {
  // Cancel prefetch se utente cambia idea
  activeController?.abort();
  setActiveController(null);
};
```

**Fonti**:
- [React Query Cancellation](https://tanstack.com/query/v3/docs/framework/react/guides/query-cancellation)
- [AbortController in React](https://westbrookdaniel.com/blog/react-abort-controllers/)

---

## METRICHE E LIMITI

### Quante Email Pre-caricare?

| Context | Prefetch Count | Rationale |
|---------|---------------|-----------|
| **Desktop - Hover** | 1 alla volta | Intent chiaro, banda OK |
| **Desktop - Top N** | 5 email | Balance hit rate / bandwidth |
| **Mobile - Top N** | 3 email | Banda limitata, screen size |
| **Tablet** | 4 email | Medio tra desktop/mobile |
| **2G/Slow Connection** | 1-2 email | Evitare lag, data saver |

### Bandwidth Considerations

**Stima Dimensioni**:
```
Email Header Only: ~2-5 KB
Email Body (text): ~10-50 KB
Email Body + Images: ~100-500 KB (no prefetch images!)
Email Body + Attachments: ~1-10 MB (NEVER prefetch!)
```

**Raccomandazione MIRACOLLOOK**:
- Prefetch SOLO body testuale + metadata
- NO prefetch attachments
- NO prefetch embedded images (lazy load on open)

**Limiti Bandwidth**:
```
Desktop WiFi:  Prefetch aggressivo OK (5-10 email)
Mobile 4G/5G:  Prefetch moderato (3-5 email)
Mobile 3G:     Prefetch conservativo (1-2 email)
Mobile 2G:     NO prefetch, solo on-demand
Data Saver ON: NO prefetch
```

**Detection Data Saver Mode**:
```javascript
// Android/Chrome Data Saver
if (navigator.connection?.saveData) {
  // DISABLE prefetch
  return;
}

// iOS Low Data Mode (via Service Worker)
if (navigator.connection?.effectiveType === 'slow-2g') {
  // DISABLE prefetch
  return;
}
```

**Fonti**:
- [Android Data Saver Optimization](https://developer.android.com/develop/connectivity/network-ops/data-saver)
- [Content Prefetching Best Practices - AT&T](https://developer.att.com/video-optimizer/docs/best-practices/content-pre-fetching)

### Cache Invalidation

**Quando Invalidare Cache Email**:

1. **Real-time Update Received** (WebSocket/SSE)
   ```typescript
   socket.on('email:updated', (emailId) => {
     queryClient.invalidateQueries({ queryKey: ['email', emailId] });
   });
   ```

2. **User Action** (mark read/unread, star, archive)
   ```typescript
   queryClient.invalidateQueries({ queryKey: ['email', emailId] });
   queryClient.invalidateQueries({ queryKey: ['emails'] }); // lista
   ```

3. **Stale Time Expired** (automatic)
   ```typescript
   staleTime: 60000, // 1 min = refetch automatico
   ```

4. **Background Sync** (polling)
   ```typescript
   refetchInterval: 30000, // 30s per inbox attiva
   ```

**Strategia MIRACOLLOOK**:
- Email content: `staleTime: 300000` (5 min)
- Email list: `staleTime: 30000` (30s)
- Invalidazione manuale su WebSocket events
- Background refetch solo su tab attiva

**Fonti**:
- [React Query Invalidation](https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation)
- [Automatic Query Invalidation - TkDodo](https://tkdodo.eu/blog/automatic-query-invalidation-after-mutations)

---

## RACCOMANDAZIONE per MIRACOLLOOK

### Strategia Implementativa (Fasi)

#### FASE 1 - MVP Prefetch (Sprint Corrente)
**FOCUS: Quick Win, Low Complexity**

1. **Top 3 Unread Prefetch**
   - Al caricamento inbox, prefetch top 3 unread
   - Background, usando `requestIdleCallback`
   - Detection bandwidth (NO prefetch se data saver)

2. **React Query Setup**
   - `staleTime: 60000` per email content
   - Cache invalidation su WebSocket events
   - Error handling graceful

**Effort**: 2-3 giorni
**Impact**: Alto (prime email sempre instant)
**Risk**: Basso

---

#### FASE 2 - Hover Prefetch (Sprint Successivo)
**FOCUS: Desktop UX Boost**

1. **Hover con Delay 300ms**
   - Desktop only (check `window.matchMedia`)
   - Abort controller per cancellazione
   - Debounce per evitare spam

2. **Mobile Fallback**
   - No hover su mobile (touchstart troppo inaccurato)
   - Rely solo su Top N

**Effort**: 3-4 giorni
**Impact**: Altissimo su desktop
**Risk**: Medio (gestione abort, edge cases)

---

#### FASE 3 - Viewport Prefetch (Refinement)
**FOCUS: Natural Scroll**

1. **Intersection Observer**
   - `rootMargin: 200px`
   - Prefetch quando email entra "near viewport"
   - Single observer per lista

2. **Priority Logic**
   - Unread > Read
   - Recent > Old

**Effort**: 2-3 giorni
**Impact**: Medio (scroll già gestito da hover)
**Risk**: Basso

---

#### FASE 4 - ML Predictive (Futuro/Optional)
**FOCUS: Personalization**

1. **User Pattern Tracking**
   - Log open patterns, sender frequency
   - Privacy-first (local only, no server)

2. **TensorFlow.js Model**
   - Training su device
   - Prefetch predictions

**Effort**: 2-3 settimane
**Impact**: Altissimo (max efficiency)
**Risk**: Alto (complessità, privacy, testing)

---

### Configurazione Finale Raccomandata

```typescript
// miracollook/src/hooks/usePrefetchStrategy.ts

export const PREFETCH_CONFIG = {
  // Top N Strategy
  topN: {
    desktop: 5,
    mobile: 3,
    tablet: 4,
  },

  // Hover Strategy
  hover: {
    enabled: true,
    delayMs: 300,
    desktopOnly: true,
  },

  // Viewport Strategy
  viewport: {
    enabled: true,
    rootMargin: '200px',
    threshold: 0,
  },

  // Cache Config
  cache: {
    emailStaleTime: 60000, // 1 min
    listStaleTime: 30000,  // 30s
  },

  // Bandwidth Limits
  bandwidth: {
    maxConcurrentPrefetch: 3,
    disableOnDataSaver: true,
    disableOn2G: true,
  },
};
```

---

## CHECKLIST IMPLEMENTAZIONE

### Pre-Sviluppo
- [ ] Read `fetchEmailContent` API signature
- [ ] Verificare dimensioni medie email (KB)
- [ ] Check se esiste già cache layer
- [ ] Verificare setup React Query nel progetto

### Durante Sviluppo
- [ ] Implementare bandwidth detection (Data Saver)
- [ ] Abort controller per hover prefetch
- [ ] Error boundaries per prefetch failures
- [ ] Logging prefetch hits/misses (analytics)

### Testing
- [ ] Test su connessione lenta (Chrome DevTools throttling)
- [ ] Test Data Saver mode (Android)
- [ ] Test hover su lista lunga (memory leaks?)
- [ ] Test abort prefetch on navigation
- [ ] Measure cache hit rate dopo 1 settimana

### Metriche di Successo
- [ ] Cache hit rate > 70% (hover prefetch)
- [ ] Perceived load time < 100ms (cached)
- [ ] Bandwidth overhead < 10% totale
- [ ] Zero memory leaks su scroll lungo

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|------------|---------|-------------|
| **Bandwidth waste** | Media | Alto | Detection data saver, limits |
| **Memory leaks** | Media | Alto | Cleanup observers, abort controllers |
| **Over-prefetch** | Alta | Medio | Limits, priority logic |
| **Stale data** | Bassa | Medio | WebSocket invalidation |
| **Desktop-only benefit** | Alta | Basso | Mobile: rely on Top N |

---

## FONTI COMPLETE

### Email Client Best Practices
- [Gmail Prefetching Impact - Mailmodo](https://www.mailmodo.com/guides/gmail-prefetching/)
- [Gmail Prefetching Images - Litmus](https://www.litmus.com/blog/gmail-prefetching-images)
- [Superhuman Speed Philosophy](https://blog.superhuman.com/superhuman-is-built-for-speed/)

### Prefetch Techniques
- [Hover Prefetch Best Practices - Alex MacArthur](https://macarthur.me/posts/best-ish-practices-for-dynamically-prefetching-and-prerendering-with-javascript/)
- [Webperf Tips - Hover Preloading](https://webperf.tips/tip/hover-preloading/)
- [Prefetching in Modern Frontend - Medium](https://medium.com/@satyrorafa/prefetching-in-modern-frontend-what-it-is-when-to-use-it-and-how-to-optimize-performance-fe8af341d303)

### React Query Implementation
- [React Query Prefetching Docs](https://tanstack.com/query/latest/docs/framework/react/guides/prefetching)
- [How to Prefetch with React Query - JSdev](https://jsdev.space/howto/react-query-prefetch/)
- [Easiest Way to Prefetch Links - Medium](https://medium.com/@anokyy/the-easiest-way-to-prefetch-links-and-fix-fetch-waterfalls-in-react-query-useswr-apollo-client-or-33ae59409bf4)

### Web APIs
- [Intersection Observer API 2026 Guide](https://future.forem.com/sherry_walker_bba406fb339/mastering-the-intersection-observer-api-2026-a-complete-guide-561k)
- [IntersectionObserver - MDN](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver)
- [requestIdleCallback - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback)
- [requestIdleCallback Guide - DEV](https://dev.to/hexshift/how-to-use-requestidlecallback-for-efficient-background-tasks-in-javascript-151g)

### Cancellation & Abort
- [React Query Cancellation](https://tanstack.com/query/v3/docs/framework/react/guides/query-cancellation)
- [Cancelling Requests with React Query](https://carlrippon.com/cancelling-requests-with-react-query/)
- [AbortController in React](https://westbrookdaniel.com/blog/react-abort-controllers/)

### Bandwidth & Performance
- [Android Data Saver Optimization](https://developer.android.com/develop/connectivity/network-ops/data-saver)
- [Content Prefetching Best Practices - AT&T](https://developer.att.com/video-optimizer/docs/best-practices/content-pre-fetching)
- [Android Connectivity for Billions](https://developer.android.com/docs/quality-guidelines/build-for-billions/connectivity)

### Cache Invalidation
- [React Query Invalidation](https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation)
- [Automatic Query Invalidation - TkDodo](https://tkdodo.eu/blog/automatic-query-invalidation-after-mutations)
- [Cache Invalidation Strategies](https://www.ioriver.io/terms/cache-invalidation)

### ML & Predictive
- [TensorFlow.js Predictive Prefetch](https://www.tensorflow.org/js/tutorials/applications/predictive_prefetching)
- [ML-Based Prefetch Optimization - ACM](https://dl.acm.org/doi/10.1145/1654059.1654116)
- [Speed up Sites with ML Prefetch - TensorFlow Blog](https://blog.tensorflow.org/2021/05/speed-up-your-sites-with-web-page-prefetching-using-ml.html)

---

## NEXT STEPS

1. **Review con Frontend Team**
   - Validare approccio tecnico
   - Check existing cache layer
   - Estimate effort FASE 1

2. **POC Hover Prefetch**
   - Test isolato su 1 componente
   - Measure cache hit rate
   - User testing percepito

3. **Decision: Go/No-Go FASE 2**
   - Se FASE 1 hit rate > 60% → procedi
   - Se < 40% → rivedi strategy

---

*Ricerca completata da Cervella Researcher*
*"Studiare prima di agire - i player grossi hanno già risolto questi problemi!"*
