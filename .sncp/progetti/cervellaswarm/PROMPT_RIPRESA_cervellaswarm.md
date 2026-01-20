# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 305
> **STATUS:** Security fixes + Stripe $29/$49 + Sync pubblico COMPLETATO!

---

## SESSIONE 305 - SECURITY + STRIPE + SYNC

```
+================================================================+
|   TUTTI I TASK COMPLETATI!                                     |
|                                                                |
|   - README.md: 17 agents + Architect                           |
|   - AGENTS_REFERENCE.md: sezione Architect aggiunta            |
|   - API: rate limiting + debug endpoints rimossi               |
|   - Stripe: $29 PRO / $49 TEAM (nuovi price_id)               |
|   - Repo pubblico: SINCRONIZZATO                               |
|                                                                |
+================================================================+
```

---

## COSA FATTO SESSIONE 305

### Documentazione
| File | Fix |
|------|-----|
| README.md (root) | 16 → 17 agents, Architect in tabella |
| docs/AGENTS_REFERENCE.md | 16 → 17, sezione Architect completa |

### Security (API Fly.io)
| Fix | Dettaglio |
|-----|-----------|
| Rate limiting | 100 req/15min per IP (express-rate-limit) |
| Debug endpoints | /debug/stripe-account e /debug/stripe-config RIMOSSI |
| Deploy | fly deploy completato |

### Stripe Pricing
| Tier | Vecchio | Nuovo | Price ID |
|------|---------|-------|----------|
| PRO | $20/mo | $29/mo | price_1Srh32DcRzSMjFE4Oy60XTvL |
| TEAM | $35/mo | $49/mo | price_1Srh4PDcRzSMjFE4GEF5jdfn |

### Sync Pubblico
- Metodo: git worktree isolato (fix definitivo)
- Script aggiornato: scripts/git/sync-to-public.sh
- Commit su public: e556db2

---

## GUARDIANE COINVOLTE

| Guardiana | Task | Verdetto |
|-----------|------|----------|
| Qualita | Audit pre-sync | GO 9/10 |
| Ops | Security check + fix script | GO |
| Ricerca | Audit outreach | 7.5/10 (canali non sfruttati) |
| Marketing | Conferma pricing | $29/$49 OK |

---

## STATO ATTUALE

```
cervellaswarm.com        → ONLINE (Cloudflare Pages)
cervellaswarm-api.fly.dev → ONLINE (health OK)
npm CLI                  → 2.0.0-beta
npm MCP                  → 2.0.0-beta
Stripe                   → Test Mode, $29/$49
GitHub pubblico          → SINCRONIZZATO
```

---

## PROSSIMI STEP

1. **Outreach non sfruttati** (da Guardiana Ricerca):
   - MCP Discord ufficiale (11K membri!) - NON JOINED
   - awesome-mcp-servers PR - NON FATTA
   - DEV.to article - NON SCRITTO

2. **Show HN** - Decidere data definitiva

3. **Stripe Live Mode** - Quando pronti per pagamenti reali

---

## FILE CHIAVE

| File | Cosa |
|------|------|
| packages/api/src/index.ts | Rate limiting + no debug |
| scripts/git/sync-to-public.sh | Metodo worktree (v2) |
| docs/AGENTS_REFERENCE.md | 17 agents + Architect |

---

*"Sessione 305! Security, Stripe, Sync - tutto fatto!"*
*Cervella & Rafa*
