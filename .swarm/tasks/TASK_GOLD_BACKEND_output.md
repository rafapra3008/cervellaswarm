# TASK_GOLD_BACKEND - Output

## Risultato: COMPLETATO

### File Creato
`test-orchestrazione/api/calculator.py`

### Funzioni Implementate

| Funzione | Signature | Descrizione |
|----------|-----------|-------------|
| `add` | `add(a: float, b: float) -> float` | Somma due numeri |
| `multiply` | `multiply(a: float, b: float) -> float` | Moltiplica due numeri |
| `power` | `power(base: float, exp: float) -> float` | Calcola potenza |

### Caratteristiche
- Type hints su tutti i parametri e return values
- Docstring completi con Args, Returns, Example
- Testato con casi base e edge cases

### Test Eseguiti
```python
# add
add(2, 3) == 5
add(-1, 1) == 0
add(0.5, 0.5) == 1.0

# multiply
multiply(4, 5) == 20
multiply(-2, 3) == -6
multiply(0, 100) == 0

# power
power(2, 3) == 8
power(5, 0) == 1
power(2, -1) == 0.5
```

**Tutti i test passati!**

---
*Completato da: cervella-backend*
*Data: 2026-01-04*
