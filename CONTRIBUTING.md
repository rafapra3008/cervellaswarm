# Contributing to CervellaSwarm

Thank you for your interest in contributing to CervellaSwarm!

## License

By contributing to CervellaSwarm, you agree that your contributions will be licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) for the full license text.

## Developer Certificate of Origin (DCO)

We use the DCO instead of a CLA. This means you certify that:

1. You wrote the contribution, OR
2. You have the right to submit it under the Apache 2.0 license

### How to Sign Off

Add a sign-off line to your commits:

```bash
git commit -s -m "Your commit message"
```

This adds:
```
Signed-off-by: Your Name <your.email@example.com>
```

### The DCO Text

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

## Good First Issues

Looking for a place to start? These are beginner-friendly:

1. **Add shell completion for bash/zsh/fish** -- Generate completion scripts for `lu` CLI subcommands.
2. **Write a new stdlib protocol** -- Add a verified `.lu` protocol to `stdlib/` (e.g., WebSocket handshake, OAuth flow). Must pass `lu lint` + `lu fmt --check`.
3. **Improve an error message** -- Find a confusing error in `_errors.py` (74 error codes) and make it friendlier. Inspiration: Elm and Rust compilers.
4. **Add a benchmark script** -- Measure parse/compile/verify time for all 20 stdlib protocols.
5. **Translate `lu chat`** -- Add Spanish, French, or German locale strings to `_intent_bridge.py`.

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests: `pytest packages/lingua-universale/tests/ -x` (all 3867 must pass)
5. Lint `.lu` files: `lu fmt --check` and `lu lint`
6. Sign off your commits (`git commit -s -m "Add amazing feature"`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Code Style

- Pure Python standard library -- zero external dependencies in the core package
- Keep it simple and readable
- Follow existing patterns in the codebase
- Add comments only where logic isn't self-evident

## Quick Links

- [Playground](https://rafapra3008.github.io/cervellaswarm/) -- Try LU in your browser
- [Interactive Tour](https://rafapra3008.github.io/cervellaswarm/?tour) -- Learn LU in 10 minutes
- [Protocol Zoo](https://rafapra3008.github.io/cervellaswarm/zoo.html) -- 20 verified protocol examples
- [PyPI](https://pypi.org/project/cervellaswarm-lingua-universale/) -- `pip install cervellaswarm-lingua-universale`

## Questions?

Open an issue on [GitHub Issues](https://github.com/rafapra3008/CervellaSwarm/issues).

---

*"Fatto BENE > Fatto VELOCE"*
