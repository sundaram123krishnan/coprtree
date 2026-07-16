# CoprTree

[![PyPI](https://img.shields.io/pypi/v/coprtree)](https://pypi.org/project/coprtree/)
[![Tests](https://github.com/sundaram123krishnan/coprtree/actions/workflows/tests.yml/badge.svg)](https://github.com/sundaram123krishnan/coprtree/actions/workflows/tests.yml)
[![Lint](https://github.com/sundaram123krishnan/coprtree/actions/workflows/python-diff-lint.yml/badge.svg)](https://github.com/sundaram123krishnan/coprtree/actions/workflows/python-diff-lint.yml)
[![codecov](https://codecov.io/gh/sundaram123krishnan/coprtree/branch/master/graph/badge.svg)](https://codecov.io/gh/sundaram123krishnan/coprtree)


Coprtree resolves a package's transitive dependency graph, prunes anything the target distribution or your Copr project already provides, and topologically sorts the rest into parallel build levels

This is a monorepo based setup which contains:

- [coprtree](coprtree/) - Dependencies resolution library
- [coprtree-cli](coprtree-cli/) - A standalone CLI

Installation and usage live in each package's README.

## Supported package managers

- [x] PyPI 
- [x] CPAN 
- [ ] RubyGems
- [ ] npm


## Supported distributions

- [x] Fedora
- [ ] CentOS Stream
- [ ] RHEL
- [ ] EPEL
- [ ] AlmaLinux
- [ ] Amazon Linux
- [ ] Azure Linux
- [ ] openSUSE
- [ ] Mageia
- [ ] openEuler

## Acknowledgments

- Dependency metadata is powered by the excellent [ecosyste.ms](https://github.com/ecosyste-ms/).
- Huge thanks to [@frostyx](https://github.com/frostyx) for continuous support and guidance.
