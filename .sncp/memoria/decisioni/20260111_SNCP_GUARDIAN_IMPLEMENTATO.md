# Decisione: SNCP Guardian Implementato

> **Data:** 11 Gennaio 2026
> **Sessione:** 164
> **Tipo:** Infrastruttura Critica

---

## Cosa

SNCP Guardian multi-layer implementato per risolvere DEFINITIVAMENTE il problema della manutenzione SNCP.

## Perche

- SNCP e' il sistema centrale dei progetti
- Ogni 10-15 sessioni serviva pulizia manuale
- "Se il sistema centrale non funziona, tutto soffre" (Rafa)
- Struttura v3.0 definita ma non enforzata

## Componenti Implementati

### 1. Validator (`~/.claude/scripts/sncp_validator.py`)
- Valida struttura path
- Valida naming convention (YYYYMMDD_nome.md)
- Messaggi di errore chiari con suggerimenti
- Exit code 0/1 per automazione

### 2. Auto-Archiver (`~/.claude/scripts/sncp_auto_archiver.py`)
- Archivia file > 30 giorni in archivio/YYYY-MM/
- Esegue ogni notte alle 2am (cron)
- Log in /tmp/sncp_archiver.log
- Processa tutti e 3 i progetti

### 3. DNA Agenti Upgrade
- 16 agenti aggiornati con regole SNCP v3.0
- Template path precisi
- Errori comuni documentati
- Warning su Guardian attivo

### 4. Cron Job
```
0 2 * * * /usr/bin/python3 ~/.claude/scripts/sncp_auto_archiver.py >> /tmp/sncp_archiver.log 2>&1
```

## Risultato Atteso

- Zero manutenzione manuale SNCP
- Agenti rispettano struttura automaticamente
- Archiving automatico notturno
- ROI: ~24h/anno risparmiate

## File Creati

| File | Descrizione |
|------|-------------|
| `~/.claude/scripts/sncp_validator.py` | Validator struttura e naming |
| `~/.claude/scripts/sncp_auto_archiver.py` | Archiver automatico |
| `~/.claude/scripts/sncp_dna_template.md` | Template per DNA agenti |

## Ricerca di Base

`.sncp/idee/20260111_RICERCA_SNCP_AUTO_MANTENUTO.md`

---

*"Il sistema centrale DEVE funzionare!"*
*"Automazione > Disciplina manuale"*

*Implementato da: Regina CervellaSwarm*
*Sessione 164 - 11 Gennaio 2026*
