# Ricerca: Risparmio Costi GPU su GCP 2026

**Data**: 11 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Contesto**: VM n1-standard-4 + T4 GPU in us-west1-b
**Costo attuale**: ~$0.56/ora = ~$400/mese on-demand

---

## Executive Summary

**Risparmio potenziale massimo**: 60-91% con Spot VMs
**Opzione raccomandata**: Combinazione Spot VMs (development) + Schedule automation

---

## 1. CUD (Committed Use Discount) - GPU

### Come Funziona
- Impegno contrattuale 1 o 3 anni
- **IMPORTANTE**: Per GPU serve **Resource-based CUD** + **Reservation obbligatoria**
- NO Flexible CUD per GPU (limitazione GCP)

### Risparmi
- **1 anno**: ~37% risparmio
- **3 anni**: fino a 55% risparmio su resource-based CUD

### Pro
- Sconto garantito e prevedibile
- Fatturazione costante
- Nessun rischio di preemption

### Contro
- **Reservation obbligatoria**: devi riservare le GPU specifiche quando acquisti il CUD
- Impegno a lungo termine (1-3 anni)
- Meno flessibilità rispetto a CPU/RAM (no Flexible CUD)
- Paghi anche se non usi la VM

### Calcolo Risparmio
- **Baseline**: $400/mese on-demand
- **CUD 1 anno (37%)**: ~$250/mese → risparmio $150/mese ($1,800/anno)
- **CUD 3 anni (55%)**: ~$180/mese → risparmio $220/mese ($2,640/anno)

**⚠️ ATTENZIONE**: Devi confermare se il tuo progetto userà T4 GPU costantemente per 1-3 anni.

---

## 2. Spot VMs (ex Preemptible)

### Come Funziona
- VM con capacità non garantita
- GCP può "preemptare" (spegnere) in qualsiasi momento
- Pricing dinamico (aggiornato ~ogni giorno)

### Risparmi
- **60-91% sconto** rispetto a on-demand
- T4 GPU Spot: da $0.09 a $0.27/ora (vs ~$0.35-0.95 on-demand)
- **NO Sustained Use Discount** su Spot VMs

### Pro
- Risparmio ENORME (massimo disponibile su GCP)
- Nessun impegno a lungo termine
- Perfetto per workload tolleranti a interruzioni

### Contro
- **Preemption risk**: VM può essere spenta con preavviso di 30 secondi
- Capacità non garantita (potrebbe non essere disponibile)
- Richiede architettura fault-tolerant (checkpoint, retry logic)

### Calcolo Risparmio
- **Baseline**: $400/mese on-demand
- **Spot (70% sconto medio)**: ~$120/mese → risparmio $280/mese ($3,360/anno)
- **Spot (90% sconto best case)**: ~$40/mese → risparmio $360/mese ($4,320/anno)

**⚠️ RISCHIO**: Se il tuo workload richiede disponibilità 24/7, Spot non è adatto.

---

## 3. Sustained Use Discount (SUD)

### Come Funziona
- **AUTOMATICO** - applicato da GCP senza azione richiesta
- Se usi una risorsa >25% del mese → sconto progressivo
- Per GPU: **30% sconto** se usi 1 GPU per tutto il mese

### Risparmi
- **30% massimo** per GPU T4 su N1 machines
- Applicato automaticamente come credito mensile
- Sconto incrementale (più usi, più risparmi)

### Pro
- ZERO configurazione
- Nessun impegno contrattuale
- Si applica automaticamente

### Contro
- **NON si applica a**:
  - Spot VMs
  - A100, H100, L4 GPUs (solo N1-compatible GPUs come T4)
  - Accelerator-optimized machines
- Sconto massimo 30% (meno di CUD o Spot)
- Devi usare la VM >25% del mese per qualificarti

### Calcolo Risparmio
- **Baseline**: $400/mese on-demand
- **SUD (30%)**: ~$280/mese → risparmio $120/mese ($1,440/anno)

**✅ BONUS**: Se NON usi Spot e NON usi CUD, ricevi SUD GRATIS automaticamente!

---

## 4. Schedule Start/Stop

### Come Funziona
- Automatizza accensione/spegnimento VM su schedule
- Due approcci:
  1. **Instance Schedules** (nativo GCP, aggiornato Gen 2026)
  2. **Cloud Scheduler + Cloud Functions** (custom logic)

### Risparmi
- Dipende da quanto tempo la VM è SPENTA
- Esempio: Dev environment solo business hours (9-17 Mon-Fri)
  - 40 ore/settimana usage vs 168 ore/settimana
  - **76% di tempo spento** → 76% risparmio!

### Pro
- Nessun downside (paghi solo quando accesa)
- Perfetto per dev/test environments
- Facile da implementare (Instance Schedules nativo)
- Combinabile con altre strategie

### Contro
- ⚠️ Startup time: VM può impiegare fino a 15 min per avviarsi dopo schedule
- Richiede workload prevedibile (non 24/7 production)
- Devi ricordare di programmare gli schedule

### Calcolo Risparmio (Dev Environment)
- **Scenario**: Solo business hours (40h/settimana vs 168h/settimana)
- **Baseline**: $400/mese on-demand 24/7
- **Scheduled (76% downtime)**: ~$95/mese → risparmio $305/mese ($3,660/anno)

**✅ BEST FOR**: Development, testing, training batch jobs.

---

## 5. Altre Opzioni di Risparmio

### A. Rightsizing
- Verifica se n1-standard-4 è necessario o se basta n1-standard-2
- Risparmio potenziale: 30-50% su VM costs (NON GPU)

### B. Regional Selection
- us-west1 non è la region più economica
- Considera us-central1 o us-east1 (leggermente cheaper)
- Risparmio: 5-10% su alcune risorse

### C. Persistent Disk Optimization
- Usa SSD solo se necessario
- Standard persistent disk è ~70% più economico
- Elimina snapshot non usati

### D. Combinazione GPU + CPU CUD
- Puoi avere CUD separati per CPU e GPU
- Risparmio cumulativo su entrambe le risorse

---

## Confronto Opzioni - Tabella Riepilogativa

| Opzione | Risparmio | Rischio | Impegno | Complessità | Best For |
|---------|-----------|---------|---------|-------------|----------|
| **CUD 1 anno** | 37% (~$150/mese) | Basso | 1 anno | Media (serve reservation) | Production 24/7 stabile |
| **CUD 3 anni** | 55% (~$220/mese) | Basso | 3 anni | Media (serve reservation) | Lungo termine certo |
| **Spot VMs** | 60-91% (~$280/mese) | Alto | Nessuno | Alta (fault tolerance) | Dev, batch, training |
| **SUD** | 30% (~$120/mese) | Nullo | Nessuno | Zero (automatico) | Qualsiasi (free bonus) |
| **Schedule Start/Stop** | 70-90% (~$305/mese) | Nullo | Nessuno | Bassa | Dev/test non 24/7 |

**Note**:
- I risparmi NON sono cumulativi (CUD + SUD = NO, scegli uno)
- Schedule è cumulativo con qualsiasi opzione (spegni VM = zero costi)
- Spot esclude SUD automaticamente

---

## Raccomandazione Finale

### Strategia Multi-Layer (Massimo Risparmio)

```
┌─────────────────────────────────────────────────┐
│ PRODUCTION (24/7)                               │
│ → CUD 1 anno (37% risparmio)                    │
│ → Baseline stabile per workload critico         │
│                                                  │
│ Costo: ~$250/mese                               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ DEVELOPMENT / TESTING                           │
│ → Spot VMs (70-90% risparmio)                   │
│ → + Schedule Start/Stop (business hours only)   │
│ → Checkpoint training jobs ogni 30 min          │
│                                                  │
│ Costo: ~$40-120/mese (quando acceso)            │
│ Costo effettivo: ~$10-30/mese (con schedule)    │
└─────────────────────────────────────────────────┘
```

### Opzione Conservativa (Basso Rischio)
Se il workload è **production-critical 24/7**:
1. **CUD 1 anno** → risparmio garantito 37% ($150/mese)
2. Valuta CUD 3 anni dopo 6 mesi se tutto stabile

### Opzione Aggressiva (Massimo Risparmio)
Se il workload è **tolerante a interruzioni**:
1. **Spot VMs** per dev/test → risparmio 70-90%
2. **Schedule Start/Stop** per business hours only
3. **Risparmio combinato**: ~$360/mese (90% totale)

### Quick Win Immediato
**OGGI puoi fare**:
1. ✅ Implementa Schedule Start/Stop (se dev/test) → 15 min setup
2. ✅ SUD si applica AUTOMATICAMENTE (già attivo se usi >25% mese)
3. ✅ Test Spot VM su ambiente non-critico → 30 min test

**PROSSIMA SETTIMANA**:
1. Analizza pattern di utilizzo effettivo (24/7 o part-time?)
2. Decidi: CUD (stabile) vs Spot (flessibile)
3. Implementa strategia scelta

---

## Implementation Checklist

### Per Schedule Start/Stop (Quick Win)
```bash
# Opzione 1: Instance Schedules (Nativo GCP)
gcloud compute resource-policies create instance-schedule dev-hours \
    --vm-start-schedule='0 9 * * 1-5' \
    --vm-stop-schedule='0 17 * * 1-5' \
    --timezone='America/Los_Angeles' \
    --region=us-west1

gcloud compute instances add-resource-policies YOUR-INSTANCE-NAME \
    --resource-policies=dev-hours \
    --zone=us-west1-b
```

### Per Spot VM (Test)
```bash
# Crea Spot VM con stessa config
gcloud compute instances create test-spot-vm \
    --zone=us-west1-b \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP
```

### Per CUD (Impegno)
1. Vai a: Console GCP → Compute Engine → Committed use discounts
2. Seleziona: Resource-based
3. Configura: T4 GPU + Region us-west1 + Duration (1 o 3 anni)
4. **CREA RESERVATION** (obbligatorio per GPU)

---

## Fonti e Riferimenti

**GCP Documentazione Ufficiale (2026)**:
- CUD Overview: docs.cloud.google.com/compute/docs/instances/committed-use-discounts-overview
- Spot VMs Pricing: cloud.google.com/spot-vms/pricing
- GPU Pricing: cloud.google.com/compute/gpus-pricing
- Sustained Use Discounts: docs.cloud.google.com/compute/docs/sustained-use-discounts
- Instance Scheduling (aggiornato Gen 2026): docs.cloud.google.com/compute/docs/instances/schedule-instance-start-stop

**Best Practices**:
- Google Cloud Blog: Save money by scheduling Compute Engine instances
- ProsperOps: Google Cloud Sustained Use Discounts Guide
- Cast.AI: GCP CUD Optimization Strategies

---

## Note Finali

- **Pricing è dinamico**: Verifica sempre prezzi attuali su cloud.google.com/compute/gpus-pricing
- **Spot pricing varia**: Può cambiare giornalmente, monitora trend
- **CUD require commitment**: Analizza 3-6 mesi di usage prima di committal lungo termine
- **Combinazioni intelligenti**: Spot per dev + CUD per prod = massimo risparmio globale

**Prossimo step suggerito**: Analizza i log di utilizzo degli ultimi 30 giorni per decidere tra CUD (usage costante) o Spot+Schedule (usage variabile).

---

*Report completato: 11 Gennaio 2026*
*Cervella Researcher - CervellaSwarm*
