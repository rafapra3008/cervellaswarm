# Agents Reference

> **Complete guide to all 16 CervellaSwarm agents**

---

## Overview

CervellaSwarm has 16 specialized agents organized in a hierarchy:

```
                    QUEEN (1)
                       |
           +----------+----------+
           |                     |
      GUARDIANS (3)         WORKERS (12)
           |                     |
    Quality, Ops,          Frontend, Backend,
     Research              Tester, Data, etc.
```

- **Queen (1):** Orchestrates everything
- **Guardians (3):** Review and validate (Opus model)
- **Workers (12):** Execute specialized tasks (Sonnet model)

---

## The Queen

### cervella-orchestrator

**Role:** Coordinates the entire swarm

**When to use:**
- Complex multi-step tasks
- Tasks requiring multiple specialists
- When you're not sure which agent to use

**Capabilities:**
- Breaks down complex tasks into subtasks
- Assigns work to appropriate specialists
- Coordinates parallel execution
- Ensures quality through Guardian reviews

**Example:**
```bash
spawn-workers --orchestrator
> "Build a user authentication system with OAuth, tests, and documentation"
```

---

## The Guardians (Quality Gates)

### cervella-guardiana-qualita

**Role:** Code quality and standards

**When to use:**
- After implementation, before merge
- Code review requests
- Quality audits

**Capabilities:**
- Reviews code for best practices
- Checks test coverage
- Validates architecture decisions
- Scores implementations (0-10)

**Example:**
```bash
spawn-workers --guardiana-qualita
> "Review the authentication module for quality issues"
```

---

### cervella-guardiana-ops

**Role:** DevOps, infrastructure, deployment

**When to use:**
- Deployment preparations
- Infrastructure changes
- CI/CD configuration

**Capabilities:**
- Validates deployment readiness
- Reviews infrastructure code
- Checks security configurations
- Monitors system health

**Example:**
```bash
spawn-workers --guardiana-ops
> "Validate the deployment configuration for production"
```

---

### cervella-guardiana-ricerca

**Role:** Research validation

**When to use:**
- After research tasks
- Before implementing researched solutions
- Validating technical decisions

**Capabilities:**
- Validates research quality
- Checks sources reliability
- Ensures completeness
- Identifies gaps

**Example:**
```bash
spawn-workers --guardiana-ricerca
> "Validate the caching research before implementation"
```

---

## The Workers (Specialists)

### cervella-frontend

**Role:** Frontend development

**Specialties:**
- React, Vue, Angular
- CSS, Tailwind, styled-components
- UI/UX implementation
- Responsive design
- Accessibility (a11y)

**Example:**
```bash
spawn-workers --frontend
> "Create a responsive dashboard component with dark mode"
```

---

### cervella-backend

**Role:** Backend development

**Specialties:**
- Python, FastAPI, Django
- REST APIs, GraphQL
- Database integration
- Business logic
- External integrations

**Example:**
```bash
spawn-workers --backend
> "Create an API endpoint for user registration with validation"
```

---

### cervella-tester

**Role:** Testing and QA

**Specialties:**
- Unit tests
- Integration tests
- E2E tests
- Test coverage analysis
- Bug hunting

**Example:**
```bash
spawn-workers --tester
> "Write comprehensive tests for the auth module"
```

---

### cervella-data

**Role:** Data and databases

**Specialties:**
- SQL optimization
- Database design
- Data migrations
- Analytics queries
- ETL processes

**Example:**
```bash
spawn-workers --data
> "Optimize the slow queries in the reporting module"
```

---

### cervella-security

**Role:** Security audits

**Specialties:**
- Vulnerability scanning
- Security best practices
- OWASP compliance
- Authentication/authorization
- Data protection

**Example:**
```bash
spawn-workers --security
> "Audit the API for security vulnerabilities"
```

---

### cervella-devops

**Role:** DevOps and infrastructure

**Specialties:**
- Docker, Kubernetes
- CI/CD pipelines
- Cloud deployment (AWS, GCP)
- Monitoring setup
- Automation scripts

**Example:**
```bash
spawn-workers --devops
> "Create a Docker setup for the application"
```

---

### cervella-researcher

**Role:** Technical research

**Specialties:**
- Technology evaluation
- Best practices research
- Competitive analysis
- Architecture patterns
- Documentation review

**Example:**
```bash
spawn-workers --researcher
> "Research best practices for rate limiting in APIs"
```

---

### cervella-docs

**Role:** Documentation

**Specialties:**
- README files
- API documentation
- User guides
- Technical specifications
- Code comments

**Example:**
```bash
spawn-workers --docs
> "Document the authentication API endpoints"
```

---

### cervella-marketing

**Role:** UX strategy and positioning

**Specialties:**
- User flow optimization
- UI placement decisions
- Copywriting
- Landing page strategy
- User research

**Example:**
```bash
spawn-workers --marketing
> "Where should we place the signup CTA for maximum conversion?"
```

---

### cervella-ingegnera

**Role:** Architecture and refactoring

**Specialties:**
- Code architecture
- Technical debt analysis
- Refactoring strategies
- Performance optimization
- Pattern implementation

**Example:**
```bash
spawn-workers --ingegnera
> "Analyze the codebase for technical debt and propose fixes"
```

---

### cervella-scienziata

**Role:** Business and market research

**Specialties:**
- Market analysis
- Competitor research
- Trend identification
- Business strategy
- Opportunity finding

**Example:**
```bash
spawn-workers --scienziata
> "Analyze competitors in the AI coding assistant space"
```

---

### cervella-reviewer

**Role:** Code review

**Specialties:**
- Pull request reviews
- Code quality checks
- Best practice enforcement
- Bug identification
- Improvement suggestions

**Example:**
```bash
spawn-workers --reviewer
> "Review the latest pull request for the auth feature"
```

---

## Agent Selection Guide

| Task Type | Primary Agent | Supporting Agents |
|-----------|---------------|-------------------|
| New feature | orchestrator | frontend, backend, tester |
| Bug fix | backend/frontend | tester |
| Performance | ingegnera | data, backend |
| Security audit | security | reviewer |
| Documentation | docs | - |
| Research | researcher | scienziata |
| Deployment | devops | guardiana-ops |
| Code review | reviewer | guardiana-qualita |

---

## Best Practices

1. **Start with the Queen** for complex tasks
2. **Use Guardians** before merging important changes
3. **Combine specialists** for full-stack features
4. **Let researchers investigate** before implementing

---

*"Ogni cervella ha il suo talento. Insieme siamo invincibili."*
*(Every brain has its talent. Together we're invincible.)*
