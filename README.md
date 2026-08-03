<p align="center"><a href="https://valkyrja.io" target="_blank">
    <img src="https://raw.githubusercontent.com/valkyrjaio/art/refs/heads/master/long-banner/orange/python.png" width="100%">
</a></p>

# Valkyrja Ruff

Shared Ruff configuration and the copyright header injector for Valkyrja Python
repositories.

Ruff enforces the copyright header through `CPY001`, and it reports a file that
does not match. It corrects nothing. Every other language in the organization has
a formatter that writes the header: PHP CS Fixer, Spotless, `goheader`, and the
ESLint rule all replace a wrong header. Python had no such tool, so a person added
each header by hand.

This package supplies that tool. `valkyrja-ruff-header` writes the header into
every Python file, and it replaces a header that names the wrong package.

The header text lives in this package and nowhere else. A repository supplies only
its own package identifier, which it already declares in
`.github/ci/copyright-header/config`. `COPYRIGHT_HEADER.md` in the `.github`
repository maps every repository to its identifier.

<p>
    <a href="https://pypi.org/project/valkyrja-ci-ruff/"><img src="https://img.shields.io/pypi/v/valkyrja-ci-ruff.svg" alt="Latest Version on PyPI"></a>
    <a href="https://pypi.org/project/valkyrja-ci-ruff/"><img src="https://img.shields.io/pypi/pyversions/valkyrja-ci-ruff.svg" alt="Supported Python Version"></a>
    <a href="https://github.com/valkyrjaio/ci-ruff-python/blob/26.x/LICENSE.md"><img src="https://img.shields.io/github/license/valkyrjaio/ci-ruff-python.svg" alt="License"></a>
    <a href="https://github.com/valkyrjaio/ci-ruff-python/actions/workflows/ci.yml?query=branch%3A26.x"><img src="https://github.com/valkyrjaio/ci-ruff-python/actions/workflows/ci.yml/badge.svg?branch=26.x" alt="CI Status"></a>
</p>

## Usage

### Write the header into every Python file

```bash
valkyrja-ruff-header
```

The command reads `src` and `tests` by default. Give it a path to read another
one. It reads the identifier from `.github/ci/copyright-header/config`, so the
repository declares its name once.

### Report a file that needs the header, and write nothing

```bash
valkyrja-ruff-header --check
```

The command reports a failure when a file needs the header, so a gate can run it.

### Options

| Option                | Effect                                                     |
| --------------------- | ---------------------------------------------------------- |
| `--check`             | report a file that needs the header, and write nothing     |
| `--identifier`        | name the package, instead of reading the repository config |
| `--root`              | name the repository root                                   |
| `--print-ruff-config` | print the Ruff `--config` override, and write nothing      |

### What the command does not touch

The command puts the header at the top of the file, below a shebang and below a
PEP 263 coding declaration. A shebang that moves off the first line stops working,
and a coding declaration that moves below the second line stops being read.

Warning: the command replaces a license header, and it replaces nothing else. A
tool that replaces the first comment block removes a comment that explains the
code, and the gate then passes because the file carries a correct header. This
command reads the leading comment block and requires every marker of a license
header in it. A file whose first comment explains the code keeps that comment, and
the header goes above it.

## What's Included

- **Full CI pipeline** — the same Ruff, mypy, Bandit, import-linter, and pytest
  configuration used across every Valkyrjaio Python repo, each isolated under
  `.github/ci/<tool>/` with its own `pyproject.toml` + `uv.lock`
- **uv configuration** — a root `pyproject.toml` whose `[tool.poe.tasks]` expose
  a shortcut for each CI tool, matching the org convention
- **Repository conventions** — aligned with
  [`REPOSITORY_NAMING.md`][repository naming url] and
  [`VOCABULARY.md`][vocabulary url]

## Running the CI Tools

Every tool is isolated under `.github/ci/<tool>/` with its own `pyproject.toml`
and `uv.lock`. Drive them through the root [poe][poe url] tasks — each runs the
tool from its isolated environment (`uv run --project …`) against the repo root:

```sh
uv run poe ci                # run the full CI gate
uv run poe ruff-format       # auto-format
uv run poe ruff              # lint
uv run poe mypy              # type-check
uv run poe import-linter     # architecture / import boundaries
uv run poe bandit            # security
uv run poe pytest-coverage   # tests + 100% coverage
```

## Versioning and Release Process

This package follows [semantic versioning][semantic versioning url] with a
major release every year, and support for each major version for 2 years
from the date of release.

For more information see our
[Versioning and Release Process documentation][Versioning and Release Process url].

### Supported Versions

Bug fixes are provided until 3 months after the next major release. Security
fixes are provided for 2 years after the initial release.

| Version | Python | Release        | Bug Fixes Until | Security Fixes Until |
| :------ | :----- | :------------- | :-------------- | :------------------- |
| 26      | 3.14+  | March 31, 2026 | Q2 2027         | Q1 2028              |

## Contributing

This package is an open-source, community-driven project. Improvements to
this package itself — refinements to the included CI configuration, uv
setup, or documentation — are welcome.

See [`CONTRIBUTING.md`][contributing url] for the submission process and
[`VOCABULARY.md`][vocabulary url] for the terminology used across Valkyrja.

## Security Issues

If you discover a security vulnerability, please follow our
[disclosure procedure][security vulnerabilities url].

## License

This package is open-source software licensed under the
[MIT license][MIT license url]. See [`LICENSE.md`](./LICENSE.md).

[Valkyrja url]: https://valkyrja.io
[uv url]: https://docs.astral.sh/uv/
[poe url]: https://poethepoet.natn.io/
[starter url]: https://github.com/valkyrjaio/valkyrja-starter-app-python
[repository naming url]: https://github.com/valkyrjaio/.github/blob/26.x/REPOSITORY_NAMING.md
[vocabulary url]: https://github.com/valkyrjaio/.github/blob/26.x/VOCABULARY.md
[contributing url]: https://github.com/valkyrjaio/.github/blob/26.x/CONTRIBUTING.md
[security vulnerabilities url]: https://github.com/valkyrjaio/.github/blob/26.x/SECURITY.md
[Versioning and Release Process url]: https://github.com/valkyrjaio/.github/blob/26.x/VERSIONING_AND_RELEASE_PROCESS.md
[semantic versioning url]: https://semver.org/
[MIT license url]: https://opensource.org/licenses/MIT
[license url]: ./LICENSE.md
