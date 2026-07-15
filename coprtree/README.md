# Coprtree

The resolver library

## Requirements

```sh
sudo dnf install python3-dnf
```


Setup virtual environment

```sh
uv venv --system-site-packages
```

## Usage

```python
from coprtree.coprtree import resolve_dependencies
from coprtree.models import BuildTarget, BuildEnv

levels = resolve_dependencies(
    BuildTarget(provider="pypi.org", name="pydantic-ai"),
    BuildEnv(chroot="fedora-44-x86_64", copr_project="OWNER/PROJECT"),
)
```

`provider` is an [ecosyste.ms](https://packages.ecosyste.ms) registry id: `pypi.org` or `metacpan.org`.

Packages within a level do not depend on each other and can be built in parallel, and every level depends only on the ones before it. 
