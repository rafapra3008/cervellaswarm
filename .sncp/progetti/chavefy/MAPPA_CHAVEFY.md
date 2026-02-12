# MAPPA CHAVEFY - STEP BY STEP

> **"Validar antes de construir. Ouvir antes de codificar."** - La Famiglia
> **Data criacao:** 12 Fevereiro 2026 - S354
> **Ultima modificacao:** 12 Fevereiro 2026 - S354

---

## COMO LER ESTA MAPPA

```
ESTADOS POSSIVEIS:
[FEITO]        = Completado, validado, REAL
[EM CURSO]     = Atualmente em andamento
[ESTUDADO]     = Pesquisa feita, abordagem clara
[A ESTUDAR]    = Precisa pesquisa antes de implementar
[A FAZER]      = Claro o que fazer, precisa tempo
[BLOQUEADO]    = Depende de algo externo

CADA STEP TEM:
- Estado
- Pesquisa feita (link ou "NENHUMA")
- Depende de (steps anteriores)
- Output (o que produz)
- Criterio conclusao (como sabemos que ta FEITO)
```

---

## VISAO GERAL

```
FASE 0: Validacao Online     [EM CURSO]  ██████████.......... 40%
  (55 dias pre-Brasil)

FASE 1: Validacao no Brasil  [A FAZER]   .................... 0%
  (conversas reais)

FASE 2: MVP Build            [A FAZER]   .................... 0%
  (6-8 meses)

FASE 3: Beta + Iteracao      [A FAZER]   .................... 0%
  (3 meses)

FASE 4: Lancamento + Growth  [A FAZER]   .................... 0%
  (6 meses)

FASE 5: Escala               [A FAZER]   .................... 0%
  (ongoing)
```

---

# FASE 0: VALIDACAO ONLINE (55 dias pre-Brasil)

> **"Nao gaste 1 real antes de ter certeza que alguem quer pagar."**
> **SUBMAPPA detalhada:** `SUBMAPPA_VALIDACAO.md`

---

## STEP 0.1: Registro Dominios e Marca

**Estado:** [A FAZER]
**Pesquisa feita:** Verificacao marca S354 (dominios livres, INPI limpo, redes livres)
**Depende de:** Nada
**Output:** Dominios registrados + redes sociais protegidas

**ACOES:**
- [ ] Registrar chavefy.com.br (Registro.br)
- [ ] Registrar chavefy.com (Namecheap/GoDaddy)
- [ ] Criar @chavefy no Instagram, Twitter/X, LinkedIn, Facebook, TikTok
- [ ] Protocolar pedido registro INPI (classe NCL 42)

**Criterio conclusao:** Dominios acessiveis + perfis criados + protocolo INPI

---

## STEP 0.2: Pesquisa Profunda Stays.net + Competitors BR

**Estado:** [ESTUDADO]
**Pesquisa feita:** ANALISE_MERCADO_BRASIL_PMS_2026.md (pesquisa geral), ANALISI_COMPETITOR_PMS_ITALIA_2026.md
**Depende de:** Nada
**Output:** Mapa completo gaps Stays.net + oportunidades

**ACOES:**
- [ ] Criar conta gratuita Stays.net (testar produto)
- [ ] Mapear TODOS os features
- [ ] Ler reviews negativas (Trustpilot, Google, Reclame Aqui)
- [ ] Identificar top 5 pain points nao resolvidos
- [ ] Documentar pricing real (todos os planos)
- [ ] Testar Hospedin, Hits, FastHotel tambem

**Criterio conclusao:** Documento com gap analysis + screenshot features

---

## STEP 0.3: Landing Page + Waitlist

**Estado:** [CONSTRUIDA] - Codigo pronto, aguardando deploy (depende 0.1)
**Pesquisa feita:** Go-to-market strategy S354, LGPD, SEO Keywords
**Depende de:** 0.1 (dominio) para deploy
**Output:** chavefy.com.br LIVE com formulario waitlist

**ACOES:**
- [x] Escolher stack landing: Vite + React + TailwindCSS v4
- [x] Copy completo por cervella-marketing (specs 1000+ linhas)
- [x] Formulario waitlist (nome, email, WhatsApp, cidade, qtd imoveis, software atual)
- [x] 9 secoes implementadas (Header, Hero, ParaQuem, PainPoints, Features, SocialProof, WaitlistCTA, FAQ, Footer)
- [x] LGPD compliance (checkboxes, consentimento, metadados)
- [x] SEO completo (meta tags, OG, Twitter Card, Schema.org, canonical)
- [x] Acessibilidade (skip-to-content, aria-expanded, labels, focus)
- [x] Auditoria guardiana (8.8/10 -> ~9.5 apos 11 correcoes)
- [ ] Criar og-image.png (1200x630) para share social
- [ ] Pagina politica de privacidade real
- [ ] Analytics (Plausible ou GA4)
- [ ] Deploy (apos dominio registrado)

**Criterio conclusao:** Pagina LIVE + formulario funcionando + analytics

---

## STEP 0.4: Blog SEO (Pain Points)

**Estado:** [A FAZER]
**Pesquisa feita:** Go-to-market strategy S354
**Depende de:** 0.3 (landing page)
**Output:** 5 artigos SEO publicados

**ARTIGOS PLANEJADOS:**
1. "Como gerenciar aluguel por temporada sem perder a cabeca em 2026"
2. "Stays.net alternativa: o que os hosts brasileiros realmente precisam"
3. "WhatsApp para aluguel por temporada: guia completo"
4. "Pricing dinamico Airbnb: como cobrar o preco certo automaticamente"
5. "Gestao de limpeza e check-in: automatize sua operacao"

**Criterio conclusao:** 5 artigos publicados + indexados no Google

---

## STEP 0.5: Comunidade (Grupos WhatsApp/Facebook)

**Estado:** [A FAZER]
**Pesquisa feita:** Nenhuma (precisa mapear grupos)
**Depende de:** Nada
**Output:** Presenca em 10+ grupos + reputacao construida

**ACOES:**
- [ ] Pesquisar e listar grupos Facebook de property managers BR
- [ ] Pesquisar grupos WhatsApp de hosts Airbnb BR
- [ ] Entrar em 10+ grupos
- [ ] Participar ativamente (responder duvidas, agregar valor)
- [ ] ZERO spam - so valor
- [ ] Documentar pain points mencionados

**Criterio conclusao:** Ativo em 10+ grupos + 20 interacoes de valor

---

## STEP 0.6: Outreach Online (20 Property Managers)

**Estado:** [A FAZER]
**Pesquisa feita:** Go-to-market strategy S354
**Depende de:** 0.5 (comunidade)
**Output:** 20 conversas com PMs reais + dados pain points

**ACOES:**
- [ ] Montar roteiro entrevista (10 perguntas-chave)
- [ ] Identificar 30 PMs no LinkedIn/Instagram/grupos
- [ ] Outreach personalizado (sem pitch, so curiosidade)
- [ ] Agendar 20 calls/chats (15-30 min cada)
- [ ] Documentar CADA conversa (pain, tools, preco, desejos)
- [ ] Compilar analise: top 5 problemas + willingness to pay

**PERGUNTAS-CHAVE:**
1. Quantos imoveis voce gerencia?
2. Quais ferramentas usa hoje? Quanto paga?
3. O que mais te incomoda no dia a dia?
4. Quanto tempo gasta respondendo hospedes?
5. Ja usou algum software especifico? O que achou?
6. Se existisse uma ferramenta que [X], voce pagaria R$97/mes?

**Criterio conclusao:** 20 entrevistas documentadas + analise compilada

---

## STEP 0.7: GO/NO-GO Pre-Brasil

**Estado:** [A FAZER]
**Pesquisa feita:** Todas as anteriores
**Depende de:** 0.1-0.6
**Output:** Decisao: continuar, pivotar, ou parar

**CRITERIOS GO:**
- [ ] 10+ PMs entrevistados online
- [ ] 5+ dispostos a pagar (verbal)
- [ ] Landing page com 50+ inscritos waitlist
- [ ] Pain points claros e consistentes
- [ ] Modelo de negocios validado (pricing aceito)

**CRITERIOS NO-GO:**
- Ninguem quer pagar
- Pain points frageis (nice-to-have, nao need-to-have)
- Mercado menor do que pesquisas indicaram
- Competitor ja resolve tudo

**Criterio conclusao:** Documento GO/NO-GO com dados + decisao Rafa

---

# FASE 1: VALIDACAO NO BRASIL (apos chegada)

> **"Nada substitui conversa cara a cara."**

---

## STEP 1.1: Entrevistas Presenciais

**Estado:** [A FAZER]
**Depende de:** Fase 0 completa + chegada ao Brasil
**Output:** 10+ entrevistas presenciais documentadas

---

## STEP 1.2: Validacao Demanda (Commits)

**Estado:** [A FAZER]
**Depende de:** 1.1
**Output:** 5-10 PMs comprometidos a pagar R$97/mes

---

## STEP 1.3: Definir MVP Features (Baseado em Feedback)

**Estado:** [A FAZER]
**Depende de:** 1.1, 1.2
**Output:** Lista features MVP priorizadas por feedback real

---

## STEP 1.4: Configurar MEI/Empresa

**Estado:** [A FAZER]
**Depende de:** 1.2 (so se GO)
**Output:** MEI do filho ativo OU LTDA constituida

---

## STEP 1.5: GO/NO-GO Final

**Estado:** [A FAZER]
**Depende de:** 1.1-1.4
**Output:** Decisao FINAL: construir MVP ou pivotar/parar

---

# FASE 2: MVP BUILD (6-8 meses)

> **"Construir o MINIMO que resolve o MAXIMO de dor."**
> **SUBMAPPA detalhada:** `SUBMAPPA_MVP.md`

---

## STEP 2.1: Arquitetura e Design System

**Estado:** [A FAZER]
**Depende de:** Fase 1 completa (GO)
**Output:** Arquitetura documentada + wireframes

---

## STEP 2.2: Backend Core (FastAPI + PostgreSQL)

**Estado:** [A FAZER]
**Depende de:** 2.1
**Output:** API base + auth + multi-tenant DB

---

## STEP 2.3: Channel Manager Basico (iCal)

**Estado:** [A FAZER]
**Depende de:** 2.2
**Output:** Sincronizacao calendario Airbnb/Booking via iCal

---

## STEP 2.4: Dashboard Frontend (React)

**Estado:** [A FAZER]
**Depende de:** 2.2
**Output:** Dashboard funcional com calendario unificado

---

## STEP 2.5: WhatsApp Integration

**Estado:** [A FAZER]
**Depende de:** 2.2
**Output:** Envio/recebimento mensagens WhatsApp Business API

---

## STEP 2.6: AI Auto-Reply

**Estado:** [A FAZER]
**Depende de:** 2.5
**Output:** Respostas automaticas inteligentes (multilingua)

---

## STEP 2.7: Compliance BR Basica

**Estado:** [A ESTUDAR]
**Pesquisa feita:** NENHUMA (precisa pesquisa regulamentacao por municipio)
**Depende de:** 2.2
**Output:** Cadastro hospede, dados obrigatorios, formularios basicos
**Nota:** Compliance BASICA (cadastro, dados) no MVP. Compliance AUTOMATIZADA (normas locais, relatorios) em v2.0+.

---

## STEP 2.8: Pagamentos (Stripe + Pix)

**Estado:** [A FAZER]
**Depende de:** 2.2
**Output:** Cobranca recorrente funcionando

---

# FASE 3: BETA + ITERACAO (3 meses)

> **[SKELETAL]** Sera detalhada apos GO na Fase 1. Steps abaixo sao indicativos.

---

## STEP 3.1: Beta 5 Clientes
**Estado:** [A FAZER] | **Depende de:** Fase 2 completa | **Output:** 5 clientes usando o produto

## STEP 3.2: Feedback Loop Semanal
**Estado:** [A FAZER] | **Depende de:** 3.1 | **Output:** Processo feedback estruturado

## STEP 3.3: Iteracao MVP (bugs + features)
**Estado:** [A FAZER] | **Depende de:** 3.2 | **Output:** MVP melhorado com base em feedback real

## STEP 3.4: Beta 10 Clientes
**Estado:** [A FAZER] | **Depende de:** 3.3 | **Output:** Expansao beta, validacao escalabilidade

## STEP 3.5: Product-Market Fit Assessment
**Estado:** [A FAZER] | **Depende de:** 3.4 | **Output:** Documento PMF com metricas (NPS, churn, retention)

---

# FASE 4: LANCAMENTO + GROWTH (6 meses)

> **[SKELETAL]** Sera detalhada apos Fase 3. Steps abaixo sao indicativos.

---

## STEP 4.1: Lancamento Publico
**Estado:** [A FAZER] | **Depende de:** Fase 3 completa | **Output:** Produto aberto ao publico

## STEP 4.2: Marketing Engine (SEO + Google Ads)
**Estado:** [A FAZER] | **Depende de:** 4.1 | **Output:** Pipeline marketing ativo

## STEP 4.3: Parcerias (Contadores + Agencias)
**Estado:** [A FAZER] | **Depende de:** 4.1 | **Output:** 5+ parceiros ativos

## STEP 4.4: Scale 50 Clientes
**Estado:** [A FAZER] | **Depende de:** 4.2, 4.3 | **Output:** 50 clientes pagantes

## STEP 4.5: Scale 100 Clientes
**Estado:** [A FAZER] | **Depende de:** 4.4 | **Output:** 100 clientes pagantes (~R$ 20k/mes)

---

# FASE 5: ESCALA (ongoing)

> **[SKELETAL]** Sera detalhada apos Fase 4. Steps abaixo sao indicativos.

---

## STEP 5.1: Features Avancadas (pricing ML, analytics)
**Estado:** [A FAZER] | **Depende de:** Fase 4 completa | **Output:** Features v2.0

## STEP 5.2: API Partner Airbnb/Booking
**Estado:** [A FAZER] | **Depende de:** 5.1 | **Output:** Integracao direta (alem de iCal)

## STEP 5.3: Mercado Italia? (avaliacao)
**Estado:** [A FAZER] | **Depende de:** 5.1 | **Output:** Estudo viabilidade expansao Europa

## STEP 5.4: Target 300+ Clientes (60k+ EUR/ano)
**Estado:** [A FAZER] | **Depende de:** 5.2 | **Output:** Meta financeira de liberdade geografica

---

## TIMELINE ESTIMADA

```
2026 Fev-Mar: FASE 0 (Validacao online, 55 dias)
2026 Abr-Mai: FASE 1 (Validacao no Brasil)
2026 Jun-Jan: FASE 2 (MVP Build, 6-8 meses)
2027 Fev-Abr: FASE 3 (Beta + Iteracao)
2027 Mai-Out: FASE 4 (Lancamento + Growth)
2027 Nov+:    FASE 5 (Escala)
```

---

*"A chave do sucesso e a validacao antes da construcao."*
*Chavefy - La Famiglia - S354*
