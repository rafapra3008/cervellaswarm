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
declare const KNOWN_PROJECTS: readonly ["cervellaswarm", "miracollo", "contabilita", "cervellacostruzione"];
export type SncpProject = (typeof KNOWN_PROJECTS)[number];
declare const FILE_TYPES: {
    readonly PROMPT_RIPRESA: "PROMPT_RIPRESA";
    readonly MEMORY: "MEMORY";
};
export type SncpFileType = keyof typeof FILE_TYPES;
/**
 * Find the SNCP root directory.
 * Strategy: env var > walk up from CWD > fall back to relative from module.
 */
export declare function getSncpRoot(): string;
/**
 * Read a project file by type.
 */
export declare function readProjectFile(project: SncpProject, fileType: SncpFileType): Promise<{
    content: string;
    path: string;
}>;
/**
 * List all SNCP projects with basic info.
 */
export declare function listProjects(): Promise<Array<{
    name: string;
    hasPromptRipresa: boolean;
    /** @deprecated stato.md eliminated in SNCP 4.0 - always false */
    hasStato: false;
    hasMemory: boolean;
    files: string[];
}>>;
/**
 * Search SNCP files for a query string (case-insensitive).
 */
export declare function searchSncp(query: string, project?: SncpProject): Promise<Array<{
    project: string;
    file: string;
    matches: Array<{
        line: number;
        text: string;
    }>;
}>>;
/**
 * Validate that a resolved path stays within the SNCP root.
 * Defense-in-depth: even if Zod validation is bypassed, prevent path traversal.
 */
declare function assertWithinRoot(root: string, targetPath: string): void;
export { KNOWN_PROJECTS, FILE_TYPES, assertWithinRoot };
//# sourceMappingURL=reader.d.ts.map