# CoprTree

[![Tests](https://github.com/sundaram123krishnan/coprtree/actions/workflows/tests.yml/badge.svg)](https://github.com/sundaram123krishnan/coprtree/actions/workflows/tests.yml)
[![Lint](https://github.com/sundaram123krishnan/coprtree/actions/workflows/python-diff-lint.yml/badge.svg)](https://github.com/sundaram123krishnan/coprtree/actions/workflows/python-diff-lint.yml)
[![codecov](https://codecov.io/gh/sundaram123krishnan/coprtree/branch/master/graph/badge.svg)](https://codecov.io/gh/sundaram123krishnan/coprtree)


Coprtree resolves a package's transitive dependency graph, prunes anything the target distribution or your Copr project already provides, and topologically sorts the rest into parallel build levels

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

## Usage

```sh
sudo dnf install python3-dnf

git clone https://github.com/sundaram123krishnan/coprtree
cd coprtree

uv venv --system-site-packages
uv sync
```

```sh
uv run coprtree --help
```

Resolve and print the build levels (no copr config required):

```sh
uv run coprtree --project OWNERNAME/PROJECTNAME --provider pypi --package pyinfra \
    --chroot fedora-44-x86_64 --dry-run
```

Resolve and submit the builds to Copr:
```sh
uv run --extra cli coprtree --project OWNERNAME/PROJECTNAME --provider pypi \
    --package pyinfra --chroot fedora-44-x86_64
```

NOTE: You need to configure copr in order to submit builds.\
Refer to: https://github.com/fedora-copr/copr/tree/main/cli/copr_cli#usage

## Acknowledgments

- Dependency metadata is powered by the excellent [ecosyste.ms](https://github.com/ecosyste-ms/).
- Huge thanks to [@frostyx](https://github.com/frostyx) for continuous support and guidance.
