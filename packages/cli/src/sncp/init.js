/**
 * SNCP Initializer
 *
 * Creates the .sncp folder structure for a project.
 * SNCP = Sistema Nervoso Centrale Progetti
 *
 * "MINIMO in memoria, MASSIMO su disco"
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
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

  // NOTE: stato.md eliminated in SNCP 4.0 (S357). Only PROMPT_RIPRESA survives.

  // Create initial PROMPT_RIPRESA
  const promptRipresaContent = `# PROMPT RIPRESA - ${answers.projectName}

<!-- LIMITI: Questo file deve restare < 150 righe -->
<!-- Se cresce troppo, archivia sessioni vecchie in .sncp/archivio/ -->

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
!PROMPT_RIPRESA_*.md
`;

  await writeFile(join(sncpPath, '.gitignore'), gitignoreContent, 'utf8');
}
