# PROMPT RIPRESA - Chavefy

> **Ultima atualizacao:** 2026-02-12 - Sessao S354+++ (checkpoint final)
> **STATUS:** FASE 0 - Step 0.4 EM CURSO (blog infra + 1o artigo pronto, faltam 4 artigos)

---

## O QUE E CHAVEFY

SaaS de gestao para property managers brasileiros (aluguel por temporada).
- Target: hosts profissionais com 3-15 imoveis no Brasil
- Diferencial: WhatsApp nativo + AI auto-reply + compliance BR
- Pricing: R$ 97-397/mes (a ser validado com clientes reais)
- Stack: FastAPI + React + PostgreSQL (multi-tenant RLS)
- Titular: Filho do Rafa (MEI no Brasil)

## HISTORICO DE SESSOES

| Sessao | O que foi feito |
|--------|----------------|
| S354 | 9 pesquisas base mercado + go-to-market + keywords SEO |
| S354+ | 4 pesquisas tecnicas + estrutura projeto + SNCP + audit 9.5/10 |
| S354++ | Landing page completa (9 secoes, waitlist, LGPD, SEO, audit 9.5) |
| S354+++ | Blog SEO: infra completa + 1o artigo + auditorias + correcoees docs |

## ESTADO ATUAL DO CODIGO

### Landing Page (Step 0.3: CONSTRUIDA, falta deploy)
- `landing/` = Vite 7.3 + React 19 + TailwindCSS v4
- 9 secoes: Header, Hero, ParaQuem, PainPoints, Features, SocialProof, WaitlistCTA, FAQ, Footer
- Formulario waitlist (6 campos + LGPD) salva em localStorage (temporario)
- SEO: title, meta desc, OG, Twitter Card, Schema.org (Organization + Software + FAQ)
- Build OK: ~273KB JS + 31KB CSS (gzip ~86KB + 6KB)

### Blog (Step 0.4: EM CURSO, 1/5 artigos)
- React Router DOM: `/` (landing), `/blog` (index), `/blog/:slug` (artigos)
- Lazy loading com React.lazy + Suspense (code splitting por artigo)
- Meta tags OG/Twitter/canonical DINAMICAS via useEffect + cleanup
- Schema.org: Article JSON-LD + FAQPage JSON-LD (injetados dinamicamente)
- Breadcrumbs: Chavefy / Blog / [titulo do artigo]
- 1o artigo pronto: "Como Gerenciar Aluguel por Temporada" (~3.200 palavras, 13 min)

### Como adicionar novo artigo:
1. Criar JSX em `landing/src/data/articles/NomeArtigo.jsx`
2. Adicionar metadata em `landing/src/data/articles.js` (slug, title, metaDescription, faq...)
3. Registrar lazy import em `landing/src/pages/BlogArticle.jsx` (articleComponents)
4. Adicionar URL no `landing/public/sitemap.xml`

## ISSUES CONHECIDAS (pre-deploy)

| Issue | Prioridade | Onde | O que fazer |
|-------|-----------|------|-------------|
| og-image.png nao existe | ALTA | `landing/public/` | Criar 1200x630, share social quebrado sem isso |
| apple-touch-icon.png | ALTA | `landing/public/` | Criar 180x180, iOS home screen |
| 5x href="#" no Footer | ALTA | `Footer.jsx` L30,35,57,65,73 | Privacidade e Termos precisam de paginas reais |
| href="#" Privacidade no WaitlistForm | ALTA | `WaitlistForm.jsx` L298 | LGPD exige link funcional |
| Cores Tailwind v4 incompletas | MEDIA | `index.css` @theme | Faltam primary-100/200/300/400 |
| Conflito @theme vs tailwind.config.js | MEDIA | Ambos definem cores | Manter so @theme (Tailwind v4 way) |
| primary-600 = primary-700 (#1E3A8A) | BAIXA | `index.css` L7-8 | Diferenciar (ex: 700=#172554) |
| Crawlers sociais nao executam JS | INFO | Blog meta tags | WhatsApp/Facebook mostrarao meta da landing, nao do artigo |

## PROGRESSO FASE 0

| Step | O que | Estado | Nota |
|------|-------|--------|------|
| 0.1 | Registro dominios + redes | AGUARDANDO RAFA | **Blocker** para deploy |
| 0.2 | Testar Stays.net trial | ESTUDADO | Desk research feita, falta testar produto |
| 0.3 | Landing page + waitlist | CONSTRUIDA | Codigo pronto, falta deploy |
| 0.4 | Blog SEO (5 artigos) | EM CURSO (1/5) | Infra + 1o artigo prontos, nota 9.4/10 |
| 0.5 | Comunidades BR | A FAZER | |
| 0.6 | Outreach 20 PMs | A FAZER | Roteiro pronto (SUBMAPPA) |
| 0.7 | GO/NO-GO pre-Brasil | A FAZER | |

## PROXIMA SESSAO

**Cervelle (prioridade):**
1. og-image.png (1200x630) + apple-touch-icon.png (180x180)
2. Pagina politica de privacidade (resolver todos os href="#" + LGPD)
3. Cores Tailwind v4 (primary-100/200/300/400 + limpar conflito config)
4. Se dominio pronto: deploy Netlify/Vercel
5. Proximo artigo SEO: "Stays.net alternativa: o que os hosts brasileiros precisam"

**Rafa/filho:**
1. Registrar chavefy.com.br (registro.br) + chavefy.com
2. Criar @chavefy nas redes (Instagram, X, LinkedIn, Facebook, TikTok)
3. Email: contato@chavefy.com.br
4. Testar Stays.net trial (produto real)

## DECISOES TOMADAS

| Decisao | Por que |
|---------|---------|
| Nome: Chavefy | "Chave" + "-fy", brasileiro, soa tech, dominio livre |
| Brasil-first | 3.5x mercado, 10x menos saturado |
| Blog integrado na landing (React Router) | Mesmo stack, lazy loading, SEO dinamico |
| Data lancamento: Marco 2026 | Padronizada em Hero + WaitlistCTA |
| Processo: marketing escreve -> frontend implementa -> guardiana audita | Formula Magica aplicada |

## PONTO ESTRATEGICO ABERTO

**Custo WhatsApp BSP ($50/cliente/mes)** pode ser 45% da receita Starter R$99.
Decisao adiada para validacao com clientes reais (Fase 1).

## FILES IMPORTANTES

| O que | Onde |
|-------|------|
| Projeto | `~/Developer/Chavefy/` |
| Landing + blog | `~/Developer/Chavefy/landing/` |
| 1o artigo (JSX) | `landing/src/data/articles/ComoGerenciarAluguelTemporada.jsx` |
| 1o artigo (fonte MD) | `landing/src/data/articles/como-gerenciar-aluguel-temporada.md` |
| Registry artigos | `landing/src/data/articles.js` |
| Specs landing | `docs/produto/LANDING_PAGE_SPECS.md` |
| Keywords SEO | `docs/pesquisa/mercado/PESQUISA_SEO_KEYWORDS_BR_2026.md` |
| Audit landing | `reports/AUDIT_LANDING_PAGE.md` |
| Audit blog | `reports/AUDIT_BLOG_SEO.md` |
| MAPPA | `CervellaSwarm/.sncp/progetti/chavefy/MAPPA_CHAVEFY.md` |

## AUDITORIAS

| O que | Nota | Arquivo |
|-------|------|---------|
| Landing page | 9.5/10 (estimada pos-correcoes) | `reports/AUDIT_LANDING_PAGE.md` |
| Blog SEO (1a) | 8.7/10 -> corrigido | `reports/AUDIT_BLOG_SEO.md` |
| Blog SEO (re-audit) | 9.4/10 | (nao salvo em arquivo) |
| Auditoria geral | 8.3/10 (docs desatualizados + cores Tailwind) | (nao salvo) |

---

*"Fatto BENE > Fatto VELOCE" - La Famiglia*
*S354+++ checkpoint - Blog SEO 1/5 artigos - 12 Fev 2026*
