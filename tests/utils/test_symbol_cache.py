"""Tests for scripts/utils/symbol_cache.py.

Target: 90%+ coverage (currently 31%, 49/71 stmts missed).

Test Strategy:
- CacheEntry dataclass
- SymbolCache init (maxsize validation)
- get: hit, miss, stale (mtime), LRU move
- set: new, update, LRU eviction
- invalidate, clear
- get_stats: all fields, hit_rate edge cases
- __len__, __contains__
- get_default_cache: singleton pattern

Author: Cervella Tester
Date: 2026-02-10
"""

import pytest
from scripts.utils.symbol_cache import (
    CacheEntry,
    SymbolCache,
    get_default_cache,
    _default_cache
)


# ============================================================================
# CacheEntry Tests
# ============================================================================

class TestCacheEntry:
    """Test CacheEntry dataclass."""

    def test_cache_entry_creation(self):
        """Test CacheEntry initialization."""
        symbols = ['func1', 'func2']
        entry = CacheEntry(mtime=123.45, symbols=symbols)

        assert entry.mtime == 123.45
        assert entry.symbols == symbols

    def test_cache_entry_empty_symbols(self):
        """Test CacheEntry with empty symbols list."""
        entry = CacheEntry(mtime=100.0, symbols=[])

        assert entry.mtime == 100.0
        assert entry.symbols == []


# ============================================================================
# SymbolCache.__init__ Tests
# ============================================================================

class TestSymbolCacheInit:
    """Test SymbolCache initialization."""

    def test_init_default_maxsize(self):
        """Test default maxsize is 1000."""
        cache = SymbolCache()
        assert cache.maxsize == 1000
        assert len(cache) == 0

    def test_init_custom_maxsize(self):
        """Test custom maxsize."""
        cache = SymbolCache(maxsize=50)
        assert cache.maxsize == 50

    def test_init_maxsize_minimum(self):
        """Test maxsize=1 (minimum allowed)."""
        cache = SymbolCache(maxsize=1)
        assert cache.maxsize == 1

    def test_init_maxsize_zero_raises_error(self):
        """Test maxsize=0 raises ValueError."""
        with pytest.raises(ValueError, match="maxsize must be at least 1"):
            SymbolCache(maxsize=0)

    def test_init_maxsize_negative_raises_error(self):
        """Test negative maxsize raises ValueError."""
        with pytest.raises(ValueError, match="maxsize must be at least 1"):
            SymbolCache(maxsize=-1)


# ============================================================================
# SymbolCache.get Tests
# ============================================================================

class TestSymbolCacheGet:
    """Test SymbolCache.get method."""

    def test_get_miss_not_in_cache(self):
        """Test get returns None when file not in cache."""
        cache = SymbolCache(maxsize=10)
        result = cache.get("file.py", 100.0)

        assert result is None
        stats = cache.get_stats()
        assert stats['misses'] == 1
        assert stats['hits'] == 0

    def test_get_hit_valid_mtime(self):
        """Test get returns symbols when mtime matches."""
        cache = SymbolCache(maxsize=10)
        symbols = ['func1', 'func2']
        cache.set("file.py", 100.0, symbols)

        result = cache.get("file.py", 100.0)

        assert result == symbols
        stats = cache.get_stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 0

    def test_get_miss_stale_mtime(self):
        """Test get returns None when mtime changed (stale)."""
        cache = SymbolCache(maxsize=10)
        symbols = ['func1']
        cache.set("file.py", 100.0, symbols)

        # File changed (new mtime)
        result = cache.get("file.py", 200.0)

        assert result is None
        assert "file.py" not in cache  # Stale entry removed
        stats = cache.get_stats()
        assert stats['misses'] == 1

    def test_get_moves_to_end_lru(self):
        """Test get moves entry to end (most recently used)."""
        cache = SymbolCache(maxsize=3)
        cache.set("file1.py", 100.0, ['a'])
        cache.set("file2.py", 200.0, ['b'])
        cache.set("file3.py", 300.0, ['c'])

        # Access file1, should move to end
        cache.get("file1.py", 100.0)

        # Add file4, should evict file2 (oldest)
        cache.set("file4.py", 400.0, ['d'])

        assert "file1.py" in cache  # Accessed, kept
        assert "file2.py" not in cache  # Evicted (LRU)
        assert "file3.py" in cache
        assert "file4.py" in cache

    def test_get_multiple_hits(self):
        """Test multiple get hits increment counter."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])

        cache.get("file.py", 100.0)
        cache.get("file.py", 100.0)
        cache.get("file.py", 100.0)

        stats = cache.get_stats()
        assert stats['hits'] == 3
        assert stats['misses'] == 0


# ============================================================================
# SymbolCache.set Tests
# ============================================================================

class TestSymbolCacheSet:
    """Test SymbolCache.set method."""

    def test_set_new_entry(self):
        """Test set adds new entry."""
        cache = SymbolCache(maxsize=10)
        symbols = ['func1', 'func2']

        cache.set("file.py", 100.0, symbols)

        assert "file.py" in cache
        assert len(cache) == 1
        result = cache.get("file.py", 100.0)
        assert result == symbols

    def test_set_update_existing(self):
        """Test set updates existing entry."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['old'])

        # Update with new symbols
        cache.set("file.py", 200.0, ['new'])

        assert len(cache) == 1
        result = cache.get("file.py", 200.0)
        assert result == ['new']

    def test_set_update_moves_to_end(self):
        """Test set on existing entry moves it to end."""
        cache = SymbolCache(maxsize=3)
        cache.set("file1.py", 100.0, ['a'])
        cache.set("file2.py", 200.0, ['b'])
        cache.set("file3.py", 300.0, ['c'])

        # Update file1, should move to end
        cache.set("file1.py", 150.0, ['a_new'])

        # Add file4, should evict file2 (oldest)
        cache.set("file4.py", 400.0, ['d'])

        assert "file1.py" in cache  # Updated, kept
        assert "file2.py" not in cache  # Evicted
        assert "file3.py" in cache
        assert "file4.py" in cache

    def test_set_lru_eviction_at_maxsize(self):
        """Test LRU eviction when cache reaches maxsize."""
        cache = SymbolCache(maxsize=2)
        cache.set("file1.py", 100.0, ['a'])
        cache.set("file2.py", 200.0, ['b'])

        # Cache full, add file3 should evict file1
        cache.set("file3.py", 300.0, ['c'])

        assert "file1.py" not in cache  # Evicted (oldest)
        assert "file2.py" in cache
        assert "file3.py" in cache
        assert len(cache) == 2

    def test_set_lru_eviction_maxsize_one(self):
        """Test LRU eviction with maxsize=1."""
        cache = SymbolCache(maxsize=1)
        cache.set("file1.py", 100.0, ['a'])

        # Add file2, should evict file1
        cache.set("file2.py", 200.0, ['b'])

        assert "file1.py" not in cache
        assert "file2.py" in cache
        assert len(cache) == 1

    def test_set_empty_symbols(self):
        """Test set with empty symbols list."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, [])

        result = cache.get("file.py", 100.0)
        assert result == []


# ============================================================================
# SymbolCache.invalidate Tests
# ============================================================================

class TestSymbolCacheInvalidate:
    """Test SymbolCache.invalidate method."""

    def test_invalidate_existing_entry(self):
        """Test invalidate removes existing entry."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])

        result = cache.invalidate("file.py")

        assert result is True
        assert "file.py" not in cache
        assert len(cache) == 0

    def test_invalidate_non_existing_entry(self):
        """Test invalidate returns False for non-existing entry."""
        cache = SymbolCache(maxsize=10)

        result = cache.invalidate("file.py")

        assert result is False

    def test_invalidate_multiple_entries(self):
        """Test invalidate with multiple entries."""
        cache = SymbolCache(maxsize=10)
        cache.set("file1.py", 100.0, ['a'])
        cache.set("file2.py", 200.0, ['b'])
        cache.set("file3.py", 300.0, ['c'])

        cache.invalidate("file2.py")

        assert "file1.py" in cache
        assert "file2.py" not in cache
        assert "file3.py" in cache
        assert len(cache) == 2


# ============================================================================
# SymbolCache.clear Tests
# ============================================================================

class TestSymbolCacheClear:
    """Test SymbolCache.clear method."""

    def test_clear_empty_cache(self):
        """Test clear on empty cache."""
        cache = SymbolCache(maxsize=10)
        cache.clear()

        assert len(cache) == 0
        stats = cache.get_stats()
        assert stats['cached_files'] == 0

    def test_clear_removes_all_entries(self):
        """Test clear removes all entries."""
        cache = SymbolCache(maxsize=10)
        cache.set("file1.py", 100.0, ['a'])
        cache.set("file2.py", 200.0, ['b'])
        cache.set("file3.py", 300.0, ['c'])

        cache.clear()

        assert len(cache) == 0
        assert "file1.py" not in cache
        assert "file2.py" not in cache
        assert "file3.py" not in cache

    def test_clear_resets_stats(self):
        """Test clear resets hits/misses stats."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])
        cache.get("file.py", 100.0)  # Hit
        cache.get("other.py", 100.0)  # Miss

        cache.clear()

        stats = cache.get_stats()
        assert stats['hits'] == 0
        assert stats['misses'] == 0
        assert stats['cached_files'] == 0


# ============================================================================
# SymbolCache.get_stats Tests
# ============================================================================

class TestSymbolCacheGetStats:
    """Test SymbolCache.get_stats method."""

    def test_get_stats_empty_cache(self):
        """Test get_stats on empty cache."""
        cache = SymbolCache(maxsize=10)
        stats = cache.get_stats()

        assert stats['cached_files'] == 0
        assert stats['cached_symbols'] == 0
        assert stats['maxsize'] == 10
        assert stats['hits'] == 0
        assert stats['misses'] == 0
        assert stats['hit_rate'] == 0

    def test_get_stats_with_entries(self):
        """Test get_stats with multiple entries."""
        cache = SymbolCache(maxsize=10)
        cache.set("file1.py", 100.0, ['a', 'b'])  # 2 symbols
        cache.set("file2.py", 200.0, ['c'])  # 1 symbol
        cache.set("file3.py", 300.0, ['d', 'e', 'f'])  # 3 symbols

        stats = cache.get_stats()

        assert stats['cached_files'] == 3
        assert stats['cached_symbols'] == 6  # 2+1+3
        assert stats['maxsize'] == 10

    def test_get_stats_hit_rate_calculation(self):
        """Test get_stats hit_rate calculation."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])

        # 3 hits, 2 misses = 60% hit rate
        cache.get("file.py", 100.0)  # Hit
        cache.get("file.py", 100.0)  # Hit
        cache.get("file.py", 100.0)  # Hit
        cache.get("other1.py", 100.0)  # Miss
        cache.get("other2.py", 100.0)  # Miss

        stats = cache.get_stats()
        assert stats['hits'] == 3
        assert stats['misses'] == 2
        assert stats['hit_rate'] == 60  # 3 / 5 * 100 = 60

    def test_get_stats_hit_rate_zero_requests(self):
        """Test get_stats hit_rate with zero requests (division by zero)."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])

        stats = cache.get_stats()

        assert stats['hits'] == 0
        assert stats['misses'] == 0
        assert stats['hit_rate'] == 0  # No division by zero error

    def test_get_stats_hit_rate_all_hits(self):
        """Test get_stats hit_rate with 100% hits."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])

        cache.get("file.py", 100.0)  # Hit
        cache.get("file.py", 100.0)  # Hit

        stats = cache.get_stats()
        assert stats['hit_rate'] == 100

    def test_get_stats_hit_rate_all_misses(self):
        """Test get_stats hit_rate with 0% hits."""
        cache = SymbolCache(maxsize=10)

        cache.get("file1.py", 100.0)  # Miss
        cache.get("file2.py", 100.0)  # Miss

        stats = cache.get_stats()
        assert stats['hit_rate'] == 0


# ============================================================================
# SymbolCache.__len__ and __contains__ Tests
# ============================================================================

class TestSymbolCacheDunderMethods:
    """Test SymbolCache __len__ and __contains__ methods."""

    def test_len_empty_cache(self):
        """Test __len__ on empty cache."""
        cache = SymbolCache(maxsize=10)
        assert len(cache) == 0

    def test_len_with_entries(self):
        """Test __len__ with multiple entries."""
        cache = SymbolCache(maxsize=10)
        cache.set("file1.py", 100.0, ['a'])
        cache.set("file2.py", 200.0, ['b'])
        cache.set("file3.py", 300.0, ['c'])

        assert len(cache) == 3

    def test_len_after_eviction(self):
        """Test __len__ after LRU eviction."""
        cache = SymbolCache(maxsize=2)
        cache.set("file1.py", 100.0, ['a'])
        cache.set("file2.py", 200.0, ['b'])
        cache.set("file3.py", 300.0, ['c'])  # Evicts file1

        assert len(cache) == 2

    def test_contains_existing_entry(self):
        """Test __contains__ returns True for existing entry."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])

        assert "file.py" in cache

    def test_contains_non_existing_entry(self):
        """Test __contains__ returns False for non-existing entry."""
        cache = SymbolCache(maxsize=10)

        assert "file.py" not in cache

    def test_contains_after_invalidate(self):
        """Test __contains__ after invalidation."""
        cache = SymbolCache(maxsize=10)
        cache.set("file.py", 100.0, ['func'])
        cache.invalidate("file.py")

        assert "file.py" not in cache


# ============================================================================
# get_default_cache Tests
# ============================================================================

class TestGetDefaultCache:
    """Test get_default_cache singleton pattern."""

    def test_get_default_cache_creates_instance(self):
        """Test get_default_cache creates cache instance."""
        # Clear global cache first
        import scripts.utils.symbol_cache as cache_module
        cache_module._default_cache = None

        cache = get_default_cache(maxsize=100)

        assert cache is not None
        assert isinstance(cache, SymbolCache)
        assert cache.maxsize == 100

    def test_get_default_cache_singleton_same_instance(self):
        """Test get_default_cache returns same instance (singleton)."""
        import scripts.utils.symbol_cache as cache_module
        cache_module._default_cache = None

        cache1 = get_default_cache(maxsize=100)
        cache2 = get_default_cache(maxsize=200)  # maxsize ignored

        assert cache1 is cache2
        assert cache1.maxsize == 100  # First maxsize used

    def test_get_default_cache_persists_data(self):
        """Test get_default_cache persists data across calls."""
        import scripts.utils.symbol_cache as cache_module
        cache_module._default_cache = None

        cache1 = get_default_cache()
        cache1.set("file.py", 100.0, ['func'])

        cache2 = get_default_cache()
        result = cache2.get("file.py", 100.0)

        assert result == ['func']
