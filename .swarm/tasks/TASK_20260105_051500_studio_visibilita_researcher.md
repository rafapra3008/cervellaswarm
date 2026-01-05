# Task: Studio Visibilita Worker - Ricerca Tecnica

**Assegnato a:** cervella-researcher
**Stato:** ready
**Priorita:** ALTA
**Data:** 05 January 2026
**Creato da:** Regina (Sessione 91)

---

## Obiettivo

Studiare come implementare VISIBILITA' REAL-TIME per i worker dello swarm.

---

## Il Problema

```
Oggi lavoriamo "al buio":
- Sappiamo quando worker INIZIA (spawn)
- Sappiamo quando worker FINISCE (cleanup)
- NON SAPPIAMO cosa fa MENTRE lavora!

Questo e' un problema CRITICO per un sistema professionale.
```

---

## Domande da Rispondere

1. **Log Real-Time**: Come fare streaming del log mentre il worker lavora?
   - tail -f funziona? Come integrarlo?
   - Il buffer di Claude quando si svuota?

2. **Heartbeat**: Come sapere se il worker e' vivo e cosa sta facendo?
   - File heartbeat con timestamp?
   - File stato con "cosa sto facendo"?

3. **Progresso**: Come mostrare quanto manca?
   - Progress file periodico?
   - Percentuale completamento?

4. **Notifiche**: Come avvisare di problemi?
   - Notifiche macOS?
   - Webhook?

5. **Dashboard**: Come visualizzare tutto insieme?
   - swarm-watch command?
   - Dashboard ASCII?
   - Refresh periodico?

---

## Cosa Cercare

1. Come altri sistemi multi-agent gestiscono la visibilita'
2. Pattern per real-time monitoring di processi CLI
3. Limitazioni di Claude Code (buffer, output, ecc.)
4. Soluzioni macOS native (osascript, notifiche)

---

## Output Atteso

Scrivi in `TASK_20260105_051500_studio_visibilita_researcher_output.md`:

1. **Analisi del problema** (cosa blocca oggi)
2. **Soluzioni trovate** (almeno 3 approcci)
3. **Pro/Contro** di ogni approccio
4. **Raccomandazione** (quale implementare prima)
5. **Piano implementazione** (step concreti)

---

## Checklist Verifica

- [ ] Almeno 3 soluzioni studiate
- [ ] Pro/contro per ogni soluzione
- [ ] Raccomandazione chiara
- [ ] Piano implementazione concreto
- [ ] Output scritto in _output.md
- [ ] File .done creato

---

*Task creato dalla Regina - Sessione 91*
*"Lavorare al buio e' difficile!" - Rafa*
