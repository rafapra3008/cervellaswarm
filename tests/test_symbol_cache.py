"""Tests for SymbolCache LRU implementation.

Tests the LRU cache behavior including:
- Basic get/set operations
- LRU eviction when maxsize exceeded
- mtime validation for cache hits
- Statistics tracking

Author: Cervella Tester (F1.1 Tech Debt Cleanup)
Date: 2026-02-02
"""

import pytest
import sys
import os

# Add scripts/utils to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts', 'utils'))

from symbol_cache import SymbolCache, CacheEntry


class TestSymbolCacheBasics:
    """Test basic cache operations."""

    def test_init_default_maxsize(self):
        """Cache initializes with default maxsize=1000."""
        cache = SymbolCache()
        assert cache.maxsize == 1000
        assert len(cache) == 0

    def test_init_custom_maxsize(self):
        """Cache accepts custom maxsize."""
        cache = SymbolCache(maxsize=50)
        assert cache.maxsize == 50

    def test_init_invalid_maxsize(self):
        """Cache rejects invalid maxsize."""
        with pytest.raises(ValueError):
            SymbolCache(maxsize=0)
        with pytest.raises(ValueError):
            SymbolCache(maxsize=-1)

    def test_set_and_get(self):
        """Basic set and get operations work."""
        cache = SymbolCache(maxsize=10)
        symbols = [{'name': 'foo'}, {'name': 'bar'}]

        cache.set('/path/to/file.py', 1234.0, symbols)
        result = cache.get('/path/to/file.py', 1234.0)

        assert result == symbols
        assert len(cache) == 1

    def test_get_nonexistent(self):
        """Get returns None for nonexistent entry."""
        cache = SymbolCache(maxsize=10)
        result = cache.get('/nonexistent.py', 1234.0)
        assert result is None

    def test_get_stale_mtime(self):
        """Get returns None when mtime changed."""
        cache = SymbolCache(maxsize=10)
        symbols = [{'name': 'foo'}]

        cache.set('/path/to/file.py', 1234.0, symbols)
        # File was modified (different mtime)
        result = cache.get('/path/to/file.py', 1235.0)

        assert result is None
        # Stale entry should be removed
        assert len(cache) == 0


class TestSymbolCacheLRU:
    """Test LRU eviction behavior."""

    def test_lru_eviction(self):
        """Oldest entry is evicted when maxsize exceeded."""
        cache = SymbolCache(maxsize=3)

        cache.set('/a.py', 1.0, [{'name': 'a'}])
        cache.set('/b.py', 2.0, [{'name': 'b'}])
        cache.set('/c.py', 3.0, [{'name': 'c'}])

        assert len(cache) == 3
        assert '/a.py' in cache

        # Add fourth entry - should evict /a.py (oldest)
        cache.set('/d.py', 4.0, [{'name': 'd'}])

        assert len(cache) == 3
        assert '/a.py' not in cache
        assert '/b.py' in cache
        assert '/c.py' in cache
        assert '/d.py' in cache

    def test_lru_access_updates_order(self):
        """Accessing entry moves it to end (most recently used)."""
        cache = SymbolCache(maxsize=3)

        cache.set('/a.py', 1.0, [{'name': 'a'}])
        cache.set('/b.py', 2.0, [{'name': 'b'}])
        cache.set('/c.py', 3.0, [{'name': 'c'}])

        # Access /a.py - should move it to end
        cache.get('/a.py', 1.0)

        # Add new entry - should evict /b.py (now oldest)
        cache.set('/d.py', 4.0, [{'name': 'd'}])

        assert '/a.py' in cache  # Was accessed, not evicted
        assert '/b.py' not in cache  # Now oldest, evicted
        assert '/c.py' in cache
        assert '/d.py' in cache

    def test_update_existing_entry(self):
        """Updating existing entry doesn't increase size."""
        cache = SymbolCache(maxsize=3)

        cache.set('/a.py', 1.0, [{'name': 'a'}])
        cache.set('/b.py', 2.0, [{'name': 'b'}])

        # Update /a.py with new symbols
        cache.set('/a.py', 1.5, [{'name': 'a_updated'}])

        assert len(cache) == 2
        result = cache.get('/a.py', 1.5)
        assert result == [{'name': 'a_updated'}]


class TestSymbolCacheStatistics:
    """Test statistics tracking."""

    def test_hit_tracking(self):
        """Cache tracks hits correctly."""
        cache = SymbolCache(maxsize=10)
        cache.set('/a.py', 1.0, [{'name': 'a'}])

        # Three hits
        cache.get('/a.py', 1.0)
        cache.get('/a.py', 1.0)
        cache.get('/a.py', 1.0)

        stats = cache.get_stats()
        assert stats['hits'] == 3
        assert stats['misses'] == 0
        assert stats['hit_rate'] == 100

    def test_miss_tracking(self):
        """Cache tracks misses correctly."""
        cache = SymbolCache(maxsize=10)

        # Three misses
        cache.get('/nonexistent1.py', 1.0)
        cache.get('/nonexistent2.py', 2.0)
        cache.get('/nonexistent3.py', 3.0)

        stats = cache.get_stats()
        assert stats['hits'] == 0
        assert stats['misses'] == 3
        assert stats['hit_rate'] == 0

    def test_mixed_stats(self):
        """Hit rate calculated correctly with mixed hits/misses."""
        cache = SymbolCache(maxsize=10)
        cache.set('/a.py', 1.0, [{'name': 'a'}])

        # 3 hits, 1 miss = 75% hit rate
        cache.get('/a.py', 1.0)
        cache.get('/a.py', 1.0)
        cache.get('/a.py', 1.0)
        cache.get('/nonexistent.py', 1.0)

        stats = cache.get_stats()
        assert stats['hits'] == 3
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 75


class TestSymbolCacheUtilities:
    """Test utility methods."""

    def test_invalidate(self):
        """Invalidate removes specific entry."""
        cache = SymbolCache(maxsize=10)
        cache.set('/a.py', 1.0, [{'name': 'a'}])
        cache.set('/b.py', 2.0, [{'name': 'b'}])

        result = cache.invalidate('/a.py')

        assert result is True
        assert '/a.py' not in cache
        assert '/b.py' in cache

    def test_invalidate_nonexistent(self):
        """Invalidate returns False for nonexistent entry."""
        cache = SymbolCache(maxsize=10)
        result = cache.invalidate('/nonexistent.py')
        assert result is False

    def test_clear(self):
        """Clear removes all entries and resets stats."""
        cache = SymbolCache(maxsize=10)
        cache.set('/a.py', 1.0, [{'name': 'a'}])
        cache.set('/b.py', 2.0, [{'name': 'b'}])
        cache.get('/a.py', 1.0)

        cache.clear()

        assert len(cache) == 0
        stats = cache.get_stats()
        assert stats['hits'] == 0
        assert stats['misses'] == 0

    def test_contains(self):
        """__contains__ works for checking membership."""
        cache = SymbolCache(maxsize=10)
        cache.set('/a.py', 1.0, [{'name': 'a'}])

        assert '/a.py' in cache
        assert '/b.py' not in cache


class TestSymbolCacheMemoryLimit:
    """Test that cache respects memory limits."""

    def test_large_dataset_respects_maxsize(self):
        """Adding many entries respects maxsize limit."""
        maxsize = 100
        cache = SymbolCache(maxsize=maxsize)

        # Add 200 entries
        for i in range(200):
            cache.set(f'/file{i}.py', float(i), [{'name': f'sym{i}'}])

        # Should never exceed maxsize
        assert len(cache) == maxsize

        # Most recent entries should be present
        assert '/file199.py' in cache
        assert '/file198.py' in cache

        # Oldest entries should be evicted
        assert '/file0.py' not in cache
        assert '/file99.py' not in cache
