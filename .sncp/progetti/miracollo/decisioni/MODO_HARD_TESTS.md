# MODO HARD TESTS - Framework Testing Miracollo

> **Creato:** 11 Gennaio 2026 - Sessione 158
> **Ispirato da:** Test ML Pipeline End-to-End che ha portato a R2=0.693!
> **Filosofia:** "Testare con coscienza, non con paura"

---

## Quando Attivare MODO HARD TESTS

| Trigger | Esempio |
|---------|---------|
| Nuova feature critica | ML Pipeline, Payment Integration |
| Bug misterioso | "Funziona in locale ma non in prod" |
| Prima di release major | v10.0.0, v11.0.0 |
| Dopo refactoring grosso | Database migration, API redesign |
| Rafa dice "testa tutto" | Carta bianca per sporcare |

---

## Le 10 Regole d'Oro

### 1. PREPARA PRIMA DI TOCCARE
```
- Leggi logs attuali (baseline)
- Verifica health check
- Salva stato DB se serve rollback
- Documenta "cosa funziona ORA"
```

### 2. UN PASSO ALLA VOLTA
```
Non fare: Fix 5 cose → deploy → test tutto
Fai: Fix 1 cosa → deploy → test → repeat
```

### 3. CURL È IL TUO MIGLIORE AMICO
```bash
# Prima di ogni test
curl -s "https://miracollo.com/health"

# Test specifico
curl -s "https://miracollo.com/api/endpoint?params"

# Logs dopo
ssh miracollo-cervella "docker logs --tail=50 backend"
```

### 4. DATI TEST = REALISTICI MA TRACCIABILI
```
- Usa prefissi: sugg_prezzo_test_001, bucco_test_2026-01-15
- Mai mischiare con dati utente reali
- Pulisci dopo se possibile
- OK sporcare in fase test (Rafa approva)
```

### 5. FIX → DEPLOY → TEST → REPEAT
```
Loop rapido:
1. Trova errore nei logs
2. Fix minimale (1 riga se possibile)
3. git commit && git push
4. Attendi deploy (30s GitHub Actions)
5. Re-test con curl
6. Se fallisce → torna a 1
```

### 6. DOCUMENTA MENTRE FAI
```
- TODO list attiva (TodoWrite tool)
- Aggiorna ogni completamento
- Screenshot/log degli errori importanti
```

### 7. LOGS SONO ORO
```bash
# Logs in tempo reale
ssh miracollo-cervella "docker compose logs -f backend"

# Filtra per keyword
ssh miracollo-cervella "docker logs backend | grep -i error"

# Ultimi N lines
ssh miracollo-cervella "docker logs --tail=100 backend"
```

### 8. SE ROMPI, SAI ROLLBACK
```bash
# Git rollback
git revert HEAD && git push

# Docker rollback (se serve)
ssh miracollo-cervella "docker rollout undo backend"

# DB rollback (backup prima!)
# Restore da backup pre-test
```

### 9. FESTEGGIA I SUCCESSI INTERMEDI
```
- API risponde 200? Log it!
- Un test passa? Mark completed!
- Pipeline non crasha? Ottimo!
- Mantieni morale alto durante debug
```

### 10. CHIUDI CON CHECKPOINT COMPLETO
```
- SNCP aggiornato (oggi.md)
- PROMPT_RIPRESA aggiornato
- git commit con dettagli
- Handoff per prossima sessione
```

---

## Checklist Pre-Test

```
[ ] Health check OK?
[ ] Logs baseline salvati?
[ ] Backup DB (se critico)?
[ ] TODO list creata?
[ ] Rafa informato (se serve)?
```

## Checklist Post-Test

```
[ ] Tutti i test passano?
[ ] Logs puliti (no errori)?
[ ] Documentazione aggiornata?
[ ] Dati test puliti (o marcati)?
[ ] Commit finale fatto?
```

---

## Pattern Testati (Sessione 158)

### Pattern: Test API Sequenziale
```bash
# 1. Verifica stato iniziale
curl -s "https://miracollo.com/api/ml/training-stats?hotel_id=1"

# 2. Esegui azione
curl -s -X POST "https://miracollo.com/api/revenue/suggestions/ID/action" \
  -H "Content-Type: application/json" \
  -d '{"action": "accept", "bucco_id": "bucco_2026-01-11"}'

# 3. Verifica effetto
curl -s "https://miracollo.com/api/pricing/history?hotel_id=1"

# 4. Check logs per errori
ssh miracollo-cervella "docker logs --tail=20 backend"
```

### Pattern: Inserimento Dati Test via Python
```bash
ssh miracollo-cervella "docker compose exec -T backend python3 << 'PYEOF'
import sqlite3
conn = sqlite3.connect('/app/backend/data/miracollo.db')
# ... insert test data ...
conn.commit()
print(f'Records inserted: {count}')
PYEOF
"
```

### Pattern: Debug Iterativo
```
1. curl fallisce con errore X
2. Leggi codice per capire
3. Fix minimale
4. git add && git commit && git push
5. sleep 30 (attendi deploy)
6. Re-curl
7. Se nuovo errore → repeat
8. Se OK → next test
```

---

## Metriche di Successo

| Metrica | Target | Sessione 158 |
|---------|--------|--------------|
| Deploy senza downtime | 100% | 100% |
| Test passati | >90% | ~85% (fix iterativi) |
| Tempo fix medio | <10 min | ~5 min |
| Rollback necessari | 0 | 0 |
| Documentazione | Completa | Completa |

---

## Cosa Abbiamo Imparato (Sessione 158)

1. **SQLite restituisce stringhe** - Sempre convertire a float/int
2. **Column alias importanti** - `changed_at as change_date`
3. **Dati test devono matchare FK** - suggestion_id deve esistere
4. **500 non sempre = fallimento** - Controlla se l'azione è avvenuta
5. **Logs > Response** - I logs dicono più dell'API response

---

## Quote della Sessione

> "La magia ora è con coscienza!"

> "Testare con coscienza, non con paura"

> "Un fix alla volta, un deploy alla volta, un test alla volta"

---

*Framework creato dopo sessione di test ML Pipeline*
*R2=0.693 raggiunto grazie a questo approccio*

*Cervella & Rafa - Gennaio 2026*
