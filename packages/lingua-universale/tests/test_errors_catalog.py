# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for errors.py catalog completeness and integrity.

Covers: all codes have all 3 locales, MappingProxyType immutability,
no duplicate codes, regex format LU-X###, non-empty strings, fallback
LU-X001 exists, category lookup covers all prefixes.
"""

from __future__ import annotations

import re
from types import MappingProxyType

import pytest

# Access the internal catalog via the module directly.
import cervellaswarm_lingua_universale.errors as _errors_mod
from cervellaswarm_lingua_universale.errors import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    ErrorCategory,
)


# ============================================================
# Catalog access helper
# ============================================================


def _get_catalog() -> MappingProxyType:
    """Return the internal _CATALOG."""
    return _errors_mod._CATALOG


def _get_code_category() -> MappingProxyType:
    """Return the internal _CODE_CATEGORY."""
    return _errors_mod._CODE_CATEGORY


# ============================================================
# Basic structure
# ============================================================


class TestCatalogStructure:
    """_CATALOG is a non-empty MappingProxyType."""

    def test_catalog_is_mapping_proxy(self):
        cat = _get_catalog()
        assert isinstance(cat, MappingProxyType)

    def test_catalog_not_empty(self):
        cat = _get_catalog()
        assert len(cat) > 0

    def test_catalog_immutable(self):
        cat = _get_catalog()
        with pytest.raises(TypeError):
            cat["LU-NEW"] = {}  # type: ignore[index]

    def test_catalog_inner_entries_are_mapping_proxy(self):
        cat = _get_catalog()
        for code, entry in cat.items():
            assert isinstance(entry, MappingProxyType), f"{code} entry is not MappingProxyType"


# ============================================================
# Code format
# ============================================================

_CODE_PATTERN = re.compile(r"^LU-[A-Z]\d{3}$")


class TestCatalogCodeFormat:
    """Every catalog code follows the LU-X### pattern."""

    def test_all_codes_match_pattern(self):
        cat = _get_catalog()
        bad = [c for c in cat if not _CODE_PATTERN.match(c)]
        assert bad == [], f"Codes with wrong format: {bad}"

    def test_no_duplicate_codes(self):
        cat = _get_catalog()
        codes = list(cat.keys())
        assert len(codes) == len(set(codes)), "Duplicate codes detected"


# ============================================================
# Locale completeness
# ============================================================


class TestCatalogLocaleCompleteness:
    """Every code has entries for all 3 supported locales."""

    def test_all_codes_have_en(self):
        cat = _get_catalog()
        missing = [c for c, e in cat.items() if "en" not in e]
        assert missing == [], f"Missing 'en' locale: {missing}"

    def test_all_codes_have_it(self):
        cat = _get_catalog()
        missing = [c for c, e in cat.items() if "it" not in e]
        assert missing == [], f"Missing 'it' locale: {missing}"

    def test_all_codes_have_pt(self):
        cat = _get_catalog()
        missing = [c for c, e in cat.items() if "pt" not in e]
        assert missing == [], f"Missing 'pt' locale: {missing}"


# ============================================================
# Message and suggestion non-empty
# ============================================================


class TestCatalogContentNonEmpty:
    """Every message template and suggestion template is a non-empty string."""

    def test_all_messages_non_empty(self):
        cat = _get_catalog()
        for code, entry in cat.items():
            for locale in SUPPORTED_LOCALES:
                if locale in entry:
                    msg, _ = entry[locale]
                    assert isinstance(msg, str), f"{code}/{locale} message is not str"
                    assert len(msg.strip()) > 0, f"{code}/{locale} message is empty"

    def test_all_suggestions_non_empty(self):
        cat = _get_catalog()
        for code, entry in cat.items():
            for locale in SUPPORTED_LOCALES:
                if locale in entry:
                    _, sug = entry[locale]
                    assert isinstance(sug, str), f"{code}/{locale} suggestion is not str"
                    assert len(sug.strip()) > 0, f"{code}/{locale} suggestion is empty"

    def test_locale_entries_are_tuples_of_two_strings(self):
        cat = _get_catalog()
        for code, entry in cat.items():
            for locale in SUPPORTED_LOCALES:
                if locale in entry:
                    pair = entry[locale]
                    assert isinstance(pair, tuple), f"{code}/{locale} entry is not tuple"
                    assert len(pair) == 2, f"{code}/{locale} tuple has {len(pair)} elements"


# ============================================================
# Required codes exist
# ============================================================


class TestCatalogRequiredCodes:
    """Key codes referenced in the humanize() logic must exist."""

    @pytest.mark.parametrize("code", [
        "LU-T001", "LU-T002", "LU-T003", "LU-T004", "LU-T005",
        "LU-T006", "LU-T007", "LU-T008", "LU-T009", "LU-T010",
    ])
    def test_type_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-P001", "LU-P002", "LU-P003", "LU-P004", "LU-P005",
    ])
    def test_protocol_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-R001", "LU-R002", "LU-R003", "LU-R004",
        "LU-R005", "LU-R006", "LU-R007",
    ])
    def test_checker_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-D001", "LU-D002", "LU-D003", "LU-D004",
        "LU-D005", "LU-D006", "LU-D007",
    ])
    def test_dsl_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-S001", "LU-S002", "LU-S003", "LU-S004",
        "LU-S005", "LU-S006", "LU-S007", "LU-S008",
    ])
    def test_spec_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-I001", "LU-I002", "LU-I003", "LU-I004", "LU-I005",
    ])
    def test_intent_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-L001", "LU-L002", "LU-L003", "LU-L004", "LU-L005", "LU-L006",
    ])
    def test_lean4_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-G001", "LU-G002", "LU-G003",
    ])
    def test_codegen_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-C001", "LU-C002", "LU-C003", "LU-C004", "LU-C005",
    ])
    def test_confidence_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    @pytest.mark.parametrize("code", [
        "LU-A001", "LU-A002", "LU-A003",
    ])
    def test_integration_codes_exist(self, code):
        assert code in _get_catalog(), f"{code} missing from catalog"

    def test_fallback_lu_x001_exists(self):
        assert "LU-X001" in _get_catalog()


# ============================================================
# Category lookup (_CODE_CATEGORY)
# ============================================================


class TestCodeCategoryLookup:
    """_CODE_CATEGORY covers all expected prefixes."""

    def test_is_mapping_proxy(self):
        cc = _get_code_category()
        assert isinstance(cc, MappingProxyType)

    def test_is_immutable(self):
        cc = _get_code_category()
        with pytest.raises(TypeError):
            cc["LU-Z"] = ErrorCategory.VALIDATION  # type: ignore[index]

    @pytest.mark.parametrize("prefix,expected_category", [
        ("LU-T", ErrorCategory.VALIDATION),
        ("LU-P", ErrorCategory.VALIDATION),
        ("LU-R", ErrorCategory.PROTOCOL),
        ("LU-D", ErrorCategory.PARSE),
        ("LU-S", ErrorCategory.PARSE),
        ("LU-I", ErrorCategory.PARSE),
        ("LU-L", ErrorCategory.VERIFICATION),
        ("LU-G", ErrorCategory.CODEGEN),
        ("LU-C", ErrorCategory.CONFIDENCE),
        ("LU-A", ErrorCategory.INTEGRATION),
        ("LU-X", ErrorCategory.VALIDATION),
    ])
    def test_prefix_maps_to_category(self, prefix, expected_category):
        cc = _get_code_category()
        assert cc[prefix] == expected_category, (
            f"{prefix} should map to {expected_category}, got {cc.get(prefix)}"
        )

    def test_category_for_code_function(self):
        """_category_for_code() is consistent with _CODE_CATEGORY."""
        cat_fn = _errors_mod._category_for_code
        assert cat_fn("LU-T001") == ErrorCategory.VALIDATION
        assert cat_fn("LU-R007") == ErrorCategory.PROTOCOL
        assert cat_fn("LU-D003") == ErrorCategory.PARSE
        assert cat_fn("LU-L001") == ErrorCategory.VERIFICATION
        assert cat_fn("LU-G001") == ErrorCategory.CODEGEN
        assert cat_fn("LU-C001") == ErrorCategory.CONFIDENCE
        assert cat_fn("LU-A001") == ErrorCategory.INTEGRATION
        assert cat_fn("LU-X001") == ErrorCategory.VALIDATION

    def test_unknown_prefix_defaults_to_validation(self):
        cat_fn = _errors_mod._category_for_code
        result = cat_fn("LU-Z999")
        assert result == ErrorCategory.VALIDATION


# ============================================================
# _VALUE_ERROR_MATCHERS integrity
# ============================================================


class TestValueErrorMatchers:
    """_VALUE_ERROR_MATCHERS references only valid catalog codes."""

    def test_all_matcher_codes_in_catalog(self):
        matchers = _errors_mod._VALUE_ERROR_MATCHERS
        cat = _get_catalog()
        bad = [(substring, code) for substring, code in matchers if code not in cat]
        assert bad == [], f"Matcher codes not in catalog: {bad}"

    def test_matchers_is_tuple(self):
        assert isinstance(_errors_mod._VALUE_ERROR_MATCHERS, tuple)

    def test_matchers_not_empty(self):
        assert len(_errors_mod._VALUE_ERROR_MATCHERS) > 0

    def test_each_matcher_entry_is_pair(self):
        for entry in _errors_mod._VALUE_ERROR_MATCHERS:
            assert len(entry) == 2, f"Matcher entry {entry!r} is not a pair"
            assert isinstance(entry[0], str)
            assert isinstance(entry[1], str)
