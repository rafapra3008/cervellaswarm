#!/usr/bin/env python3
"""
SNCP Smart Search - BM25 Based Intelligent Search

Ricerca intelligente nei file SNCP usando BM25Plus algorithm.
Ottimizzato per documenti corti (log, note, decisioni).

Usage:
    python3 smart-search.py "query string" /path/to/search
    python3 smart-search.py "SSE real-time" .sncp/progetti/miracollo/

Output: JSON con [{file, score, snippet}, ...]
Target: <500ms per ~100 file
"""

__version__ = "1.1.0"
__version_date__ = "2026-02-02"
__changelog__ = "Added explainable search: matched_terms, match_positions, explanation"

import os
import sys
import json
import glob
import re
from pathlib import Path
from typing import List, Dict, Tuple

try:
    from rank_bm25 import BM25Plus
except ImportError:
    print("ERROR: rank-bm25 not installed", file=sys.stderr)
    print("Install with: pip3 install rank-bm25", file=sys.stderr)
    sys.exit(1)


def preprocess_text(text: str) -> List[str]:
    """
    Preprocessing testo per BM25.

    - Lowercase
    - Rimuove punteggiatura
    - Split in token
    """
    # Lowercase
    text = text.lower()

    # Rimuove punteggiatura (mantiene spazi)
    text = re.sub(r'[^\w\s]', ' ', text)

    # Split e rimuove token vuoti
    tokens = [t for t in text.split() if t]

    return tokens


def read_markdown_files(directory: str) -> List[Tuple[str, str]]:
    """
    Legge tutti i file .md nella directory (ricorsivo).

    Returns:
        List di tuple (filepath, content)
    """
    files_content = []

    # Glob ricorsivo per .md
    pattern = os.path.join(directory, "**/*.md")
    md_files = glob.glob(pattern, recursive=True)

    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

                # Skip file vuoti
                if content.strip():
                    files_content.append((filepath, content))

        except Exception as e:
            # Log errore ma continua
            print(f"WARNING: Cannot read {filepath}: {e}", file=sys.stderr)
            continue

    return files_content


def get_match_details(content: str, query_tokens: List[str]) -> Dict:
    """
    Calcola dettagli di match per explainability.

    Returns:
        Dict con matched_terms, match_positions, explanation
    """
    content_lower = content.lower()
    content_tokens = set(preprocess_text(content))

    # Quali query tokens sono presenti nel documento
    matched_terms = []
    match_positions = []

    for token in query_tokens:
        if token in content_tokens:
            matched_terms.append(token)
            # Trova TUTTE le posizioni del token (non solo la prima)
            start = 0
            while True:
                pos = content_lower.find(token, start)
                if pos == -1:
                    break
                match_positions.append(pos)
                start = pos + 1

    # Calcola frequenza media dei termini matchati
    term_frequencies = []
    for token in matched_terms:
        freq = content_lower.count(token)
        term_frequencies.append(freq)

    avg_freq = sum(term_frequencies) / len(term_frequencies) if term_frequencies else 0

    # Genera explanation
    total_query_terms = len(query_tokens)
    matched_count = len(matched_terms)

    if matched_count == 0:
        explanation = "No direct term matches, ranked by document similarity"
    elif matched_count == total_query_terms:
        explanation = f"All {matched_count} query terms matched"
        if avg_freq > 3:
            explanation += f", high frequency (avg {avg_freq:.1f} occurrences)"
        elif avg_freq > 1:
            explanation += f", moderate frequency (avg {avg_freq:.1f} occurrences)"
    else:
        explanation = f"Matched {matched_count}/{total_query_terms} query terms"
        if avg_freq > 1:
            explanation += f" with avg {avg_freq:.1f} occurrences"

    return {
        "matched_terms": matched_terms,
        "match_positions": sorted(match_positions),
        "explanation": explanation
    }


def extract_snippet(content: str, query_tokens: List[str], context_chars: int = 150) -> str:
    """
    Estrae snippet rilevante dal contenuto.

    Trova la prima occorrenza di un token della query
    e ritorna contesto attorno.
    """
    content_lower = content.lower()

    # Trova prima occorrenza di qualsiasi token
    best_pos = -1
    for token in query_tokens:
        pos = content_lower.find(token)
        if pos != -1 and (best_pos == -1 or pos < best_pos):
            best_pos = pos

    # Nessuna match diretta - ritorna inizio
    if best_pos == -1:
        return content[:context_chars] + "..."

    # Estrai contesto
    start = max(0, best_pos - context_chars // 2)
    end = min(len(content), best_pos + context_chars // 2)

    snippet = content[start:end]

    # Aggiungi ellipsis
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."

    return snippet


def search_bm25(query: str, directory: str, top_k: int = 10) -> List[Dict]:
    """
    Esegue ricerca BM25 nei file markdown.

    Args:
        query: Query string
        directory: Path directory da cercare
        top_k: Numero massimo risultati

    Returns:
        Lista dizionari [{file, score, snippet}, ...]
    """
    # Leggi tutti i file
    files_content = read_markdown_files(directory)

    if not files_content:
        return []

    # Separa path e contenuti
    filepaths = [fc[0] for fc in files_content]
    contents = [fc[1] for fc in files_content]

    # Tokenizza documenti
    tokenized_docs = [preprocess_text(content) for content in contents]

    # Crea BM25Plus index
    bm25 = BM25Plus(tokenized_docs)

    # Tokenizza query (stesso preprocessing!)
    query_tokens = preprocess_text(query)

    # Esegui ricerca
    scores = bm25.get_scores(query_tokens)

    # Ordina per score (desc)
    indexed_scores = [(i, score) for i, score in enumerate(scores)]
    indexed_scores.sort(key=lambda x: x[1], reverse=True)

    # Prendi top_k
    top_results = indexed_scores[:top_k]

    # Formatta risultati
    results = []
    for idx, score in top_results:
        # Skip risultati con score troppo basso (irrilevanti)
        if score < 0.1:
            continue

        filepath = filepaths[idx]
        content = contents[idx]
        snippet = extract_snippet(content, query_tokens)

        # NEW: Explainable search details
        match_details = get_match_details(content, query_tokens)

        results.append({
            "file": filepath,
            "score": round(score, 3),
            "snippet": snippet,
            "matched_terms": match_details["matched_terms"],
            "match_positions": match_details["match_positions"],
            "explanation": match_details["explanation"]
        })

    return results


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: smart-search.py <query> <directory>", file=sys.stderr)
        print("Example: smart-search.py 'SSE real-time' .sncp/progetti/miracollo/", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    directory = sys.argv[2]

    # Verifica directory esiste
    if not os.path.isdir(directory):
        print(f"ERROR: Directory not found: {directory}", file=sys.stderr)
        sys.exit(1)

    # Esegui ricerca
    results = search_bm25(query, directory)

    # Output JSON
    output = {
        "query": query,
        "directory": directory,
        "results_count": len(results),
        "results": results
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
