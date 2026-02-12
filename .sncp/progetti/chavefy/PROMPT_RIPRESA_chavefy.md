# PROMPT RIPRESA - Chavefy

> **Ultima atualizacao:** 2026-02-12 - Sessao 354+++ (quarta sessao)
> **STATUS:** FASE 0 - Step 0.4 EM CURSO (blog infra + 1/5 artigos), Step 0.3 aguardando deploy

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

## O QUE FOI FEITO (HISTORICO)

### S354: Pesquisas base (9 pesquisas mercado + 4 tecnicas)
### S354+: Estrutura projeto + SNCP
### S354++: Landing page construida (nota 9.5 pos-correcoes)
### S354+++: Blog SEO - infraestrutura + primeiro artigo

**Step 0.4 - Blog SEO: EM CURSO**

Processo seguido:
1. Pesquisa SEO keywords BR 2026 (768 linhas de analise)
2. Infra blog: React Router DOM + lazy loading + code splitting
3. Cervella-marketing escreveu artigo (~3.200 palavras, 13 min)
4. Convertido para JSX completo com Schema.org
5. Auditoria guardiana: 8.7/10 -> correcoes -> re-auditoria: 9.4/10

**O que o blog tem:**
- React Router: / (landing), /blog (index), /blog/:slug (artigos)
- BlogHome: lista artigos com meta tags OG/Twitter/canonical dinamicas
- BlogArticle: lazy loading, Article JSON-LD, FAQPage JSON-LD, meta tags dinamicas, cleanup
- BlogLayout: breadcrumbs com titulo artigo (Chavefy / Blog / Titulo)
- 1o artigo: "Como Gerenciar Aluguel por Temporada Sem Perder a Cabeca em 2026"
  - 6 secoes H2, 7 desafios, tabela financeira, 6 FAQ, 3 links internos, CTA
- Sitemap.xml (3 URLs), robots.txt, _redirects (Netlify SPA)
- Header e Footer atualizados com Link para /blog

**Auditoria geral (guardiana): 8.3/10**
- Issues corrigidas: data inconsistente Hero/WaitlistCTA, docs desatualizados
- Issues pendentes pre-deploy: og-image.png, apple-touch-icon.png, cores Tailwind v4 incompletas, href="#" no Footer

## PROGRESSO FASE 0

| Step | O que | Estado | Nota |
|------|-------|--------|------|
| 0.1 | Registro dominios + redes | AGUARDANDO RAFA | Blocker para deploy |
| 0.2 | Testar Stays.net trial | ESTUDADO | Desk research feita |
| 0.3 | Landing page + waitlist | CONSTRUIDA | Falta deploy (depende 0.1) |
| 0.4 | Blog SEO (5 artigos) | EM CURSO (1/5) | Infra + 1o artigo prontos, 9.4/10 |
| 0.5 | Comunidades BR | A FAZER | |
| 0.6 | Outreach 20 PMs | A FAZER | Roteiro pronto (SUBMAPPA) |
| 0.7 | GO/NO-GO pre-Brasil | A FAZER | |

## PROXIMA SESSAO - O QUE FAZER

**Cervelle (em ordem de prioridade):**
1. Criar og-image.png (1200x630) para share social
2. Pagina politica de privacidade (resolver href="#" + LGPD)
3. Corrigir cores Tailwind v4 (adicionar primary-100/200/300/400, limpar conflito @theme vs config)
4. Se Rafa registrou dominio: deploy landing + blog
5. Step 0.4 continuacao: proximo artigo "Stays.net alternativa"

**Rafa/filho:**
1. **Step 0.1:** Registrar chavefy.com.br + chavefy.com
2. Criar @chavefy nas redes sociais
3. Email profissional: contato@chavefy.com.br
4. **Step 0.2:** Criar trial Stays.net e testar produto real

## DECISOES TOMADAS

| Decisao | Por que |
|---------|---------|
| Nome: Chavefy | "Chave" + "-fy", brasileiro, soa tech, dominio livre |
| Brasil-first | 3.5x mercado, 10x menos saturado |
| FastAPI + React | Stack que Rafa domina |
| WhatsApp nativo | Diferencial killer (nenhum competitor tem) |
| Landing React+Tailwind | Stack consistente, performance boa |
| Blog SPA (React Router) | Integrado na landing, lazy loading, SEO via meta tags dinamicas |
| Data lancamento: Marco 2026 | Padronizada em todas as secoes |

## PONTO ESTRATEGICO ABERTO

**Custo WhatsApp BSP ($50/cliente/mes)** pode ser 45% da receita no plano Starter R$99.
**Decisao:** Apos validacao com clientes reais (Fase 1).

## PESQUISAS (13 completas)

9 base (S354) + 4 tecnicas (S354+). Ver `docs/pesquisa/` para arquivos completos.

## FILES

| O que | Onde |
|-------|------|
| Projeto | ~/Developer/Chavefy/ |
| Landing + blog (codigo) | ~/Developer/Chavefy/landing/ |
| Specs landing | ~/Developer/Chavefy/docs/produto/LANDING_PAGE_SPECS.md |
| Keywords SEO | ~/Developer/Chavefy/docs/pesquisa/mercado/PESQUISA_SEO_KEYWORDS_BR_2026.md |
| Audit landing | ~/Developer/Chavefy/reports/AUDIT_LANDING_PAGE.md |
| Audit blog SEO | ~/Developer/Chavefy/reports/AUDIT_BLOG_SEO.md |
| SNCP | CervellaSwarm/.sncp/progetti/chavefy/ |
| MAPPA | CervellaSwarm/.sncp/progetti/chavefy/MAPPA_CHAVEFY.md |
| SUBMAPPA Validacao | CervellaSwarm/.sncp/progetti/chavefy/SUBMAPPA_VALIDACAO.md |
| SUBMAPPA MVP | CervellaSwarm/.sncp/progetti/chavefy/SUBMAPPA_MVP.md |

---

*"A chave do sucesso e a validacao antes da construcao."*
*Sessao 354+++ - Blog SEO EM CURSO (1/5) - La Famiglia*
