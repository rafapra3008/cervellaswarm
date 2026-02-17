# CervellaSwarm Code Review Standards

> This file guides automated Claude reviews on pull requests.

---

## Code Standards

### Python
- Max 500 lines per file
- Max 50 lines per function
- snake_case for functions and variables
- PascalCase for classes
- Docstrings for public functions

### JavaScript/TypeScript
- Max 500 lines per file
- camelCase for functions and variables
- PascalCase for components
- TypeScript types or PropTypes for props

### Markdown
- Max 1000 lines per file
- Hierarchical headings
- Working links

---

## Security Checklist

- [ ] No hardcoded secrets or passwords
- [ ] All input validated
- [ ] SQL queries parameterized
- [ ] HTML output sanitized
- [ ] HTTPS for external calls
- [ ] Minimum necessary permissions

---

## Quality Checklist

- [ ] Public functions have docstrings/JSDoc
- [ ] Tests for new features
- [ ] No TODOs without linked issue
- [ ] Specific error handling (no catch-all)
- [ ] Appropriate logging

---

## When to Block a PR

1. **Security issues** - Any vulnerability
2. **Breaking changes** - Without documentation
3. **No tests** - For critical logic
4. **Hardcoded secrets** - Never acceptable

---

## Review Tone

- Professional but friendly
- Suggest, don't impose
- Provide code examples
- Acknowledge things done well

*Quality is not negotiable.*
