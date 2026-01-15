# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 15 Gennaio 2026 - Sessione 229
> **STATO: 3 BUG FIXATI, 4 DA FARE**

---

## STATO IN UNA RIGA

**MIRACALLOOK: Email rendering OK, resize OK, bulk actions OK. Mancano checkbox gruppi e UX polish.**

---

## SESSIONE 229: BUG FIX

### FIXATI
1. **Email HTML rendering** - Backend ora preferisce text/html, plain text con \n-><br>
   - File: `gmail/api.py` linee 716-736 e 793-813
2. **Resize pannelli** - CSS flexbox con `resize: horizontal` (temporaneo ma funziona)
   - File: `ThreePanel.tsx` - layout semplice con width px
3. **Bulk Actions 422** - Aggiunto `embed=True` a tutti gli endpoint Body()
   - File: `gmail/api.py` - archive, trash, untrash, mark-read, mark-unread

### DA FARE (PROSSIMA SESSIONE)

**PRIORITA ALTA:**
1. **Checkbox nei gruppi** - Email aggregate non mostrano checkbox individuali
2. **Barra bulk opaca** - Si sovrappone al contenuto, serve background blur/opaco

**PRIORITA MEDIA:**
3. **Sistema cartelle** - Archive funziona ma dove vanno le email? UI per cartelle
4. **Drag handles custom** - Sostituire CSS resize con drag professionale

**FUTURO:**
5. Sanitizzazione HTML (XSS protection)

---

## FILE MODIFICATI (Sessione 229)

```
miracallook/backend/gmail/api.py    <- HTML preference + embed=True
miracallook/frontend/src/components/Layout/ThreePanel.tsx <- CSS resize
```

---

## MAPPA PORTE

| Progetto | Backend | Frontend |
|----------|---------|----------|
| Miracollo PMS | 8001 | 80/443 |
| Miracallook | 8002 | 5173/5174 |

---

## NOTE TECNICHE

**react-resizable-panels v4.4.1:**
- Bug fix v4.3.1 NON ha risolto il problema per noi
- La libreria calcola male le dimensioni dal DOM
- Usato CSS resize come workaround

**FastAPI Body():**
- Singolo parametro Body() senza embed=True si aspetta valore diretto
- Con embed=True si aspetta {"param": value}
- Frontend manda sempre oggetto JSON

---

*"3 bug fixati, app funziona! UX polish nella prossima sessione."*
