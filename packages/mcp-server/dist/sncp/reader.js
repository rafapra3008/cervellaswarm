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
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// Known SNCP projects
const KNOWN_PROJECTS = ["cervellaswarm", "miracollo", "contabilita", "cervellacostruzione"];
// File types available per project
// NOTE: stato.md eliminated in SNCP 4.0 (S357). Only PROMPT_RIPRESA and MEMORY survive.
const FILE_TYPES = {
    PROMPT_RIPRESA: "PROMPT_RIPRESA",
    MEMORY: "MEMORY",
};
/**
 * Find the SNCP root directory.
 * Strategy: env var > walk up from CWD > fall back to relative from module.
 */
export function getSncpRoot() {
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
        if (parent === dir)
            break;
        dir = parent;
    }
    // Priority 3: Fall back to relative path from module location
    // From dist/sncp/reader.js -> go up 4 levels to CervellaSwarm/
    return resolve(__dirname, "..", "..", "..", "..", ".sncp", "progetti");
}
/**
 * Read a project file by type.
 */
export async function readProjectFile(project, fileType) {
    const root = getSncpRoot();
    let fileName;
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
export async function listProjects() {
    const root = getSncpRoot();
    const results = [];
    let entries;
    try {
        entries = await readdir(root);
    }
    catch {
        return [];
    }
    for (const entry of entries) {
        const projectDir = join(root, entry);
        try {
            const stats = await stat(projectDir);
            if (!stats.isDirectory())
                continue;
        }
        catch {
            continue;
        }
        let projectFiles;
        try {
            projectFiles = await readdir(projectDir);
        }
        catch {
            continue;
        }
        results.push({
            name: entry,
            hasPromptRipresa: projectFiles.some((f) => f.startsWith("PROMPT_RIPRESA_")),
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
export async function searchSncp(query, project) {
    const root = getSncpRoot();
    const results = [];
    const projectsToSearch = project ? [project] : KNOWN_PROJECTS;
    const queryLower = query.toLowerCase();
    for (const proj of projectsToSearch) {
        const projectDir = join(root, proj);
        assertWithinRoot(root, projectDir);
        let files;
        try {
            files = await readdir(projectDir);
        }
        catch {
            continue;
        }
        for (const file of files) {
            if (!file.endsWith(".md"))
                continue;
            const filePath = join(projectDir, file);
            let content;
            try {
                content = await readFile(filePath, "utf-8");
            }
            catch {
                continue;
            }
            const matches = [];
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
        // Also search roadmaps/ subdirectory
        const roadmapsDir = join(projectDir, "roadmaps");
        assertWithinRoot(root, roadmapsDir);
        let roadmapFiles;
        try {
            roadmapFiles = await readdir(roadmapsDir);
        }
        catch {
            continue;
        }
        for (const file of roadmapFiles) {
            if (!file.endsWith(".md"))
                continue;
            const filePath = join(roadmapsDir, file);
            let content;
            try {
                content = await readFile(filePath, "utf-8");
            }
            catch {
                continue;
            }
            const matches = [];
            const lines = content.split("\n");
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].toLowerCase().includes(queryLower)) {
                    matches.push({ line: i + 1, text: lines[i].trim() });
                }
            }
            if (matches.length > 0) {
                results.push({ project: proj, file: `roadmaps/${file}`, matches });
            }
        }
    }
    return results;
}
/**
 * Validate that a resolved path stays within the SNCP root.
 * Defense-in-depth: even if Zod validation is bypassed, prevent path traversal.
 */
function assertWithinRoot(root, targetPath) {
    const resolvedRoot = resolve(root);
    const resolvedTarget = resolve(targetPath);
    if (!resolvedTarget.startsWith(resolvedRoot + "/") && resolvedTarget !== resolvedRoot) {
        throw new Error(`Path traversal blocked: target is outside SNCP root`);
    }
}
export { KNOWN_PROJECTS, FILE_TYPES, assertWithinRoot };
//# sourceMappingURL=reader.js.map