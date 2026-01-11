# ANALISI PROBLEMA DEPLOY - Sessione 152

> **Data:** 10 Gennaio 2026
> **Sessione:** 152
> **Problema:** cervella-devops si è bloccato al primo tentativo

---

## COSA È SUCCESSO

### Primo Tentativo Deploy
**Risposta cervella-devops:**
```
DOMANDA OBBLIGATORIA A RAFA:

1. PATH ERRATO: Sono su CervellaSwarm, ma i file sono su Miracollo
2. FILE NON TROVATI: Nessun file locale esiste per il deploy
3. PERMESSO DEPLOY PRODUZIONE non esplicito

STATUS: BLOCKED
```

### Ma i File ESISTEVANO!
Verifica successiva:
```
/Users/rafapra/Developer/miracollogeminifocus/backend/database/migrations/031_pricing_tracking.sql ✅
/Users/rafapra/Developer/miracollogeminifocus/backend/services/pricing_tracking_service.py ✅
/Users/rafapra/Developer/miracollogeminifocus/backend/routers/pricing_tracking.py ✅
```

### Secondo Tentativo
Dopo aver confermato esplicitamente che i file esistono, deploy OK.

---

## PERCHÉ È SUCCESSO

### 1. Contesto Progetto Confuso
- La sessione è su **CervellaSwarm** (working directory)
- Ma i file da deployare sono su **Miracollo**
- cervella-devops non ha trovato i file perché cercava nel path sbagliato?

### 2. Prompt Non Abbastanza Esplicito
Il primo prompt diceva:
```
**FILE DA DEPLOYARE:**
- `backend/database/migrations/031_pricing_tracking.sql`
```

Ma non specificava il PATH ASSOLUTO completo.

### 3. Mancava Conferma Esplicita File
cervella-devops voleva conferma che i file esistevano PRIMA di procedere.
Questo è GIUSTO come comportamento FORTEZZA MODE!

---

## LEZIONI APPRESE

### 1. Sempre PATH ASSOLUTI nei Prompt Deploy
```
# SBAGLIATO
backend/database/migrations/031_pricing_tracking.sql

# GIUSTO
/Users/rafapra/Developer/miracollogeminifocus/backend/database/migrations/031_pricing_tracking.sql
```

### 2. Verificare File PRIMA di Lanciare Deploy
La Regina dovrebbe:
1. Verificare con Glob/Read che i file esistono
2. Poi lanciare cervella-devops con conferma esplicita

### 3. Il Comportamento di cervella-devops Era Corretto!
Chiedere conferma PRIMA di toccare produzione è GIUSTO.
È FORTEZZA MODE fatto bene!
Il "problema" era nel prompt, non nell'agente.

---

## AZIONI CORRETTIVE

### Per la Regina (me):
1. **Sempre verificare file esistono** prima di lanciare deploy
2. **Usare path assoluti** nei prompt per devops
3. **Confermare esplicitamente** "i file esistono, permesso dato"

### Per i Prompt Devops:
Aggiungere template:
```
**CONFERMA PRE-DEPLOY:**
- File verificati con Glob: ✅
- Path assoluto: /Users/rafapra/Developer/[progetto]/...
- Permesso Rafa: ✅

PROCEDI CON FORTEZZA MODE.
```

### Per Documentazione:
Aggiungere in `FORTEZZA_MODE.md`:
- Sezione "Pre-Deploy Checklist per Regina"
- Verifica file esistenti PRIMA di lanciare agente

---

## RISULTATO FINALE

Il deploy è andato a buon fine al secondo tentativo.
Non c'era un bug, ma una **comunicazione migliorabile**.

cervella-devops ha fatto BENE a chiedere conferma!
È esattamente lo spirito FORTEZZA MODE.

---

*"Ogni problema è un'opportunità di miglioramento"*
*"FORTEZZA MODE = Mai fretta, sempre verificare"*
