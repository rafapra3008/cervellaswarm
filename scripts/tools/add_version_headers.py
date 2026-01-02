#!/usr/bin/env python3
"""
CervellaSwarm - Add Version Headers to Agent Files
===================================================

Aggiunge o aggiorna i campi version/updated/compatible_with
nel frontmatter YAML dei file agent.

Versione: 1.0.0
Data: 2 Gennaio 2026

USAGE:
    python3 add_version_headers.py                    # Preview changes
    python3 add_version_headers.py --apply            # Apply changes
    python3 add_version_headers.py --version 1.0.0    # Set specific version
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Add parent to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_agents_path, list_agents


DEFAULT_VERSION = "1.0.0"
DEFAULT_COMPATIBLE = "cervellaswarm >= 1.0.0"


def parse_frontmatter(content: str) -> tuple:
    """
    Estrae il frontmatter YAML da un file Markdown.

    Returns:
        tuple: (frontmatter_dict, rest_of_content, original_frontmatter_text)
    """
    # Pattern per frontmatter YAML (--- ... ---)
    pattern = r'^---\n(.*?)\n---\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content, ""

    frontmatter_text = match.group(1)
    rest_content = match.group(2)

    # Parse frontmatter (semplice key: value)
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, rest_content, frontmatter_text


def build_frontmatter(data: dict) -> str:
    """
    Costruisce il testo frontmatter YAML da un dizionario.

    Ordine dei campi:
    1. name
    2. version
    3. updated
    4. compatible_with
    5. description
    6. tools
    7. model
    8. altri campi
    """
    # Ordine preferito dei campi
    order = ['name', 'version', 'updated', 'compatible_with', 'description', 'tools', 'model']

    lines = []
    added = set()

    # Prima aggiungi i campi nell'ordine preferito
    for key in order:
        if key in data:
            lines.append(f"{key}: {data[key]}")
            added.add(key)

    # Poi aggiungi eventuali altri campi
    for key, value in data.items():
        if key not in added:
            lines.append(f"{key}: {value}")

    return '\n'.join(lines)


def update_agent_file(filepath: Path, version: str, dry_run: bool = True) -> dict:
    """
    Aggiorna un file agent con version headers.

    Args:
        filepath: Path al file agent
        version: Versione da impostare
        dry_run: Se True, non salva le modifiche

    Returns:
        dict con info sulle modifiche
    """
    content = filepath.read_text()
    frontmatter, rest_content, original_fm = parse_frontmatter(content)

    result = {
        'file': filepath.name,
        'had_frontmatter': bool(frontmatter),
        'changes': [],
        'new_frontmatter': None
    }

    if not frontmatter:
        result['error'] = "No frontmatter found"
        return result

    # Campi da aggiungere/aggiornare
    today = datetime.now().strftime("%Y-%m-%d")

    if 'version' not in frontmatter:
        frontmatter['version'] = version
        result['changes'].append(f"Added version: {version}")
    elif frontmatter['version'] != version:
        old_version = frontmatter['version']
        frontmatter['version'] = version
        result['changes'].append(f"Updated version: {old_version} -> {version}")

    if 'updated' not in frontmatter or frontmatter['updated'] != today:
        old_updated = frontmatter.get('updated', '(none)')
        frontmatter['updated'] = today
        result['changes'].append(f"Updated date: {old_updated} -> {today}")

    if 'compatible_with' not in frontmatter:
        frontmatter['compatible_with'] = DEFAULT_COMPATIBLE
        result['changes'].append(f"Added compatible_with: {DEFAULT_COMPATIBLE}")

    # Ricostruisci il file
    new_frontmatter = build_frontmatter(frontmatter)
    result['new_frontmatter'] = new_frontmatter

    if not dry_run and result['changes']:
        new_content = f"---\n{new_frontmatter}\n---\n{rest_content}"
        filepath.write_text(new_content)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Add version headers to CervellaSwarm agent files"
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes (default is dry-run/preview)'
    )
    parser.add_argument(
        '--version',
        default=DEFAULT_VERSION,
        help=f'Version to set (default: {DEFAULT_VERSION})'
    )
    parser.add_argument(
        '--agents-path',
        type=Path,
        help='Custom path to agents directory'
    )

    args = parser.parse_args()

    # Get agents path
    agents_path = args.agents_path or get_agents_path()

    if not agents_path.exists():
        print(f"ERROR: Agents path not found: {agents_path}")
        sys.exit(1)

    # Find all agent files
    agent_files = list(agents_path.glob("cervella-*.md"))

    if not agent_files:
        print(f"ERROR: No agent files found in {agents_path}")
        sys.exit(1)

    print("=" * 60)
    print("CervellaSwarm - Version Headers Tool")
    print("=" * 60)
    print(f"Agents path: {agents_path}")
    print(f"Version:     {args.version}")
    print(f"Mode:        {'APPLY' if args.apply else 'DRY-RUN (preview)'}")
    print(f"Files found: {len(agent_files)}")
    print("-" * 60)

    total_changes = 0
    errors = 0

    for filepath in sorted(agent_files):
        result = update_agent_file(filepath, args.version, dry_run=not args.apply)

        if 'error' in result:
            print(f"  {result['file']}: ERROR - {result['error']}")
            errors += 1
            continue

        if result['changes']:
            print(f"  {result['file']}:")
            for change in result['changes']:
                print(f"    - {change}")
            total_changes += len(result['changes'])
        else:
            print(f"  {result['file']}: (no changes needed)")

    print("-" * 60)
    print(f"SUMMARY:")
    print(f"  Files processed: {len(agent_files)}")
    print(f"  Total changes:   {total_changes}")
    print(f"  Errors:          {errors}")

    if not args.apply and total_changes > 0:
        print("\n  Run with --apply to save changes")

    print("=" * 60)


if __name__ == "__main__":
    main()
