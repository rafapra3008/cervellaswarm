# LEZIONE: Verifica Tools nel DNA Prima di Copiare Template

> **Data:** 10 Gennaio 2026
> **Sessione:** 146
> **Categoria:** DNA Agenti

---

## Cosa E' Successo

Il DNA di `cervella-reviewer` conteneva istruzioni per:
- Eseguire script bash
- Scrivere file output

Ma il reviewer ha solo: `Read, Glob, Grep, WebSearch`

**NON ha:** Bash, Write, Edit

Risultato: Errori "No such tool available: Bash"

---

## Perche' E' Successo

Le istruzioni erano state copiate da un template generico senza verificare la compatibilita' con i tool dichiarati.

---

## Cosa Abbiamo Imparato

> **"DNA e Tools devono essere COERENTI"**

Quando si copia un template DNA:
1. Verificare i `tools:` dichiarati nel frontmatter
2. Assicurarsi che le istruzioni usino SOLO quei tool
3. Testare con un task semplice prima di usare in produzione

---

## Fix Applicato

Aggiunta sezione "COME LAVORO (Read-Only)" che spiega come il reviewer lavora con i suoi tool limitati.

---

## Come Evitarlo in Futuro

1. **Checklist DNA:** Sempre verificare coerenza istruzioni-tools
2. **Test di base:** Prima task con nuovo agente = task semplice
3. **Documentazione tool:** Ogni DNA deve avere lista tool ben visibile

---

*"Prima leggi cosa puoi fare, poi scrivi come farlo"*
