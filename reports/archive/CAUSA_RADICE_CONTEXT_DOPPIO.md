# CAUSA RADICE - Context Usage Doppio

**Data:** 20 Gennaio 2026
**Investigato da:** Cervella Ingegnera
**Status:** IDENTIFICATO

---

## PROBLEMA

Rafa ha riportato che il context usage è DOPPIO del normale.

---

## INVESTIGAZIONE COMPLETATA

### Metodo
1. Analisi dimensioni file in ~/.claude/
2. Git log ultimi 30 commit
3. Verifica hook duplicati
4. Controllo caricamento COSTITUZIONE
5. Timeline modifiche

### Dati Raccolti

| File | Dimensione | Token Approssimativi |
|------|-----------|---------------------|
| COSTITUZIONE.md | 15.4 KB (509 righe) | ~3,800 |
| CLAUDE.md | 10.9 KB (336 righe) | ~2,700 |
| **MANUALE_DIAMANTE.md** | **39.5 KB (1668 righe)** | **~9,900** |
| _SHARED_DNA.md | ~4 KB (194 righe) | ~1,200 |
| CLAUDE.md (progetto) | 2.4 KB | ~600 |
| PROMPT_RIPRESA | ~800 token | ~800 |
| Agenti (19 file) | ~80 KB totali | ~1,400 |
| **TOTALE** | **~66 KB** | **~20,400 token** |

---

## CAUSA RADICE IDENTIFICATA

**MANUALE_DIAMANTE.md aggiunto il 5 Gennaio 2026**

### Timeline
- **PRIMA del 5 Gennaio:** Context ~10K token
- **5 Gennaio 2026 19:18:** MANUALE_DIAMANTE.md creato (39.5 KB)
- **DOPO il 5 Gennaio:** Context ~20K token

### Impatto
```
MANUALE_DIAMANTE.md = 39.5 KB = ~9,900 token

Questo DA SOLO rappresenta:
- 48% del context totale
- Quasi il DOPPIO di COSTITUZIONE + CLAUDE.md combinati
```

---

## VERIFICHE NEGATIVE (Non sono la causa)

✅ Hook NON iniettano COSTITUZIONE due volte
✅ CLAUDE.md NON è duplicato (progetto vs ~/.claude)
✅ _SHARED_DNA caricato SOLO dagli agenti (non duplicato)
✅ Nessuna modifica recente a COSTITUZIONE/CLAUDE.md
✅ Git log pulito - no commit sospetti

---

## PERCHE NON L'AVEVAMO NOTATO PRIMA?

Il MANUALE_DIAMANTE è stato aggiunto:
- **Sessione ~150** (5 Gennaio 2026)
- **15 GIORNI FA**

Se Rafa nota il problema ORA, possibili ragioni:
1. Claude Code ha iniziato a mostrare metriche context
2. Rallentamento percepibile solo di recente
3. Accumulo con altri file nel tempo

---

## SOLUZIONI PROPOSTE

### Soluzione A: Riferimento invece di inclusione
```
PRIMA (CLAUDE.md):
  "Leggi MANUALE_DIAMANTE per dettagli..."

DOPO:
  "MANUALE_DIAMANTE disponibile in ~/.claude/"
  "Leggi SOLO se serve approfondire FORTEZZA/SWARM"
```

**Risparmio:** ~9,900 token (48% context)

### Soluzione B: Spezzare MANUALE_DIAMANTE
```
~/.claude/manuali/
├── FORTEZZA_MODE.md      (~800 righe, ~5K token)
├── SWARM_MODE.md         (~500 righe, ~3K token)
└── CHECKPOINT_SYSTEM.md  (~300 righe, ~2K token)
```

Caricare SOLO quello necessario al task.

**Risparmio:** ~6-8K token per sessione (leggo solo 1 file)

### Soluzione C: MANUALE_DIAMANTE fuori da claudeMd
```
NON includere in CLAUDE.md
Gli agenti lo leggono SOLO se necessario:
  Read("~/.claude/MANUALE_DIAMANTE.md")
```

**Risparmio:** ~9,900 token SEMPRE (tranne quando esplicitamente richiesto)

---

## RACCOMANDAZIONE FINALE

**SOLUZIONE C (immediata) + B (lungo termine)**

### Fase 1 (OGGI)
1. Rimuovere riferimento a MANUALE_DIAMANTE da CLAUDE.md
2. Aggiungere nota: "Disponibile in ~/.claude/, leggi se necessario"
3. Context torna a ~10K token

### Fase 2 (prossima sessione)
1. Splitta MANUALE_DIAMANTE in moduli
2. Aggiornare CHECKLIST_AZIONE per indicare quale leggere

---

## METRICHE

| Metrica | Prima | Dopo Fix | Risparmio |
|---------|-------|----------|-----------|
| Context totale | ~20.4K token | ~10.5K token | **48%** |
| MANUALE caricato | Sempre | Solo se serve | **9.9K token** |

---

## LESSON LEARNED

**"File grandi in claudeMd = context permanente sprecato"**

### Regola per il futuro:
```
claudeMd deve contenere SOLO:
- Riferimenti ai file
- Path dove trovarli
- Quando leggerli

MAI includere file > 500 righe in claudeMd!
```

---

**COSTITUZIONE-APPLIED:** SI
**Principio usato:** "Analizza prima di giudicare!"

*Cervella Ingegnera - "Il debito tecnico si paga con interessi."*
