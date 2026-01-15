/**
 * SNCP Loader
 *
 * Loads project context from .sncp folder.
 * Reads the project's constitution and state.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import { readFile, access, readdir } from 'fs/promises';
import { join } from 'path';

export async function loadProjectContext() {
  const projectPath = process.cwd();
  const sncpPath = join(projectPath, '.sncp');
  const projectsPath = join(sncpPath, 'progetti');

  try {
    await access(projectsPath);
  } catch {
    return null;
  }

  try {
    // Find project folder (first one found)
    const projects = await readdir(projectsPath);
    if (projects.length === 0) {
      return null;
    }

    const projectName = projects[0];
    const projectSncpPath = join(projectsPath, projectName);

    // Try to load project.json (optional - graceful degradation if missing)
    let projectData = null;
    try {
      const projectJsonPath = join(projectSncpPath, 'project.json');
      const content = await readFile(projectJsonPath, 'utf8');
      projectData = JSON.parse(content);
    } catch {
      // Graceful degradation: no project.json, infer from folder name
      // This is intentional - older projects may not have this file
      projectData = { projectName };
    }

    // Try to load stato.md for progress (optional)
    let statoContent = null;
    try {
      const statoPath = join(projectSncpPath, 'stato.md');
      statoContent = await readFile(statoPath, 'utf8');
    } catch {
      // Graceful degradation: stato.md is optional
      // Progress will default to 0% if not found
    }

    // Try to load PROMPT_RIPRESA for last session (optional)
    let promptRipresa = null;
    try {
      const promptPath = join(projectSncpPath, `PROMPT_RIPRESA_${projectName}.md`);
      promptRipresa = await readFile(promptPath, 'utf8');
    } catch {
      // Graceful degradation: PROMPT_RIPRESA is optional
      // lastSession will be null if not found
    }

    // Parse progress from stato.md
    let progress = 0;
    let nextStep = 'Run your first task with: cervellaswarm task "description"';

    if (statoContent) {
      // Count completed checkboxes
      const completed = (statoContent.match(/\[x\]/gi) || []).length;
      const total = (statoContent.match(/\[ \]/gi) || []).length + completed;
      if (total > 0) {
        progress = Math.round((completed / total) * 100);
      }

      // Extract next step from unchecked items
      const unchecked = statoContent.match(/\[ \] ([^\n]+)/);
      if (unchecked) {
        nextStep = unchecked[1];
      }
    }

    // Parse last session from PROMPT_RIPRESA
    let lastSession = null;
    if (promptRipresa) {
      const dateMatch = promptRipresa.match(/Ultimo aggiornamento:\*\* ([0-9-]+)/);
      if (dateMatch) {
        lastSession = {
          date: dateMatch[1],
          summary: 'Previous session documented in PROMPT_RIPRESA'
        };
      }
    }

    return {
      name: projectData.projectName || projectName,
      description: projectData.description || 'A CervellaSwarm project',
      goal: projectData.mainGoal || projectData.description || 'Building something great',
      projectType: projectData.projectType || 'unknown',
      techStack: projectData.techStack || null,
      timeline: projectData.timeline || 'exploratory',
      progress,
      nextStep,
      lastSession,
      sncpPath: projectSncpPath
    };

  } catch (error) {
    console.error('Error loading project context:', error);
    return null;
  }
}
