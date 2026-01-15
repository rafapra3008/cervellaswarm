/**
 * SNCP Initializer
 *
 * Creates the .sncp folder structure for a project.
 * SNCP = Sistema Nervoso Centrale Progetti
 *
 * "MINIMO in memoria, MASSIMO su disco"
 */

import { mkdir, writeFile } from 'fs/promises';
import { join } from 'path';

export async function initSNCP(answers) {
  const projectPath = process.cwd();
  const sncpPath = join(projectPath, '.sncp', 'progetti', answers.projectName);

  // Create folder structure
  const folders = [
    '',
    'idee',
    'decisioni',
    'reports',
    'roadmaps',
    'workflow',
    'sessions',
    'archivio'
  ];

  for (const folder of folders) {
    await mkdir(join(sncpPath, folder), { recursive: true });
  }

  // Create initial stato.md
  const statoContent = `# ${answers.projectName} - Stato Attuale

> **Ultimo aggiornamento:** ${new Date().toISOString().split('T')[0]}
> **Fase:** Inizializzazione

---

## COSA STA SUCCEDENDO

Progetto appena inizializzato con CervellaSwarm.

---

## PROSSIMI PASSI

1. [ ] Primo task con \`cervellaswarm task\`
2. [ ] Esplorare il progetto
3. [ ] Definire la prima feature

---

## NOTE

*Questo file viene aggiornato automaticamente dallo sciame.*
*Ogni sessione lascia traccia qui.*

---

*"Un progresso al giorno = 365 progressi all'anno"*
`;

  await writeFile(join(sncpPath, 'stato.md'), statoContent, 'utf8');

  // Create initial PROMPT_RIPRESA
  const promptRipresaContent = `# PROMPT RIPRESA - ${answers.projectName}

> **Ultimo aggiornamento:** ${new Date().toISOString().split('T')[0]}

---

## STATO ATTUALE

Progetto appena inizializzato.

---

## ULTIMA SESSIONE

*Nessuna sessione precedente*

---

## PROSSIMA SESSIONE

- Iniziare il primo task
- Esplorare le possibilità

---

## CONTESTO IMPORTANTE

**Tipo progetto:** ${answers.projectType}
**Goal:** ${answers.description}

---

*Questo file aiuta la prossima sessione a partire subito.*
`;

  await writeFile(join(sncpPath, `PROMPT_RIPRESA_${answers.projectName}.md`), promptRipresaContent, 'utf8');

  // Create .gitignore for sessions folder (keep sessions local)
  const gitignoreContent = `# Keep sessions local
sessions/*.json

# But track important files
!COSTITUZIONE.md
!stato.md
!PROMPT_RIPRESA_*.md
`;

  await writeFile(join(sncpPath, '.gitignore'), gitignoreContent, 'utf8');
}
