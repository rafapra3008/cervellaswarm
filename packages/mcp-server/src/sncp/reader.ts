/**
 * SNCP Reader - Read CervellaSwarm memory files via MCP
 *
 * Provides access to SNCP project files:
 * - PROMPT_RIPRESA (session context)
 * - MEMORY.md (project memory)
 * - roadmaps and other docs
 *
 * Version: 1.0.0
 * Date: 2026-02-10 - Sessione 352 (Step D.2)
 */

import { existsSync } from "node:fs";
import { readFile, readdir, stat } from "node:fs/promises";
import { join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Internal project list -- used for search defaults, NOT exposed in tool schemas
// (exposing private project names in MCP tool schemas is a privacy leak)
// NOTE: Auto-discovered at runtime via discoverProjects(). This static list is a fallback only.
const FALLBACK_PROJECTS = ["cervellaswarm", "miracollo", "contabilita", "economato", "lumine"] as const;
export type SncpProject = string;

// File types available per project
// NOTE: stato.md eliminated in SNCP 4.0 (S357). Only PROMPT_RIPRESA and MEMORY survive.
const FILE_TYPES = {
  PROMPT_RIPRESA: "PROMPT_RIPRESA",
  MEMORY: "MEMORY",
} as const;
export type SncpFileType = keyof typeof FILE_TYPES;

/**
 * Find the SNCP root directory.
 * Strategy: env var > walk up from CWD > fall back to relative from module.
 */
export function getSncpRoot(): string {
  // Priority 1: Environment variable (most reliable for MCP servers)
  const envRoot = process.env.CERVELLASWARM_SNCP_ROOT;
  if (envRoot) {
    return resolve(envRoot, "progetti");
  }

  // Priority 2: Walk up from CWD looking for .sncp/progetti/
  let dir = process.cwd();
  for (let i = 0; i < 10; i++) {
    const candidate = join(dir, ".sncp", "progetti");
    if (existsSync(candidate)) {
      return candidate;
    }
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }

  // Priority 3: Fall back to relative path from module location
  // From dist/sncp/reader.js -> go up 4 levels to CervellaSwarm/
  return resolve(__dirname, "..", "..", "..", "..", ".sncp", "progetti");
}

/**
 * Discover projects at runtime by scanning .sncp/progetti/ directory.
 * Falls back to FALLBACK_PROJECTS if directory scan fails.
 */
async function discoverProjects(): Promise<string[]> {
  const root = getSncpRoot();
  try {
    const entries = await readdir(root);
    const projects: string[] = [];
    for (const entry of entries) {
      const projectDir = join(root, entry);
      try {
        const stats = await stat(projectDir);
        if (!stats.isDirectory()) continue;
        // Only include projects that have a PROMPT_RIPRESA file
        const files = await readdir(projectDir);
        if (files.some((f) => f.startsWith("PROMPT_RIPRESA_"))) {
          projects.push(entry);
        }
      } catch (e) {
        console.warn(`discoverProjects: skipping ${entry}: ${e}`);
        continue;
      }
    }
    return projects.length > 0 ? projects : [...FALLBACK_PROJECTS];
  } catch (e) {
    console.warn(`discoverProjects: scan failed, using fallback: ${e}`);
    return [...FALLBACK_PROJECTS];
  }
}

/**
 * Read a project file by type.
 */
export async function readProjectFile(
  project: SncpProject,
  fileType: SncpFileType
): Promise<{ content: string; path: string }> {
  const root = getSncpRoot();
  let fileName: string;

  switch (fileType) {
    case "PROMPT_RIPRESA":
      fileName = `PROMPT_RIPRESA_${project}.md`;
      break;
    case "MEMORY":
      fileName = "MEMORY.md";
      break;
  }

  const filePath = join(root, project, fileName);
  assertWithinRoot(root, filePath);

  const content = await readFile(filePath, "utf-8");
  return { content, path: filePath };
}

/**
 * List all SNCP projects with basic info.
 */
export async function listProjects(): Promise<
  Array<{
    name: string;
    hasPromptRipresa: boolean;
    /** @deprecated stato.md eliminated in SNCP 4.0 - always false */
    hasStato: false;
    hasMemory: boolean;
    files: string[];
  }>
> {
  const root = getSncpRoot();
  const results: Array<{
    name: string;
    hasPromptRipresa: boolean;
    /** @deprecated stato.md eliminated in SNCP 4.0 - always false */
    hasStato: false;
    hasMemory: boolean;
    files: string[];
  }> = [];

  let entries: string[];
  try {
    entries = await readdir(root);
  } catch {
    return [];
  }

  for (const entry of entries) {
    const projectDir = join(root, entry);
    try {
      const stats = await stat(projectDir);
      if (!stats.isDirectory()) continue;
    } catch {
      continue;
    }

    let projectFiles: string[];
    try {
      projectFiles = await readdir(projectDir);
    } catch {
      continue;
    }

    results.push({
      name: entry,
      hasPromptRipresa: projectFiles.some((f) =>
        f.startsWith("PROMPT_RIPRESA_")
      ),
      hasStato: false, // stato.md eliminated in SNCP 4.0 (S357)
      hasMemory: projectFiles.includes("MEMORY.md"),
      files: projectFiles.filter((f) => f.endsWith(".md")),
    });
  }

  return results;
}

/**
 * Search SNCP files for a query string (case-insensitive).
 */
export async function searchSncp(
  query: string,
  project?: SncpProject
): Promise<
  Array<{
    project: string;
    file: string;
    matches: Array<{ line: number; text: string }>;
  }>
> {
  const root = getSncpRoot();
  const results: Array<{
    project: string;
    file: string;
    matches: Array<{ line: number; text: string }>;
  }> = [];

  const projectsToSearch = project ? [project] : await discoverProjects();
  const queryLower = query.toLowerCase();

  for (const proj of projectsToSearch) {
    const projectDir = join(root, proj);
    assertWithinRoot(root, projectDir);
    let files: string[];
    try {
      files = await readdir(projectDir);
    } catch {
      continue;
    }

    for (const file of files) {
      if (!file.endsWith(".md")) continue;

      const filePath = join(projectDir, file);
      let content: string;
      try {
        content = await readFile(filePath, "utf-8");
      } catch {
        continue;
      }

      const matches: Array<{ line: number; text: string }> = [];
      const lines = content.split("\n");
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes(queryLower)) {
          matches.push({ line: i + 1, text: lines[i].trim() });
        }
      }

      if (matches.length > 0) {
        results.push({ project: proj, file, matches });
      }
    }

    // Search subdirectories (roadmaps, reports, studi, ricerche, memoria)
    const subdirs = ["roadmaps", "reports", "studi", "ricerche", "memoria"];
    for (const subdir of subdirs) {
      const subdirPath = join(projectDir, subdir);
      assertWithinRoot(root, subdirPath);
      let subdirFiles: string[];
      try {
        subdirFiles = await readdir(subdirPath);
      } catch {
        continue;
      }

      for (const file of subdirFiles) {
        if (!file.endsWith(".md")) continue;

        const filePath = join(subdirPath, file);
        // Skip archived files (both English "archive" and Italian "archivio")
        if (filePath.includes("/archive/") || filePath.includes("/archivio/")) continue;
        let content: string;
        try {
          const stats = await stat(filePath);
          if (!stats.isFile()) continue;
          content = await readFile(filePath, "utf-8");
        } catch {
          continue;
        }

        const matches: Array<{ line: number; text: string }> = [];
        const lines = content.split("\n");
        for (let i = 0; i < lines.length; i++) {
          if (lines[i].toLowerCase().includes(queryLower)) {
            matches.push({ line: i + 1, text: lines[i].trim() });
          }
        }

        if (matches.length > 0) {
          results.push({ project: proj, file: `${subdir}/${file}`, matches });
        }
      }
    }
  }

  return results;
}

/**
 * Validate that a resolved path stays within the SNCP root.
 * Defense-in-depth: even if Zod validation is bypassed, prevent path traversal.
 */
function assertWithinRoot(root: string, targetPath: string): void {
  const resolvedRoot = resolve(root);
  const resolvedTarget = resolve(targetPath);
  if (!resolvedTarget.startsWith(resolvedRoot + sep) && resolvedTarget !== resolvedRoot) {
    throw new Error(`Path traversal blocked: target is outside SNCP root`);
  }
}

export { FALLBACK_PROJECTS, FILE_TYPES, assertWithinRoot, discoverProjects };
