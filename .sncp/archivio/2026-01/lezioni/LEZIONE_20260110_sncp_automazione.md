# LEZIONE: Automazione SNCP per Mantenerlo Vivo

> **Data:** 10 Gennaio 2026
> **Sessione:** 148
> **Categoria:** Automazione

---

## Cosa E' Stato Fatto

Creato hook `sncp_auto_update.py` che:

1. **A fine sessione:** Aggiorna automaticamente `stato/oggi.md`
2. **A inizio sessione:** Verifica file obsoleti (>48h) e notifica

---

## Perche' E' Importante

> **"SNCP funziona solo se lo VIVIAMO"**

Nella sessione 147b abbiamo scoperto che SNCP era rating 5/10 perche:
- I file non venivano aggiornati
- Nessun reminder automatico
- Dipendeva tutto dalla disciplina manuale

L'automazione risolve questo problema.

---

## Come Funziona

### SessionStart (startup/resume)
```python
# Verifica file critici:
- stato/oggi.md
- coscienza/pensieri_regina.md
- futuro/roadmap.md

# Se non aggiornati da >48h -> notifica warning
```

### SessionEnd
```python
# Appende automaticamente a stato/oggi.md:
## AUTO-CHECKPOINT: 2026-01-10 12:45 (session_end)
- Progetto: CervellaSwarm
- Evento: session_end
- Generato da: sncp_auto_update.py v1.0.0
```

---

## Configurazione

Hook registrato in `~/.claude/settings.json`:
- SessionStart (startup + resume)
- SessionEnd

---

## Prossimi Miglioramenti

1. Reminder piu intelligenti (non solo 48h)
2. Report settimanale SNCP health
3. Integrazione con spawn-workers (worker aggiornano SNCP)

---

*"L'automazione ci libera dalla disciplina"*
