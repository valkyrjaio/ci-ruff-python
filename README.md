<p align="center"><a href="https://valkyrja.io" target="_blank">
    <img src="https://raw.githubusercontent.com/valkyrjaio/art/refs/heads/master/long-banner/orange/python.png" width="100%">
</a></p>

# Project Template (Python)

A starter template for creating new Python repositories in the Valkyrjaio
organization.

This template ships with the full Valkyrja CI pipeline pre-wired (Ruff, mypy,
Bandit, import-linter, pytest), a minimal [uv][uv url] setup, and the
repository conventions used across the rest of the org. Use it as the starting
point for any new Python package, CI tool config, or integration repo — not for
end-user applications built on the Valkyrja framework (use
[`valkyrja-starter-app-python`][starter url] for that).

<p>
    <a href="https://pypi.org/project/valkyrja-template/"><img src="https://img.shields.io/pypi/v/valkyrja-template.svg" alt="Latest Version on PyPI"></a>
    <a href="https://pypi.org/project/valkyrja-template/"><img src="https://img.shields.io/pypi/pyversions/valkyrja-template.svg" alt="Supported Python Version"></a>
    <a href="https://github.com/valkyrjaio/project-template-python/blob/26.x/LICENSE.md"><img src="https://img.shields.io/github/license/valkyrjaio/project-template-python.svg" alt="License"></a>
    <a href="https://github.com/valkyrjaio/project-template-python/actions/workflows/ci.yml?query=branch%3A26.x"><img src="https://github.com/valkyrjaio/project-template-python/actions/workflows/ci.yml/badge.svg?branch=26.x" alt="CI Status"></a>
</p>

## Usage

### Use this template _(recommended)_

This repository is a GitHub template. Click the **Use this template** button
at the top of the repo to create a new repository in the Valkyrjaio
organization, pre-populated with the template's structure and CI.

### After Creating Your Repo

1. Update `pyproject.toml` with your package's name, description, and metadata
2. Rename `src/valkyrja/template/` to your component's package and replace its
   contents with your source code
3. Update this `README.md` to describe the new package
4. Configure the required secrets and variables — see
   [`REPOSITORY_NAMING.md`][repository naming url] for naming guidance and
   `.github`'s workflow documentation for secret requirements
5. Verify CI passes on the first commit

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

This template follows [semantic versioning][semantic versioning url] with a
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

This template is an open-source, community-driven project. Improvements to
the template itself — refinements to the included CI configuration, uv
setup, or documentation — are welcome.

See [`CONTRIBUTING.md`][contributing url] for the submission process and
[`VOCABULARY.md`][vocabulary url] for the terminology used across Valkyrja.

## Security Issues

If you discover a security vulnerability, please follow our
[disclosure procedure][security vulnerabilities url].

## License

This template is open-source software licensed under the
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
