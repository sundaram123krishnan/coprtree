# Coprtree CLI

The command line interface for [coprtree](https://github.com/sundaram123krishnan/coprtree/tree/master/coprtree) library.

## Requirements

```sh
sudo dnf install python3-dnf
```

Setup virtual environment

```sh
git clone https://github.com/sundaram123krishnan/coprtree
cd coprtree

uv venv --system-site-packages
```

## Usage

Resolve and print the build levels:

```sh
uv run coprtree-cli --project OWNER/PROJECT --provider pypi --package pyinfra \
    --chroot fedora-44-x86_64 --dry-run
```

Resolve and submit each level to Copr as a batch build:

```sh
uv run coprtree-cli --project OWNER/PROJECT --provider pypi --package pyinfra \
    --chroot fedora-44-x86_64
```

By default the latest version is built. Use `--package-version` to pick another,
and `coprtree-cli --help` for the full list of options.

NOTE: You need to configure copr in order to submit builds.\
Refer to: https://github.com/fedora-copr/copr/tree/main/cli/copr_cli#usage
