# PROMPT RIPRESA - Chavefy

> **Ultima atualizacao:** 2026-02-12 - Sessao 354+
> **STATUS:** FASE 0 - Pesquisas completas (13 total), documentacao 9.5/10, pronto pra execucao

---

## O QUE E CHAVEFY

**SaaS de gestao para property managers brasileiros** (aluguel por temporada).
- Target: hosts profissionais com 3-15 imoveis no Brasil
- Diferencial: WhatsApp nativo + AI auto-reply + compliance BR
- Pricing: R$ 97-397/mes (a ser validado com clientes reais)
- Stack: FastAPI + React + PostgreSQL (multi-tenant RLS)
- Titular: Filho do Rafa (MEI no Brasil)
- Rafa: developer + produto (da Italia ou Brasil)
- Cervelle: constroem TUDO

## POR QUE BRASIL

| Metrica | Italia | Brasil |
|---------|--------|--------|
| Saturacao SaaS | ALTA (15+ player) | BAIXA (5% PME usa SaaS) |
| Crescimento | Estagnado | +9.4%/ano |
| LTV/CAC | 6:1 | 15:1 |
| Break-even | 24-36 meses | 12-18 meses |

Competitor principal: Stays.net (55% mercado, suporte 23 dias resposta, zero AI, zero WhatsApp nativo).

## PESQUISAS COMPLETAS (13 total)

### Base (S354) - 9 pesquisas, 7000+ linhas, 400+ fontes

| # | Pesquisa | Arquivo |
|---|----------|---------|
| 1 | InvestHero analise | .sncp/progetti/cervellaswarm/RICERCA_INVESTHERO_20260212.md |
| 2 | Business imobiliario sem propriedade | .sncp/ricerche/ANALISI_BUSINESS_IMMOBILIARE_SENZA_PROPRIETA_2025.md |
| 3 | Property Management Rafa+AI | .sncp/progetti/cervellaswarm/ricerche/ANALISI_PROPERTY_MANAGEMENT_RAFA_AI_2026.md |
| 4 | Competitor PMS Italia | .sncp/analisi/ANALISI_COMPETITOR_PMS_ITALIA_2026.md |
| 5 | Tech Research SaaS PMS | docs/studio/RICERCA_PROPERTY_MANAGEMENT_SAAS_ITALIA_2026.md |
| 6 | Go-to-Market Strategy | (in-context S354, dados-chave na MAPPA) |
| 7 | Mercado Brasil PMS | .sncp/progetti/miracollo/ANALISE_MERCADO_BRASIL_PMS_2026.md |
| 8 | Domain/Brand Check | (in-context S354, dados-chave neste doc) |
| 9 | Mercado Brasil detalhado | (in-context S354, dados-chave neste doc) |

### Tecnicas (S354+) - 4 pesquisas, ~3.800 linhas, 115+ fontes

| Pesquisa | Arquivo | Destaque |
|----------|---------|----------|
| LGPD para SaaS BR | docs/pesquisa/tecnico/PESQUISA_LGPD_SAAS_2026.md | DPO dispensado MEI, templates prontos |
| WhatsApp Business API | docs/pesquisa/tecnico/PESQUISA_WHATSAPP_API_2026.md | Viavel, BSP $50/cliente, service msgs gratis |
| SEO Keywords BR | docs/pesquisa/mercado/PESQUISA_SEO_KEYWORDS_BR_2026.md | 50+ keywords, WhatsApp = zero competicao |
| Stays.net Deep Analysis | docs/pesquisa/competitor/STAYS_NET_DEEP_ANALYSIS.md | 23d suporte, zero AI, zero WhatsApp nativo |

## DECISOES TOMADAS

| Decisao | Por que |
|---------|---------|
| Nome: Chavefy | "Chave" + "-fy", brasileiro, soa tech, dominio livre |
| Brasil-first | 3.5x mercado, 10x menos saturado |
| Lean approach | Validar antes de construir |
| FastAPI + React | Stack que Rafa domina |
| WhatsApp nativo | Diferencial killer (nenhum competitor tem) |
| Compliance basica MVP | Cadastro hospede basico. Automatizacao em v2.0+ |

## PONTO ESTRATEGICO ABERTO

**Custo WhatsApp BSP ($50/cliente/mes)** pode ser 45% da receita no plano Starter R$99. Opcoes a validar:
1. Cloud API direta (sem BSP) - custo menor
2. Ajustar pricing minimo R$149+
3. WhatsApp so nos planos Pro/Business
**Decisao:** Apos validacao com clientes reais (Fase 1).

## PROXIMA SESSAO

**Fase 0 - Execucao (pesquisas PRONTAS, agora e FAZER):**
1. **Step 0.1:** Registrar dominios + redes sociais (acao Rafa/filho)
2. **Step 0.2:** Testar Stays.net trial (pesquisa desk FEITA, falta testar produto real)
3. **Step 0.3:** Landing page + waitlist (LGPD compliance pronta, SEO keywords prontas)
4. **Step 0.4:** Blog SEO (5 artigos, ordem: geral > pricing > WhatsApp > limpeza > Stays alt)
5. **Step 0.5-0.6:** Comunidades + outreach 20 PMs

## FILES

| O que | Onde |
|-------|------|
| Projeto | ~/Developer/Chavefy/ |
| SNCP | CervellaSwarm/.sncp/progetti/chavefy/ |
| MAPPA | CervellaSwarm/.sncp/progetti/chavefy/MAPPA_CHAVEFY.md |
| SUBMAPPA Validacao | CervellaSwarm/.sncp/progetti/chavefy/SUBMAPPA_VALIDACAO.md |
| SUBMAPPA MVP | CervellaSwarm/.sncp/progetti/chavefy/SUBMAPPA_MVP.md |
| Estado detalhado | CervellaSwarm/.sncp/progetti/chavefy/stato.md |

---

*"A chave do sucesso e a validacao antes da construcao."*
*Sessao 354+ - Audit 9.5/10 - 13 pesquisas - La Famiglia*
