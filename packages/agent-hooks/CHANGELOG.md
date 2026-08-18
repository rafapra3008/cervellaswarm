# Changelog

All notable changes to `cervellaswarm-agent-hooks` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-06-07

### Added

- **bash-validator: 4 security RISKY patterns** ported 1:1 from the internal
  source-of-truth hook (HOME v1.5.0, S519 P2.3 extension). All backward-compatible
  additions to `RISKY_PATTERNS` (ASK, not BLOCKED — a false-positive costs one
  confirm, never a hard block):
  - overwrite of `~/.zshrc` / `~/.bashrc` via redirect (shell config; check backup)
  - `curl`/`wget -o X.sh ... && bash X.sh` — download + *separate* shell exec
    (distinct from the already-blocked `curl ... | bash` pipe; some legit
    installers e.g. rustup/nvm — review the script first)
  - `sudo rm /etc/<file>` — removal of a critical system file
- **8 new tests** in `tests/test_bash_validator.py` (`TestRisky`): 4 ASK + 4
  anti-FP ALLOW (`cat ~/.zshrc`, `source ~/.bashrc`, `curl -o setup.sh ...` with
  no exec, `sudo rm /var/log/...`). Tests assert behaviour, never repeat the
  regex (lesson: bash_validator_regex_antipattern S519).

### Notes

- **Ported faithfully (parity with the internal moat), not micro-fixed:** the
  `>` redirect patterns also match `>>` (append) and `~/.zshrc.bak` (the `\b`
  sits at the `c`->`.` boundary) — known pre-existing false-positives carried
  over verbatim. Any fix belongs in HOME first, then re-ported.
- The `curl ... | bash` pipe was already shipped in 1.2.0 (BLOCKED); this
  release adds only the *download + separate exec* variant (RISKY).
- The Contabilita-specific `git merge`/`git rebase` scope-fix and the
  config-driven `_load_extra_patterns` extension are intentionally NOT in scope
  (two-tiers by design: project-specific / HOME-only).
- `bash_validator.py` `__version__` bumped to `1.3.0` to match `pyproject.toml`.

## [1.2.0] - 2026-06-05

### Added

- **bash-validator: 9 security BLOCKED patterns** ported 1:1 from the internal
  source-of-truth hook (HOME v1.5.0). All backward-compatible additions to
  `BLOCKED_PATTERNS` (no behaviour change for existing patterns):
  - `rm /*` glob-root (S526)
  - `rm $HOME` / `rm ${HOME}` (S526)
  - force push to `main`/`master` via `+refspec`, e.g. `git push origin +master`,
    `+main`, `+refs/heads/master`, `+HEAD:main` (S526)
  - SQL `DELETE FROM <table>` without a `WHERE` clause (S519)
  - overwrite of `~/.claude/settings.json` via redirect (config + secret leak
    risk, S517 scenario / S519)
  - overwrite of `~/.claude-insiders/settings.json` via redirect (S519)
  - `curl`/`wget ... | bash`/`sh`/`zsh` — arbitrary code injection (S519)
  - `git push origin`/`public --delete main`/`master` (S519)
  - `git push --mirror` — overwrites all remote branches incl. protected
    (dual-repo workflows must use a sync script, S519)
- **24 new tests** in `tests/test_bash_validator.py` (`TestBlocked`): 15 DENY + 9
  anti-FP ALLOW (76 baseline -> 100 total). Each of the 9 patterns has >=1 DENY +
  >=1 ALLOW; multi-variant patterns (`+refspec`, `$HOME`) add extra DENY cases (e.g. `rm -rf dist/*`,
  `$HOMEBREW_CACHE`, `git push origin +feature`, `DELETE FROM logs WHERE id=1`,
  `curl ... -o file.sh`, `git push origin --delete feature-x`). Tests assert
  behaviour, never repeat the regex (lesson: bash_validator_regex_antipattern S519).

### Notes

- **Two `rm` regex styles now coexist by design.** The 4 pre-existing `rm`
  patterns keep their original package style; the 2 newly ported `rm` patterns
  (`/*`, `$HOME`) use the richer HOME style (command-boundary prefix +
  multi-terminator) — more robust. The old ones were intentionally NOT
  re-harmonized (that would be an out-of-scope refactor).
- **Ported faithfully (parity with the internal moat), not micro-fixed:** the
  `DELETE FROM` regex anchors on end-of-string (`$`), so it matches a statement
  followed by a terminator (e.g. `DELETE FROM logs;`); a `settings.json.bak`
  append (`>>`) is a known pre-existing false-positive carried over verbatim.
  Both are deliberate parity choices, to be addressed (if ever) as separate
  changes.
- **Known version drift (out of scope):** `__init__.py` still reports the
  aggregate package `__version__ = "0.1.0"` (pre-existing drift, untouched).
  `bash_validator.py` `__version__` is bumped to `1.2.0` to match `pyproject.toml`
  (heals the module↔pyproject drift).
- The Contabilita-specific `git merge`/`git rebase` scope-fix from HOME is
  intentionally NOT ported: it is project-specific, while this package is generic.

## [1.1.0] - 2026-05-22

### Added
- `quality_validator.py` FASE 2: full implementation of 6 SNCP 5.1 metrics
  (density, recency scope-restricted, coverage 3 HARD + 2 WARN, actionability,
  anti-rot, self-sufficiency). Warning-only mode (mai blocco).
- `tests/test_quality_validator.py`: 18+ tests covering 6 metrics + 12 edge cases
  + boundary conditions.
- `cervella-quality-validator` CLI entry point (SessionEnd hook).
- Daily report generation `.sncp/reports/daily/sncp_quality_YYYY-MM-DD.md`.
- State A/B/C back-compat fallbacks: status header "Ultimo aggiornamento" for
  fresh_h2 fallback, legacy step pattern for actionability, configurable
  anti-rot threshold per state (A=0.20, C=0.80).

### Changed
- Module-level regex compilation (no ReDoS, no inner-loop recompile).
- Atomic write pattern (tempfile + os.rename POSIX) for daily report.

### Fixed
- N/A (FASE 2 = new functionality)

## [1.0.1-skeleton] - 2026-05-22

### Added
- `quality_validator.py` FASE 1 skeleton: 3-state detector (A/B/C), 6 metric
  stubs, atomic write report generation, env-var disable
  (`SNCP_QUALITY_VALIDATOR_DISABLE=1`).
- Config keys: density_min/max, recency_*, coverage_*, actionability_min,
  anti_rot_min_pct, self_sufficiency_lines, split_threshold_lines.

### Fixed
- Line count off-by-one (S519 D2 F5): `len(content.splitlines())` instead of
  `content.split("\n")` to avoid trailing-newline overcount.

## [0.1.0] - 2026-02-18

### Added

- **bash-validator**: PreToolUse hook that blocks destructive commands (rm -rf /, DROP TABLE, fork bombs), asks for confirmation on risky commands (git reset --hard, chmod 777), and auto-fixes `--force` to `--force-with-lease`. 15+ blocked patterns, 10 risky patterns, 19 safe rm targets. Zero dependencies.
- **git-reminder**: Stop hook that sends discreet desktop notifications about uncommitted files. 30-minute cooldown to avoid noise. Cross-platform: macOS (osascript) + Linux (notify-send).
- **file-limits**: SessionEnd hook that warns when files exceed configured line count or file count limits. Configurable via hooks.yaml.
- **context-inject**: SubagentStart hook that automatically injects project facts and session state into all subagents. Config-driven with sensible defaults.
- **session-checkpoint**: SessionEnd/PreCompact hook that auto-saves git status, recent commits, and branch info to a state file.
- **cervella-hooks CLI**: Setup command generates `.cervella/hooks.yaml` config and prints `settings.json` snippet for Claude Code.
- **YAML configuration**: All hooks configurable via `.cervella/hooks.yaml` (project) or `~/.claude/hooks.yaml` (user). Environment variable `CERVELLA_HOOKS_CONFIG` for explicit path.
- **227 tests**, 98% code coverage, runs in 0.12s.

[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/agent-hooks-v0.1.0
