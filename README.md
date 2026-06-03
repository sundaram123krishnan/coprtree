
### Coprtree

This project is in an experimental phase. The goal for the first release is to compute the dependency graph for a given package (only pypi.org is supported for now) and produce a pruned graph that reports which dependencies are missing from the Fedora and Copr repositories.

The graph is topologically sorted to support batch builds, so that packages without inter-dependencies can be built in parallel.

### Usage

In `main.py`, update the `Coprtree(...)` call:
- `BuildTarget(provider="pypi.org", name="enter-any-package-name-here")`
- `copr_project`
- `chroot` 

```shell
uv run main.py
```
NOTE: 
- Supports only Fedora distributions; install `python3-dnf`.
- Copr project should be named as `python-{package-name}` for testing.


Using https://ecosyste.ms/ API for querying dependencies for each package.

### Future Plans

- Support additional providers (rubygems, npm, ...)
- Integrate with `copr-cli`


