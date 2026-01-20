#!/usr/bin/env python3
"""
MEASURE CONTEXT TOKENS - CervellaSwarm
Misura token injection all'avvio sessione.

Uso: python3 measure_context_tokens.py [--verbose]

Token estimate: words * 1.3 (approssimazione Claude)
"""

import os
import sys
from pathlib import Path

# Files iniettati automaticamente da Claude Code
CLAUDE_MD_FILES = [
    Path.home() / ".claude/COSTITUZIONE.md",
    Path.home() / ".claude/CLAUDE.md",
    Path.home() / "Developer/CervellaSwarm/CLAUDE.md",
]

# Files iniettati da hook SessionStart
HOOK_FILES = [
    Path.home() / "Developer/CervellaSwarm/NORD.md",
    Path.home() / "Developer/CervellaSwarm/.sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md",
]

# DNA files (per reference)
DNA_FILES = [
    Path.home() / ".claude/agents/cervella-ingegnera.md",
    Path.home() / ".claude/agents/cervella-backend.md",
    Path.home() / ".claude/agents/cervella-frontend.md",
]


def count_tokens(text: str) -> int:
    """Stima token count (words * 1.3)."""
    words = len(text.split())
    return int(words * 1.3)


def measure_file(file_path: Path) -> dict:
    """Misura un singolo file."""
    if not file_path.exists():
        return {"exists": False, "path": str(file_path)}

    content = file_path.read_text(encoding='utf-8')
    lines = len(content.split('\n'))
    chars = len(content)
    words = len(content.split())
    tokens = count_tokens(content)

    return {
        "exists": True,
        "path": str(file_path),
        "name": file_path.name,
        "lines": lines,
        "chars": chars,
        "words": words,
        "tokens": tokens,
    }


def print_table(title: str, files: list, results: list):
    """Stampa tabella risultati."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    print(f"{'File':<35} {'Lines':>8} {'Chars':>10} {'Tokens':>8}")
    print(f"{'-'*35} {'-'*8} {'-'*10} {'-'*8}")

    total_lines = 0
    total_chars = 0
    total_tokens = 0

    for r in results:
        if r["exists"]:
            print(f"{r['name']:<35} {r['lines']:>8} {r['chars']:>10} {r['tokens']:>8}")
            total_lines += r['lines']
            total_chars += r['chars']
            total_tokens += r['tokens']
        else:
            print(f"{Path(r['path']).name:<35} {'N/A':>8} {'N/A':>10} {'N/A':>8}")

    print(f"{'-'*35} {'-'*8} {'-'*10} {'-'*8}")
    print(f"{'TOTALE':<35} {total_lines:>8} {total_chars:>10} {total_tokens:>8}")

    return total_tokens


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print("\n" + "="*60)
    print(" CONTEXT TOKEN MEASUREMENT - CervellaSwarm")
    print(" " + "="*58)

    # Misura CLAUDE.md files
    claude_results = [measure_file(f) for f in CLAUDE_MD_FILES]
    claude_tokens = print_table("CLAUDE.md Files (Auto-injected)", CLAUDE_MD_FILES, claude_results)

    # Misura Hook files
    hook_results = [measure_file(f) for f in HOOK_FILES]
    hook_tokens = print_table("Hook SessionStart Files", HOOK_FILES, hook_results)

    # Misura DNA files (sample)
    if verbose:
        dna_results = [measure_file(f) for f in DNA_FILES]
        dna_tokens = print_table("DNA Agent Files (Sample)", DNA_FILES, dna_results)
    else:
        dna_tokens = 0

    # Stima load_context output
    load_context_estimate = 1500  # Da audit

    # Totale
    print("\n" + "="*60)
    print(" SUMMARY")
    print("="*60)
    print(f"{'Source':<35} {'Tokens':>10}")
    print(f"{'-'*35} {'-'*10}")
    print(f"{'CLAUDE.md files':<35} {claude_tokens:>10}")
    print(f"{'Hook files (NORD + PR)':<35} {hook_tokens:>10}")
    print(f"{'load_context output (estimate)':<35} {load_context_estimate:>10}")
    print(f"{'-'*35} {'-'*10}")

    total = claude_tokens + hook_tokens + load_context_estimate
    print(f"{'TOTAL INJECTION':<35} {total:>10}")

    # Target comparison
    target = 8000
    print(f"\n{'Target':<35} {target:>10}")
    print(f"{'Difference':<35} {total - target:>+10}")
    print(f"{'Reduction needed':<35} {((total - target) / total * 100):>9.1f}%")

    print("\n" + "="*60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
