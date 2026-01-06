# Task: Fix Security - Escape Notifiche

**Assegnato a:** cervella-backend
**Stato:** pending
**Data:** 6 Gennaio 2026
**Priorita:** ALTA

## Problema

Code Review 6 Gen 2026 ha trovato 2 issue di sicurezza minori:

### Issue 1: context_check.py
- **Linee:** 48-60
- **Problema:** `escape_applescript` manuale
- **Fix:** Usare `shlex.quote()` per sicurezza extra

### Issue 2: auto_review_hook.py  
- **Linee:** 143-148
- **Problema:** Notifica con stringa non escaped
- **Fix:** Escape `title` e `message` con shlex.quote()

## Output

Modifica i due file e verifica che le notifiche funzionino ancora.

## Note

Non sono blocker ma vanno fixati per security best practice.
