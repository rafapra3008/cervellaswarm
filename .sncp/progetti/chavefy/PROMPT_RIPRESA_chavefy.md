# PROMPT RIPRESA - Chavefy

> **Ultima atualizacao:** 2026-02-13 - Sessao S355 (checkpoint)
> **STATUS:** FASE 0 - Step 0.4 EM CURSO (2/5 artigos prontos)

---

## O QUE E CHAVEFY

SaaS de gestao para property managers brasileiros (aluguel por temporada).
- Target: hosts profissionais com 3-15 imoveis no Brasil
- Diferencial: WhatsApp nativo + AI auto-reply + compliance BR
- Pricing: R$ 97-397/mes (a ser validado com clientes reais)
- Stack landing: Vite 7.3 + React 19 + TailwindCSS v4 + React Router DOM
- Stack produto: FastAPI + React + PostgreSQL (multi-tenant RLS)
- Titular: Filho do Rafa (MEI no Brasil)

## HISTORICO DE SESSOES

| Sessao | O que foi feito |
|--------|----------------|
| S354 | 9 pesquisas base mercado + go-to-market + keywords SEO |
| S354+ | 4 pesquisas tecnicas + estrutura projeto + SNCP + audit 9.5/10 |
| S354++ | Landing page completa (9 secoes, waitlist, LGPD, SEO, audit 9.5) |
| S354+++ | Blog SEO: infra completa + 1o artigo + auditorias + correcoes docs |
| S355 | 4 etapas: cores Tailwind, LGPD pages, OG images, 2o artigo SEO |

## ESTADO ATUAL DO CODIGO

### Landing Page (Step 0.3: PRONTA para deploy)
- `landing/` = Vite 7.3 + React 19 + TailwindCSS v4
- 9 secoes: Header, Hero, ParaQuem, PainPoints, Features, SocialProof, WaitlistCTA, FAQ, Footer
- Formulario waitlist (6 campos + LGPD) salva em localStorage (temporario)
- SEO: title, meta desc, OG, Twitter Card, Schema.org (Organization + Software + FAQ)
- **ZERO href="#"** em todo o codebase (todos resolvidos na S355)
- Build OK: ~294KB JS + 32KB CSS (gzip ~91KB + 6KB)

### Blog (Step 0.4: EM CURSO, 2/5 artigos)
- React Router DOM: `/`, `/blog`, `/blog/:slug`, `/politica-privacidade`, `/termos-uso`
- Lazy loading com React.lazy + Suspense (code splitting por artigo)
- Meta tags OG/Twitter/canonical DINAMICAS via useEffect + cleanup
- Schema.org: Article JSON-LD + FAQPage JSON-LD (injetados dinamicamente)
- Breadcrumbs: Chavefy / Blog / [titulo do artigo]
- **Artigo 1:** "Como Gerenciar Aluguel por Temporada" (~3.200 palavras, 13 min)
- **Artigo 2:** "Melhores Alternativas ao Stays.net em 2026" (~3.800 palavras, 15 min)

### Paginas Legais (NOVAS na S355)
- `/politica-privacidade` = PoliticaPrivacidade.jsx (12 secoes, LGPD Art. 18 completo)
- `/termos-uso` = TermosUso.jsx (11 secoes, foro CDC Art. 101)
- Cross-links entre as duas paginas

### Imagens (NOVAS na S355)
- `landing/public/og-image.png` (1200x630, 62KB) - share social
- `landing/public/apple-touch-icon.png` (180x180, 2.8KB) - iOS
- `landing/public/favicon-32x32.png` + `favicon-16x16.png` - PNG fallbacks
- Geradas via `scripts/generate-images.mjs` (Sharp + SVG, sem Puppeteer)

### Como adicionar novo artigo:
1. Criar JSX em `landing/src/data/articles/NomeArtigo.jsx`
2. Adicionar metadata em `landing/src/data/articles.js` (slug, title, metaDescription, faq...)
3. Registrar lazy import em `landing/src/pages/BlogArticle.jsx` (articleComponents)
4. Adicionar URL no `landing/public/sitemap.xml`

## O QUE FOI RESOLVIDO NA S355

| Issue | Como resolvida |
|-------|---------------|
| og-image.png | Gerada (1200x630, Sharp+SVG) |
| apple-touch-icon.png | Gerada (180x180) + favicon PNGs |
| 5x href="#" no Footer | 2 viraram Link, 3 social viraram span |
| href="#" Privacidade no WaitlistForm | Link para /politica-privacidade |
| Cores Tailwind v4 incompletas | primary-100/200/300/400 adicionadas no @theme |
| Conflito @theme vs tailwind.config.js | tailwind.config.js deletado (dead code em v4) |
| primary-600 = primary-700 | primary-700 corrigida para #172554 |

## ISSUES REMANESCENTES

| Issue | Prioridade | Nota |
|-------|-----------|------|
| Crawlers sociais nao executam JS | INFO | Meta tags dinamicas nao funcionam para preview WhatsApp/Facebook |
| Faltam 3 artigos SEO | MEDIA | Step 0.4 = 2/5 artigos |
| Deploy pendente (sem dominio) | BLOQUEADO | Aguardando Rafa registrar dominios |

## PROGRESSO FASE 0

| Step | O que | Estado | Nota |
|------|-------|--------|------|
| 0.1 | Registro dominios + redes | AGUARDANDO RAFA | **Blocker** para deploy |
| 0.2 | Testar Stays.net trial | ESTUDADO | Desk research feita |
| 0.3 | Landing page + waitlist | **PRONTA** | Todos issues pre-deploy resolvidos |
| 0.4 | Blog SEO (5 artigos) | EM CURSO (2/5) | 2 artigos + LGPD pages prontos |
| 0.5 | Comunidades BR | A FAZER | |
| 0.6 | Outreach 20 PMs | A FAZER | Roteiro pronto (SUBMAPPA) |
| 0.7 | GO/NO-GO pre-Brasil | A FAZER | |

## PROXIMA SESSAO

**Cervelle (prioridade):**
1. 3o artigo SEO: "Precificacao Dinamica Airbnb" (PESQUISA PRONTA - 55+ fontes, salva em docs/pesquisa/)
   - Marketing escreve JSX -> guardiana audita -> corrige ate 9.5
2. 4o artigo SEO: "WhatsApp para aluguel por temporada" (pesquisa a fazer)
3. 5o artigo SEO: "Gestao de limpeza e check-in" (pesquisa a fazer)
4. Se dominio pronto: deploy Netlify/Vercel

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
| Processo: marketing escreve -> guardiana audita -> corrige | Formula Magica |
| tailwind.config.js deletado | Dead code em Tailwind v4, so @theme funciona |
| Sharp+SVG para imagens | Leve (sem Puppeteer), reusavel via script |
| LGPD: consentimento granular | 2 checkboxes separados no waitlist form |

## FILES IMPORTANTES

| O que | Onde |
|-------|------|
| Projeto | `~/Developer/Chavefy/` |
| Landing + blog | `~/Developer/Chavefy/landing/` |
| 1o artigo | `landing/src/data/articles/ComoGerenciarAluguelTemporada.jsx` |
| 2o artigo | `landing/src/data/articles/AlternativasStaysNet.jsx` |
| Registry artigos | `landing/src/data/articles.js` |
| Politica Privacidade | `landing/src/pages/PoliticaPrivacidade.jsx` |
| Termos de Uso | `landing/src/pages/TermosUso.jsx` |
| Gerador imagens | `landing/scripts/generate-images.mjs` |
| MAPPA | `CervellaSwarm/.sncp/progetti/chavefy/MAPPA_CHAVEFY.md` |

## AUDITORIAS S355
Todas aprovadas: Cores Tailwind (9.5), LGPD pages (9.4), OG images (9.3), Artigo 2 (8.6->9.5+).

---
*"Fatto BENE > Fatto VELOCE" - S355 checkpoint - 13 Fev 2026*
