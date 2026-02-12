# SUBMAPPA MVP - Chavefy

> **FASE 2: MVP Build (6-8 meses)**
> **Criacao:** 12 Fevereiro 2026 - S354
> **ATENCAO:** Esta fase SO INICIA apos GO na Fase 1!

---

## OBJETIVO

Construir o MINIMO que resolve o MAXIMO de dor dos property managers brasileiros.

---

## STACK DEFINIDO

| Camada | Tecnologia | Por que |
|--------|------------|---------|
| Backend | FastAPI (Python) | Rafa sabe Python, Cervelle constroem |
| Frontend | React + TailwindCSS | Produtividade, ecosystem |
| Database | PostgreSQL + RLS | Multi-tenant nativo, robusto |
| Cache | Redis | Sessions, rate limiting |
| Hosting | Fly.io | Edge deploy, bom custo |
| Pagamentos | Stripe + Pix (via API) | BR precisa Pix |
| Messaging | WhatsApp Business API | Diferencial killer |
| AI | Claude API | Auto-reply multilingua |
| Email | Resend | Transacional, barato |

---

## MVP FEATURES (priorizadas)

### MUST-HAVE (MVP v1.0)
1. **Calendario unificado** - Sincroniza Airbnb + Booking via iCal
2. **Dashboard** - Visao geral imoveis, reservas, revenue
3. **WhatsApp messaging** - Enviar/receber mensagens hospedes
4. **AI auto-reply** - Respostas automaticas inteligentes (PT/EN/ES)
5. **Gestao check-in/checkout** - Lista diaria, status
6. **Gestao limpeza** - Assign cleaner, status, notificacao
7. **Cobranca** - Planos R$97-397/mes via Stripe + Pix

### NICE-TO-HAVE (v1.1)
8. Pricing dinamico (sugestao baseada em demanda)
9. Report financeiro mensal (revenue, ocupacao, ADR)
10. Multi-usuario (time property manager)

### FUTURO (v2.0+)
11. API Partner Airbnb (beyond iCal)
12. API Partner Booking.com
13. Compliance AUTOMATIZADA (relatorios, normas por municipio)
14. App mobile (React Native)

> **Nota Compliance:** MVP v1.0 inclui compliance BASICA (cadastro hospede, dados obrigatorios). Compliance AUTOMATIZADA (normas locais, relatorios fiscais) e v2.0+.

---

## TIMELINE MVP

```
Mes 1: Setup + Arquitetura + Auth + DB
Mes 2: Calendario + iCal sync
Mes 3: Dashboard + gestao propriedades
Mes 4: WhatsApp integration
Mes 5: AI auto-reply + gestao limpeza
Mes 6: Pagamentos + onboarding flow
Mes 7: Testes (unit + integration + E2E) + CI/CD pipeline
Mes 8: Polish + bug fixes + beta launch (5 clientes)
```

---

## CUSTOS ESTIMADOS (Ano 1)

| Item | Custo/mes | Custo/ano |
|------|-----------|-----------|
| Fly.io (hosting) | $25 | $300 |
| PostgreSQL (managed) | $15 | $180 |
| Redis (managed) | $10 | $120 |
| WhatsApp Business API | $50-57* | $600-684 |
| Claude API | $30 | $360 |
| Stripe fees | 2.9% + R$0.50/tx | variavel |
| Dominio + email | $5 | $60 |
| **TOTAL fixo** | **~$135-167/mes** | **~$1.620-2.004/ano** |

*\* WhatsApp API: BSP 360dialog $50/numero/mes + Meta cobra per-message (service msgs GRATIS dentro 24h, utility $0.0068/msg, marketing $0.0625/msg). Estimativa baseada em ~200 msgs/mes. Ver pesquisa completa: docs/pesquisa/tecnico/PESQUISA_WHATSAPP_API_2026.md*

**Custo marketing (Fase 0-1):** ~$600/6 meses
**TOTAL Ano 1 estimado:** ~$3.000-5.000 (~EUR 2.700-4.500)

---

## ARQUITETURA (High-Level)

```
                    [React Frontend]
                          |
                    [API Gateway]
                          |
              +-----------+-----------+
              |           |           |
         [Auth API]  [Property API]  [Messaging API]
              |           |           |
              +-----+-----+     [WhatsApp API]
                    |                 |
              [PostgreSQL]     [Claude AI]
              (multi-tenant)
```

---

*"O MVP perfeito e aquele que o cliente usa, nao aquele que o developer admira."*
*Chavefy - Submappa MVP - S354*
