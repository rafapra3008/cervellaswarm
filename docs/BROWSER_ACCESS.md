# Browser Access - CervellaSwarm v4.0.0

> Worker che possono navigare il web autonomamente

## Overview

A partire da v4.0.0, alcuni worker CervellaSwarm hanno accesso a Playwright MCP per navigare il web.

## Worker con Browser Access

| Worker | Browser Access | Use Cases |
|--------|---------------|-----------|
| cervella-researcher | SI | Documentazione tecnica, ricerca, analisi siti |
| Altri worker | NO | Non necessario per il loro lavoro |

## Come Funziona

1. `spawn-workers.sh` rileva se il worker ha browser access
2. Inietta `--mcp-config` con la configurazione Playwright
3. Il worker riceve i browser tools nel suo contesto

## Configurazione

File: `~/.claude/mcp-configs/researcher.json`

```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest",
        "--browser", "chromium",
        "--headless"
      ]
    }
  }
}
```

## Browser Tools Disponibili

Il worker con browser access ha questi tools:

- `browser_navigate` - Vai a URL
- `browser_snapshot` - Cattura stato pagina (accessibility tree)
- `browser_click` - Click su elemento
- `browser_type` - Digita testo
- `browser_press_key` - Premi tasto
- `browser_scroll` - Scorri pagina

## Uso Corretto

**QUANDO USARE:**
- Navigare documentazione ufficiale (docs.python.org, react.dev, etc.)
- Verificare esempi live
- Analizzare struttura siti tecnici
- Raccogliere informazioni da pagine web

**QUANDO NON USARE:**
- Search generici (usa WebSearch invece)
- Siti che richiedono autenticazione
- Scraping massivo
- Siti non correlati al task

## Security

- Headless mode: nessuna finestra visibile
- Prima esecuzione scarica Chromium (~400MB)
- I browser tools consumano context tokens

## Estendere ad Altri Worker

Per aggiungere browser access a un altro worker:

1. Modifica `BROWSER_ACCESS_WORKERS` in `spawn-workers.sh`:
   ```bash
   BROWSER_ACCESS_WORKERS="researcher marketing"
   ```

2. (Opzionale) Crea config MCP specifica per il worker

## Troubleshooting

**Browser non si avvia:**
```bash
# Verifica che Playwright MCP funzioni
npx -y @playwright/mcp@latest --help
```

**Chromium non installato:**
```bash
# Scarica Chromium (automatico al primo uso)
npx playwright install chromium
```

---

*CervellaSwarm v4.0.0 - Browser Access MVP*
*Cervella & Rafa - Sessione 312*
