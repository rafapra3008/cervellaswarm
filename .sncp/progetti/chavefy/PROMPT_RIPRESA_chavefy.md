# PROMPT RIPRESA - Chavefy

> **Ultima atualizacao:** 2026-02-12 - Sessao 354++ (terceira sessao)
> **STATUS:** FASE 0 - Step 0.3 CONSTRUIDO (landing page pronta), aguardando deploy

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

## O QUE FOI FEITO NESTA SESSAO (S354++)

### Step 0.3 - Landing Page + Waitlist: CONSTRUIDA

**Processo seguido (metodo correto):**
1. Cervella-marketing criou specs completas (`docs/produto/LANDING_PAGE_SPECS.md`, ~1000 linhas)
2. Cervella-frontend implementou (`landing/`, Vite + React + TailwindCSS v4)
3. Cervella-guardiana auditou (nota 8.8/10)
4. Cervella-regina corrigiu TODAS as issues (3 falhas + 8 melhorias)
5. Build final OK: 224KB JS + 28KB CSS (gzip 70KB + 5.6KB)

**O que a landing page tem:**
- 9 secoes: Header, Hero, ParaQuem, PainPoints, Features, SocialProof, WaitlistCTA, FAQ, Footer
- Formulario waitlist: nome, email, WhatsApp, cidade, qtd imoveis, software atual
- LGPD compliance: checkbox obrigatorio desmarcado, consentimento marketing opcional, metadados timestamp/user-agent
- SEO completo: title, meta desc, OG tags, Twitter Card, Schema.org (Organization, Software, FAQ), canonical
- Acessibilidade: skip-to-content, aria-expanded FAQ, labels, focus states
- Design System: Inter font, cores #1E40AF (primary), #10B981 (success), #F59E0B (accent)
- Mobile-first, scroll suave, header sticky, FAQ accordion
- Formulario salva em localStorage (temporario, backend vira depois)

**O que FALTA para deploy (Step 0.3 estar 100% FEITO):**
1. Dominio registrado (Step 0.1, acao Rafa/filho) - BLOCKER
2. og-image.png (1200x630) para share WhatsApp/Facebook
3. Pagina politica de privacidade real (nao placeholder)
4. Hosting (Vercel/Netlify gratuito)

**Relatorio auditoria:** `reports/AUDIT_LANDING_PAGE.md` (nota final estimada 9.5 apos correcoes)

## PROGRESSO FASE 0

| Step | O que | Estado | Nota |
|------|-------|--------|------|
| 0.1 | Registro dominios + redes | AGUARDANDO RAFA | Blocker para deploy landing |
| 0.2 | Testar Stays.net trial | ESTUDADO | Desk research feita, falta testar produto real |
| 0.3 | Landing page + waitlist | CONSTRUIDA | Codigo pronto, falta deploy (depende 0.1) |
| 0.4 | Blog SEO (5 artigos) | A FAZER | Keywords prontas, PROXIMO STEP das Cervelle |
| 0.5 | Comunidades BR | A FAZER | |
| 0.6 | Outreach 20 PMs | A FAZER | Roteiro pronto (SUBMAPPA) |
| 0.7 | GO/NO-GO pre-Brasil | A FAZER | |

## PROXIMA SESSAO - O QUE FAZER

**Cervelle (em ordem de prioridade):**
1. **Step 0.4:** Blog SEO - primeiro artigo "Gestao aluguel temporada 2026: guia completo"
   - Keywords prontas em `docs/pesquisa/mercado/PESQUISA_SEO_KEYWORDS_BR_2026.md`
   - Artigos planejados: 5 (geral > Stays alt > WhatsApp > pricing > limpeza)
   - Setup blog: integrar no landing site ou pagina separada
2. Criar og-image.png + politica privacidade (pre-deploy)
3. Se Rafa registrou dominio: deploy landing page

**Rafa/filho:**
1. **Step 0.1:** Registrar chavefy.com.br (registro.br, ~R$40) + chavefy.com (~$10)
2. Criar @chavefy nas redes (Instagram, X, LinkedIn, Facebook, TikTok)
3. Email profissional: contato@chavefy.com.br
4. **Step 0.2:** Criar trial Stays.net e testar produto real

## DECISOES TOMADAS

| Decisao | Por que |
|---------|---------|
| Nome: Chavefy | "Chave" + "-fy", brasileiro, soa tech, dominio livre |
| Brasil-first | 3.5x mercado, 10x menos saturado |
| FastAPI + React | Stack que Rafa domina |
| WhatsApp nativo | Diferencial killer (nenhum competitor tem) |
| Landing React+Tailwind | Stack consistente, performance boa, Cervelle dominam |

## PONTO ESTRATEGICO ABERTO

**Custo WhatsApp BSP ($50/cliente/mes)** pode ser 45% da receita no plano Starter R$99.
**Decisao:** Apos validacao com clientes reais (Fase 1).

## PESQUISAS (13 completas)

9 base (S354) + 4 tecnicas (S354+). Ver `stato.md` para lista completa.

## FILES

| O que | Onde |
|-------|------|
| Projeto | ~/Developer/Chavefy/ |
| Landing page (codigo) | ~/Developer/Chavefy/landing/ |
| Specs landing | ~/Developer/Chavefy/docs/produto/LANDING_PAGE_SPECS.md |
| Audit landing | ~/Developer/Chavefy/reports/AUDIT_LANDING_PAGE.md |
| SNCP | CervellaSwarm/.sncp/progetti/chavefy/ |
| MAPPA | CervellaSwarm/.sncp/progetti/chavefy/MAPPA_CHAVEFY.md |
| SUBMAPPA Validacao | CervellaSwarm/.sncp/progetti/chavefy/SUBMAPPA_VALIDACAO.md |
| SUBMAPPA MVP | CervellaSwarm/.sncp/progetti/chavefy/SUBMAPPA_MVP.md |
| Estado detalhado | CervellaSwarm/.sncp/progetti/chavefy/stato.md |

---

*"A chave do sucesso e a validacao antes da construcao."*
*Sessao 354++ - Landing page CONSTRUIDA - La Famiglia*
