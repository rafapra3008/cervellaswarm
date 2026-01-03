# TASK: Verificare task_manager.py creato da Backend

## METADATA
- ID: TASK_002
- Assegnato a: cervella-tester
- Livello rischio: 1 (BASSO - solo test, nessuna modifica)
- Timeout: 10 minuti
- Creato: 2026-01-03 14:25
- Dipende da: TASK_001 (completato)

## PERCHE
Backend ha creato task_manager.py. Ora dobbiamo verificare che funzioni correttamente.
Questo e il secondo step del flusso Backend -> Tester.

## CRITERI DI SUCCESSO
- [ ] Script esiste e e eseguibile
- [ ] Tutti i comandi CLI funzionano
- [ ] Edge cases gestiti correttamente
- [ ] Nessun bug critico trovato
- [ ] Report test scritto

## FILE DA VERIFICARE
- scripts/swarm/task_manager.py

## CHI VERIFICHERA
N/A (questo E il task di verifica)

## DETTAGLI

### Test da Eseguire

1. **Verifica esistenza e permessi**
   ```bash
   ls -la scripts/swarm/task_manager.py
   ```

2. **Test help**
   ```bash
   python3 scripts/swarm/task_manager.py
   python3 scripts/swarm/task_manager.py --help 2>/dev/null || echo "No --help"
   ```

3. **Test list**
   ```bash
   python3 scripts/swarm/task_manager.py list
   ```

4. **Test create + ready + done flow**
   ```bash
   python3 scripts/swarm/task_manager.py create TASK_TEST_002 cervella-tester "Test automatico" 1
   python3 scripts/swarm/task_manager.py ready TASK_TEST_002
   python3 scripts/swarm/task_manager.py status TASK_TEST_002
   python3 scripts/swarm/task_manager.py done TASK_TEST_002
   python3 scripts/swarm/task_manager.py status TASK_TEST_002
   python3 scripts/swarm/task_manager.py cleanup TASK_TEST_002
   ```

5. **Test edge cases**
   ```bash
   # Task non esistente
   python3 scripts/swarm/task_manager.py status TASK_NON_ESISTE

   # Comando invalido
   python3 scripts/swarm/task_manager.py comando_invalido
   ```

### Output Atteso

Scrivi un report in `.swarm/tasks/TASK_002_output.md` con:
- Risultato ogni test (PASS/FAIL)
- Bug trovati (se presenti)
- Suggerimenti miglioramento
- Valutazione finale (APPROVATO/RESPINTO)
