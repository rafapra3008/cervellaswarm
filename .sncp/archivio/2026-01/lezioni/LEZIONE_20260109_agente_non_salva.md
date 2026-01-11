# LEZIONE: Agente Researcher Non Salva File

> **Data:** 9 Gennaio 2026 - Sessione 141
> **Tipo:** Bug/Problema

---

## Cosa È Successo

cervella-researcher ha detto di aver creato 2 file:
- `RICERCA_CLAUDE_CODE_PARTE1_SUBAGENTS.md`
- `RICERCA_CLAUDE_CODE_PARTE2_PLUGINS.md`

Ma i file NON esistono.

---

## Possibili Cause

1. **Permessi Write tool** - L'agente potrebbe non avere il tool Write
2. **Path errato** - Ha scritto in un path diverso
3. **Errore silenzioso** - Il tool ha fallito senza errore visibile
4. **Hallucination** - L'agente ha detto di aver fatto ma non ha fatto

---

## Da Investigare

- [ ] Verificare quali tools ha cervella-researcher
- [ ] Verificare se il path era corretto
- [ ] Aggiungere logging ai salvataggi
- [ ] Testare l'agente con task semplice di scrittura

---

## Workaround Usato

Ho fatto io (Regina) la ricerca direttamente e salvato il documento.

---

*Da sistemare in sessione futura*
