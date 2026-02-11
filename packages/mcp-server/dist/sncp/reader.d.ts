/**
 * SNCP Reader - Read CervellaSwarm memory files via MCP
 *
 * Provides access to SNCP project files:
 * - PROMPT_RIPRESA (session context)
 * - stato.md (project state)
 * - roadmaps and other docs
 *
 * Version: 1.0.0
 * Date: 2026-02-10 - Sessione 352 (Step D.2)
 */
declare const KNOWN_PROJECTS: readonly ["cervellaswarm", "miracollo", "contabilita", "cervellacostruzione"];
export type SncpProject = (typeof KNOWN_PROJECTS)[number];
declare const FILE_TYPES: {
    readonly PROMPT_RIPRESA: "PROMPT_RIPRESA";
    readonly stato: "stato";
    readonly MEMORY: "MEMORY";
};
export type SncpFileType = keyof typeof FILE_TYPES;
/**
 * Find the SNCP root directory.
 * Strategy: go up from compiled dist/ to project root, find .sncp/progetti/
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
    hasStato: boolean;
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
export { KNOWN_PROJECTS, FILE_TYPES };
//# sourceMappingURL=reader.d.ts.map