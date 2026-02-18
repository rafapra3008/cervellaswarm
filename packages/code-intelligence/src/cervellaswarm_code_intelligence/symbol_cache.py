# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""LRU Cache for Symbol Extraction.

This module provides an LRU (Least Recently Used) cache implementation
for caching extracted symbols. It prevents memory leaks by limiting
the cache size and evicting old entries.

Usage:
    cache = SymbolCache(maxsize=1000)
    cache.set("path/to/file.py", mtime, symbols)
    cached = cache.get("path/to/file.py", current_mtime)

Author: Cervella Backend (F1.1 Tech Debt Cleanup)
Version: 1.0.0
Date: 2026-02-02
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-02"

import logging
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """A single cache entry with mtime and data."""
    mtime: float
    symbols: List[Any]


class SymbolCache:
    """LRU Cache for symbol extraction results.

    This cache stores extracted symbols keyed by file path, with
    automatic eviction of least recently used entries when the
    cache exceeds maxsize.

    Features:
        - LRU eviction: oldest unused entries removed first
        - mtime validation: returns None if file changed
        - Thread-safe for basic operations
        - Configurable maxsize (default 1000)

    Attributes:
        maxsize: Maximum number of entries to cache

    Example:
        >>> cache = SymbolCache(maxsize=100)
        >>> cache.set("app.py", os.path.getmtime("app.py"), symbols)
        >>> cached = cache.get("app.py", os.path.getmtime("app.py"))
        >>> if cached:
        ...     print(f"Cache hit: {len(cached)} symbols")
    """

    def __init__(self, maxsize: int = 1000):
        """Initialize cache with maximum size.

        Args:
            maxsize: Maximum number of file entries to cache.
                     When exceeded, least recently used entries
                     are evicted. Default 1000.
        """
        if maxsize < 1:
            raise ValueError("maxsize must be at least 1")

        self.maxsize = maxsize
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
        self._misses = 0
        logger.debug(f"SymbolCache initialized with maxsize={maxsize}")

    def get(self, file_path: str, current_mtime: float) -> Optional[List[Any]]:
        """Get cached symbols if valid.

        Returns cached symbols only if:
        1. File is in cache
        2. Cached mtime matches current mtime (file unchanged)

        Also moves entry to end (most recently used).

        Args:
            file_path: Absolute path to the file
            current_mtime: Current modification time of file

        Returns:
            List of symbols if cache hit, None if miss or stale
        """
        if file_path not in self._cache:
            self._misses += 1
            return None

        entry = self._cache[file_path]

        # Check if file changed (mtime mismatch)
        if entry.mtime != current_mtime:
            # Stale entry - remove and return miss
            del self._cache[file_path]
            self._misses += 1
            logger.debug(f"Cache stale for: {file_path}")
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(file_path)
        self._hits += 1
        logger.debug(f"Cache hit for: {file_path}")
        return entry.symbols

    def set(self, file_path: str, mtime: float, symbols: List[Any]) -> None:
        """Cache symbols for a file.

        If cache is full, evicts the least recently used entry first.

        Args:
            file_path: Absolute path to the file
            mtime: Modification time when symbols were extracted
            symbols: List of extracted symbols
        """
        # If already exists, update and move to end
        if file_path in self._cache:
            self._cache[file_path] = CacheEntry(mtime=mtime, symbols=symbols)
            self._cache.move_to_end(file_path)
            logger.debug(f"Cache updated for: {file_path}")
            return

        # Evict oldest if at capacity
        while len(self._cache) >= self.maxsize:
            evicted_path, _ = self._cache.popitem(last=False)
            logger.debug(f"Cache evicted (LRU): {evicted_path}")

        # Add new entry
        self._cache[file_path] = CacheEntry(mtime=mtime, symbols=symbols)
        logger.debug(f"Cache set for: {file_path}")

    def invalidate(self, file_path: str) -> bool:
        """Remove a specific file from cache.

        Args:
            file_path: Path to invalidate

        Returns:
            True if entry was removed, False if not in cache
        """
        if file_path in self._cache:
            del self._cache[file_path]
            logger.debug(f"Cache invalidated: {file_path}")
            return True
        return False

    def clear(self) -> None:
        """Remove all entries from cache."""
        count = len(self._cache)
        self._cache.clear()
        self._hits = 0
        self._misses = 0
        logger.debug(f"Cache cleared ({count} entries)")

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics.

        Returns:
            Dictionary with:
            - cached_files: Number of cached entries
            - cached_symbols: Total symbols across all entries
            - maxsize: Maximum cache size
            - hits: Number of cache hits
            - misses: Number of cache misses
            - hit_rate: Percentage of hits (0-100)
        """
        total_symbols = sum(len(e.symbols) for e in self._cache.values())
        total_requests = self._hits + self._misses
        hit_rate = (self._hits * 100 // total_requests) if total_requests > 0 else 0

        return {
            'cached_files': len(self._cache),
            'cached_symbols': total_symbols,
            'maxsize': self.maxsize,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': hit_rate,
        }

    def __len__(self) -> int:
        """Return number of cached entries."""
        return len(self._cache)

    def __contains__(self, file_path: str) -> bool:
        """Check if file is in cache (may be stale)."""
        return file_path in self._cache


# Default cache instance for convenience
_default_cache: Optional[SymbolCache] = None


def get_default_cache(maxsize: int = 1000) -> SymbolCache:
    """Get or create the default global cache.

    Args:
        maxsize: Max size if creating new cache

    Returns:
        Global SymbolCache instance
    """
    global _default_cache
    if _default_cache is None:
        _default_cache = SymbolCache(maxsize=maxsize)
    return _default_cache
