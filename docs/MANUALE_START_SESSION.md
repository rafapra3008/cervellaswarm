# Manuale start-session

> Script per avviare sessioni Claude su qualsiasi progetto

---

## Comandi

```bash
# Vedi tutti i progetti
start-session --list

# Avvia sessione
start-session cervellaswarm
start-session miracollo
start-session contabilita
start-session cervellacostruzione
```

---

## Cosa Fa

1. Mostra preview PROMPT_RIPRESA (prime 30 righe)
2. Cambia directory al progetto
3. Avvia Claude Code

---

## Aggiungere Nuovo Progetto

Modifica `scripts/start-session.sh`:

```bash
# 1. Aggiungi path in get_project_path()
get_project_path() {
    case "$1" in
        ...
        nuovoprogetto) echo "/Users/rafapra/Developer/nuovoprogetto" ;;
    esac
}

# 2. Aggiungi descrizione in get_project_desc()
get_project_desc() {
    case "$1" in
        ...
        nuovoprogetto) echo "Descrizione progetto" ;;
    esac
}

# 3. Aggiungi alla lista PROJECTS
PROJECTS="... nuovoprogetto"
```

---

## Requisiti

- PROMPT_RIPRESA in: `CervellaSwarm/.sncp/progetti/{progetto}/PROMPT_RIPRESA_{progetto}.md`
- Directory progetto esistente

---

## Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| `command not found` | `source ~/.zshrc` |
| RIPRESA non trovato | Crea con `sncp-init.sh` |
| Progetto non in lista | Aggiungi a `start-session.sh` |

---

*Creato: Sessione 333 - 3 Febbraio 2026*
