# DECISIONE: Tailwind v4 - MAI PIU' ERRORI!

> **Data:** 15 Gennaio 2026
> **Problema:** Design perso 2 VOLTE per stesso errore
> **Impatto:** Spreco di energia, doppio lavoro

---

## IL PROBLEMA

```
Tailwind v4 usa sintassi DIVERSA da v3!

SBAGLIATO (v3):
@tailwind base;
@tailwind components;
@tailwind utilities;

CORRETTO (v4):
@import "tailwindcss";
```

---

## REGOLA PERMANENTE

```
+================================================================+
|                                                                |
|   MIRACALLOOK USA TAILWIND v4                                  |
|                                                                |
|   index.css DEVE avere:                                        |
|   @import "tailwindcss";                                       |
|                                                                |
|   MAI usare @tailwind base/components/utilities!               |
|                                                                |
+================================================================+
```

---

## COME VERIFICARE

```bash
# 1. Controlla versione Tailwind
grep tailwindcss package.json
# Se >= 4.x.x -> usa @import "tailwindcss"

# 2. Controlla index.css
grep "@tailwind\|@import.*tailwind" src/index.css
# Deve mostrare: @import "tailwindcss"
```

---

## CHECKLIST PRE-COMMIT (Miracallook Frontend)

- [ ] index.css ha `@import "tailwindcss"` (NON @tailwind)
- [ ] Design visibile nel browser
- [ ] Nessun warning Tailwind nella console

---

*"Errore ripetuto = sistema rotto. Documentiamo per non ripetere MAI!"*
