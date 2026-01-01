#!/usr/bin/env python3
"""
L'Ingegnera - Analisi Codebase Automatica
Trova file grandi, codice duplicato, TODO dimenticati.

v1.0.0 - 1 Gennaio 2026
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Rich per progress bar (fallback se non disponibile)
try:
    from rich.progress import track
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    def track(items, description="Processing..."):
        """Fallback quando Rich non è disponibile"""
        print(f"{description}")
        return items

__version__ = "1.0.0"
__version_date__ = "2026-01-01"


# CONFIGURAZIONE
EXCLUDED_DIRS = {
    'node_modules', '.git', '__pycache__', 'venv', '.venv',
    'dist', 'build', '.next', '.nuxt', 'coverage'
}

EXCLUDED_FILES = {
    '.min.js', '.min.css', '.map', '.lock', 'package-lock.json', 'yarn.lock'
}

EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.md', '.css', '.html'
}

MAX_FILE_SIZE = 500  # righe
MAX_FUNCTION_SIZE = 50  # righe

# Pattern per TODO/FIXME
TODO_PATTERN = re.compile(
    r'#\s*(TODO|FIXME|HACK|XXX|BUG):?\s*(.+)',
    re.IGNORECASE
)

# Pattern per funzioni Python
PYTHON_FUNCTION_PATTERN = re.compile(
    r'^\s*(def|async def)\s+(\w+)\s*\(',
    re.MULTILINE
)

# Pattern per funzioni JavaScript/TypeScript
JS_FUNCTION_PATTERN = re.compile(
    r'^\s*(function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(|export\s+(?:async\s+)?function\s+\w+)',
    re.MULTILINE
)


class CodebaseAnalyzer:
    """Analizzatore principale della codebase"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results = {
            'large_files': [],
            'large_functions': [],
            'todos': [],
            'duplicates': [],
            'stats': {
                'total_files': 0,
                'total_lines': 0,
                'total_issues': 0
            }
        }
        self.file_hashes = defaultdict(list)

    def should_skip(self, path: Path) -> bool:
        """Verifica se un path deve essere saltato"""
        # Controlla directory escluse
        for part in path.parts:
            if part in EXCLUDED_DIRS:
                return True

        # Controlla file esclusi
        for excluded in EXCLUDED_FILES:
            if path.name.endswith(excluded):
                return True

        return False

    def get_files(self) -> List[Path]:
        """Ottiene tutti i file da analizzare"""
        files = []
        for ext in EXTENSIONS:
            for file_path in self.project_path.rglob(f'*{ext}'):
                if not self.should_skip(file_path):
                    files.append(file_path)
        return files

    def analyze_file_size(self, file_path: Path, content: str) -> None:
        """Analizza dimensione file"""
        lines = content.split('\n')
        line_count = len(lines)

        self.results['stats']['total_lines'] += line_count

        if line_count > MAX_FILE_SIZE:
            relative_path = file_path.relative_to(self.project_path)
            self.results['large_files'].append({
                'file': str(relative_path),
                'lines': line_count,
                'suggestion': self._suggest_split(file_path)
            })
            self.results['stats']['total_issues'] += 1

    def _suggest_split(self, file_path: Path) -> str:
        """Suggerisce come splittare un file grande"""
        if file_path.suffix in ['.jsx', '.tsx']:
            return "Split in componenti separati"
        elif file_path.suffix == '.py':
            return "Split in moduli separati"
        elif file_path.suffix == '.md':
            return "Split in sezioni separate"
        return "Considera splitting in file multipli"

    def analyze_functions(self, file_path: Path, content: str) -> None:
        """Analizza dimensione funzioni"""
        if file_path.suffix == '.py':
            pattern = PYTHON_FUNCTION_PATTERN
        elif file_path.suffix in ['.js', '.jsx', '.ts', '.tsx']:
            pattern = JS_FUNCTION_PATTERN
        else:
            return

        lines = content.split('\n')
        relative_path = file_path.relative_to(self.project_path)

        # Trova tutte le funzioni
        for match in pattern.finditer(content):
            start_line = content[:match.start()].count('\n') + 1

            # Calcola dimensione funzione (approssimativa)
            # Cerca prossima funzione o fine file
            next_match = None
            for m in pattern.finditer(content[match.end():]):
                next_match = m
                break

            if next_match:
                end_pos = match.end() + next_match.start()
            else:
                end_pos = len(content)

            function_content = content[match.start():end_pos]
            function_lines = function_content.count('\n')

            if function_lines > MAX_FUNCTION_SIZE:
                self.results['large_functions'].append({
                    'file': str(relative_path),
                    'line': start_line,
                    'lines': function_lines,
                    'name': match.group(2) if file_path.suffix == '.py' else 'function'
                })
                self.results['stats']['total_issues'] += 1

    def analyze_todos(self, file_path: Path, content: str) -> None:
        """Trova TODO/FIXME/HACK"""
        lines = content.split('\n')
        relative_path = file_path.relative_to(self.project_path)

        for line_num, line in enumerate(lines, 1):
            match = TODO_PATTERN.search(line)
            if match:
                self.results['todos'].append({
                    'file': str(relative_path),
                    'line': line_num,
                    'type': match.group(1).upper(),
                    'content': match.group(2).strip()
                })
                self.results['stats']['total_issues'] += 1

    def analyze_duplicates(self, file_path: Path, content: str) -> None:
        """Trova file duplicati (stesso hash)"""
        # Hash del contenuto
        file_hash = hashlib.md5(content.encode()).hexdigest()
        relative_path = file_path.relative_to(self.project_path)
        self.file_hashes[file_hash].append(str(relative_path))

    def finalize_duplicates(self) -> None:
        """Finalizza analisi duplicati"""
        for file_hash, files in self.file_hashes.items():
            if len(files) > 1:
                self.results['duplicates'].append({
                    'files': files,
                    'count': len(files)
                })
                self.results['stats']['total_issues'] += len(files) - 1

    def analyze(self) -> Dict:
        """Esegue analisi completa"""
        files = self.get_files()
        self.results['stats']['total_files'] = len(files)

        print(f"\n🔍 Analizzo {len(files)} file...\n")

        for file_path in track(files, description="Analisi in corso..."):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')

                self.analyze_file_size(file_path, content)
                self.analyze_functions(file_path, content)
                self.analyze_todos(file_path, content)
                self.analyze_duplicates(file_path, content)

            except Exception as e:
                print(f"⚠️  Errore analizzando {file_path}: {e}", file=sys.stderr)

        self.finalize_duplicates()
        return self.results


class ReportGenerator:
    """Generatore report markdown e JSON"""

    def __init__(self, results: Dict, project_path: str):
        self.results = results
        self.project_path = project_path
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    def generate_markdown(self) -> str:
        """Genera report markdown"""
        md = f"# 🔧 ENGINEERING REPORT - {self.timestamp}\n"
        md += f"## Progetto: {self.project_path}\n\n"

        # Summary
        md += "### 📊 Summary\n"
        md += f"- File analizzati: {self.results['stats']['total_files']}\n"
        md += f"- Righe totali: {self.results['stats']['total_lines']}\n"
        md += f"- Issues trovate: {self.results['stats']['total_issues']}\n\n"

        # Priorità
        critical_count = len([f for f in self.results['large_files'] if f['lines'] > 1000])
        high_count = len(self.results['large_files']) + len(self.results['large_functions'])
        medium_count = len(self.results['todos'])
        low_count = len(self.results['duplicates'])

        md += f"- Priorità CRITICA (>1000 righe): {critical_count}\n"
        md += f"- Priorità ALTA: {high_count}\n"
        md += f"- Priorità MEDIA: {medium_count}\n"
        md += f"- Priorità BASSA: {low_count}\n\n"

        # CRITICO
        critical_files = [f for f in self.results['large_files'] if f['lines'] > 1000]
        if critical_files:
            md += "### 🔴 CRITICO\n"
            md += "#### File Enormi (> 1000 righe)\n"
            md += "| File | Righe | Suggerimento |\n"
            md += "|------|-------|-------------|\n"
            for item in critical_files:
                md += f"| {item['file']} | {item['lines']} | {item['suggestion']} |\n"
            md += "\n"

        # ALTO
        if self.results['large_files'] or self.results['large_functions']:
            md += "### 🟠 ALTO\n"

            if self.results['large_files']:
                md += "#### File Grandi (> 500 righe)\n"
                md += "| File | Righe | Suggerimento |\n"
                md += "|------|-------|-------------|\n"
                for item in self.results['large_files'][:10]:  # Top 10
                    md += f"| {item['file']} | {item['lines']} | {item['suggestion']} |\n"
                md += "\n"

            if self.results['large_functions']:
                md += "#### Funzioni Grandi (> 50 righe)\n"
                md += "| File | Linea | Righe | Nome |\n"
                md += "|------|-------|-------|------|\n"
                for item in self.results['large_functions'][:10]:  # Top 10
                    md += f"| {item['file']} | {item['line']} | {item['lines']} | {item.get('name', 'N/A')} |\n"
                md += "\n"

        # MEDIO
        if self.results['todos']:
            md += "### 🟡 MEDIO\n"
            md += "#### TODO/FIXME Trovati\n"
            md += "| File | Linea | Tipo | Contenuto |\n"
            md += "|------|-------|------|----------|\n"
            for item in self.results['todos'][:20]:  # Top 20
                md += f"| {item['file']} | {item['line']} | {item['type']} | {item['content']} |\n"
            md += "\n"

        # BASSO
        if self.results['duplicates']:
            md += "### 🟢 BASSO\n"
            md += "#### File Duplicati\n"
            for item in self.results['duplicates']:
                md += f"- {item['count']} file identici:\n"
                for f in item['files']:
                    md += f"  - {f}\n"
            md += "\n"

        # Raccomandazioni
        md += "### 💡 Raccomandazioni\n"
        recommendations = self._generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            md += f"{i}. [ ] {rec}\n"

        return md

    def _generate_recommendations(self) -> List[str]:
        """Genera raccomandazioni prioritizzate"""
        recs = []

        # Priorità 1: File critici
        critical_files = [f for f in self.results['large_files'] if f['lines'] > 1000]
        if critical_files:
            recs.append(f"CRITICO: Split {len(critical_files)} file enormi (>1000 righe)")

        # Priorità 2: File grandi
        if self.results['large_files']:
            recs.append(f"Refactor {len(self.results['large_files'])} file grandi (>500 righe)")

        # Priorità 3: Funzioni grandi
        if self.results['large_functions']:
            recs.append(f"Split {len(self.results['large_functions'])} funzioni grandi (>50 righe)")

        # Priorità 4: TODO vecchi
        if self.results['todos']:
            fixmes = [t for t in self.results['todos'] if t['type'] == 'FIXME']
            if fixmes:
                recs.append(f"Risolvere {len(fixmes)} FIXME trovati")
            recs.append(f"Completare o rimuovere {len(self.results['todos'])} TODO")

        # Priorità 5: Duplicati
        if self.results['duplicates']:
            recs.append(f"Rimuovere {len(self.results['duplicates'])} file duplicati")

        return recs

    def generate_json(self) -> str:
        """Genera report JSON"""
        output = {
            'timestamp': self.timestamp,
            'project': self.project_path,
            'results': self.results
        }
        return json.dumps(output, indent=2)


def main():
    """Entry point CLI"""
    parser = argparse.ArgumentParser(
        description="L'Ingegnera - Analisi Codebase Automatica",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s /path/to/project
  %(prog)s /path/to/project --output report.md
  %(prog)s /path/to/project --json --output report.json
        """
    )

    parser.add_argument(
        'project_path',
        help='Path del progetto da analizzare'
    )

    parser.add_argument(
        '--output', '-o',
        help='File di output (default: stampa a schermo)',
        default=None
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in formato JSON invece di Markdown'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__} ({__version_date__})'
    )

    args = parser.parse_args()

    # Verifica progetto esiste
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"❌ Errore: Path non trovato: {project_path}", file=sys.stderr)
        sys.exit(1)

    if not project_path.is_dir():
        print(f"❌ Errore: Path non è una directory: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Analizza
    print(f"🔧 L'Ingegnera - Analisi Codebase v{__version__}")
    print(f"📂 Progetto: {project_path}\n")

    analyzer = CodebaseAnalyzer(str(project_path))
    results = analyzer.analyze()

    # Genera report
    generator = ReportGenerator(results, str(project_path))

    if args.json:
        output = generator.generate_json()
    else:
        output = generator.generate_markdown()

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding='utf-8')
        print(f"\n✅ Report salvato: {output_path}")
    else:
        print("\n" + output)

    # Summary finale
    print(f"\n📊 Analisi completata!")
    print(f"   File: {results['stats']['total_files']}")
    print(f"   Issues: {results['stats']['total_issues']}")


if __name__ == '__main__':
    main()
