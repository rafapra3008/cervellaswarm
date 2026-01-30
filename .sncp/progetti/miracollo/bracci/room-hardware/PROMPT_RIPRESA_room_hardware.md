# PROMPT RIPRESA - Room Hardware

> **Ultimo aggiornamento:** 30 Gennaio 2026 - Sessione 321
> **Braccio 3 dell'ecosistema Miracollo**

---

## STATO IN UNA RIGA

**BLOCCATI su accesso VLAN 1101. Rafa sta cercando admin UniFi o FortiGate.**

---

## PROBLEMA ATTUALE

```
Rafa ha VIEW-ONLY su UniFi → non può creare WiFi VLAN 1101
FortiGate GUI disabilitata dalla rete → non può creare firewall rule
Serve: Admin UniFi OPPURE Admin FortiGate
```

---

## NUCLEUS CUSTODE (Target Test)

```
Nome:     rcu-Custode-1
IP:       10.0.101.12
MAC:      00:08:0C:20:1F:6D
VLAN:     VDA CAMERE (ID 1101)
Porta:    Armadio P2, Port 47
Modello:  H155300 v1.4
```

---

## STRUTTURA RETE VDA

```
VLAN 1101 "VDA CAMERE" (10.0.101.0/24)
├── rcu-Custode-1 (10.0.101.12) ← TARGET TEST
├── Altri NUCLEUS camere
└── Isolata dalle altre VLAN
```

---

## PORTE MODBUS NUCLEUS

```
M1: OCCUPATA | M2: LIBERA ← usabile! | M3: OCCUPATA | M4: OCCUPATA
NOTA: Connettori RJ11, non morsetti. Per RS-485 serve cavo RJ11.
```

---

## DUE VIE DI COMUNICAZIONE

| Via | Metodo | Note |
|-----|--------|------|
| ETH (RJ45) | Modbus TCP porta 502 | PREFERITA - serve accesso VLAN |
| M1-M4 (RJ11) | Modbus RS-485 | BACKUP - cavo fisico diretto |

---

## PROSSIMI STEP

1. [ ] **Rafa ottiene admin** (UniFi o FortiGate)
2. [ ] Creare accesso VLAN 1101 (WiFi o Firewall Rule)
3. [ ] Test Modbus TCP porta 502
4. [ ] Scan tutti i NUCLEUS hotel
5. [ ] Mappatura registri → Rosetta Stone

---

## OPZIONI VELOCI (senza admin)

| Opzione | Costo | Note |
|---------|-------|------|
| Porta Switch Diretta | 0€ | Devi stare in armadio P2 |
| TP-Link TL-SG108E | 30€ | Switch managed economico |
| Cavo RJ11 RS-485 | 3€ | Backup fisico |

---

## ARCHIVIO

Dettagli sessione 311: `archivio/ARCHIVIO_S311_dettagli.md`
Studio VLAN completo: `studi/STUDIO_VLAN_1101_ACCESSO_COMPLETO.md`

---

*Braccio 3 - Automazione Stanze*
*"Non esistono cose difficili, esistono cose non studiate!"*
