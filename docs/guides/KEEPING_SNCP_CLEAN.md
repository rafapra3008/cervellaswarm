# Keeping Your .sncp/ Clean

> *"Casa pulita = mente pulita = lavoro pulito!"*

---

## Why It Matters

A clean `.sncp/` folder means:

- **Smaller context** = faster AI responses
- **Clean history** = easier debugging
- **Less token usage** = lower costs
- **Better focus** = AI works on what matters NOW

---

## The Rules

| File | Max Lines | When Too Big |
|------|-----------|--------------|
| `PROMPT_RIPRESA_*.md` | 250 | Archive old sessions |
| `stato.md` | 500 | Compact with housekeeping |
| `reports/` | 30 days | Archive old files |

---

## How To Keep It Clean

### 1. Run Housekeeping Weekly

```bash
cervellaswarm housekeeping
```

This shows you what needs attention.

### 2. Archive When Starting Fresh

When you start a new sprint or phase:

1. Move old session notes to `.sncp/archivio/`
2. Keep only the CURRENT session in PROMPT_RIPRESA
3. Compact stato.md to essentials

### 3. Use the `--compact` Flag

```bash
cervellaswarm housekeeping --compact
```

This automatically compacts oversized files.

---

## What Gets Archived

When you run housekeeping with `--archive`:

```
.sncp/archivio/
  2026-01/
    PROMPT_RIPRESA_backup_20260115.md
    reports_20260101_20260115/
      *.json
```

Files are organized by month for easy reference.

---

## Best Practices

1. **Check limits daily** - Look at the comments in your files
2. **Archive before it's urgent** - Don't wait until 149 lines
3. **One session per PROMPT_RIPRESA** - Current session only
4. **Compact weekly** - Make it a habit

---

## The Comments Are Your Friends

Every generated file includes limit comments:

```markdown
<!-- LIMITI: Questo file deve restare < 250 righe -->
<!-- Se cresce troppo, archivia sessioni vecchie in .sncp/archivio/ -->
```

When you see these, respect them!

---

## Why These Specific Limits?

| Limit | Reason |
|-------|--------|
| 250 lines for PROMPT_RIPRESA | AI reads this EVERY session - keep it focused |
| 500 lines for stato.md | History is good, but too much slows everything |
| 30 days for reports | Old reports rarely needed, archive them |

---

## The Philosophy

> *"MINIMO in memoria, MASSIMO su disco"*

Your AI team works better with focused context.
Archive generously. The history is preserved, just not loaded every time.

---

*"Un progresso al giorno = 365 progressi all'anno"*

*CervellaSwarm - docs/guides/KEEPING_SNCP_CLEAN.md*
