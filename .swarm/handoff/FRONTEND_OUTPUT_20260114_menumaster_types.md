# OUTPUT: MenuMaster Frontend Types Alignment

**Data**: 20260114 | **Worker**: cervella-frontend
**Task**: Allineamento tipi frontend con backend

## Status: ✅ COMPLETATO

## File Modificati

1. **menuApi.ts** - Sostituito `getPublicMenu` con endpoints separati
   - `getPublicCategories(slug)` → `/v1/public/menu/{slug}/categories`
   - `getPublicDishes(slug)` → `/v1/public/menu/{slug}/dishes`

2. **PublicMenu.tsx** - Refactor completo
   - Rimosso tipo `Menu` con `logoUrl`, `restaurantName`
   - Usa `Category` e `Dish` separati con `name_translations`, `base_price`
   - Fetch parallelo di categorie e piatti
   - Usa `getTranslation()` per tutti i campi traducibili

3. **MenuEditor.tsx** - Migrato a React Query
   - Rimosso `useMenuStore` per dati
   - Usa `useCategories()` e `useDishes()` hooks
   - Calcolo locale dei piatti per categoria (filter su `dish.category_id`)
   - Usa `getTranslation()` per nomi categorie

4. **menuStore.ts** - Semplificato
   - Rimossa gestione categorie/piatti embedded
   - Ora solo UI state minimo (`selectedCategory`)
   - Aggiunto commento DEPRECATED

## Build Verificato

```bash
✓ npm run build - SUCCESS
✓ 150 modules transformed
✓ No TypeScript errors
```

## Verifica Acceptance Criteria

- [x] Allineamento tipi con backend (`name_translations`, `base_price`, etc.)
- [x] `PublicMenu.tsx` usa nuovi endpoints
- [x] `MenuEditor.tsx` usa React Query hooks
- [x] Rimossi riferimenti a vecchi field (`name`, `price`, `soldOut`, etc.)
- [x] Build TypeScript passa senza errori

## Come Testare

1. **PublicMenu**
   ```bash
   # Start backend + frontend
   # Naviga a /menu/[slug]
   # Verifica che categorie e piatti si carichino
   # Verifica traduzioni (IT/EN se disponibili)
   ```

2. **MenuEditor**
   ```bash
   # Login come tenant
   # Naviga a /editor
   # Verifica lista categorie con count piatti
   # Verifica piatti per categoria
   ```

## Note per Guardiana

- Non ho aggiunto features, solo fix tipi
- Logica esistente mantenuta
- menuStore ridotto a minimo (può essere rimosso in futuro)
- Tutti i componenti (DishCard, DishModal, CategoryCard) già allineati

## Prossimi Step Suggeriti

- Test runtime con backend reale
- Eventuale rimozione completa di menuStore
- Verificare gestione errori in PublicMenu (slug non trovato)
