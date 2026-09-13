class CoprtreeError(Exception):
    """Base class for all coprtree errors."""


class UnsupportedProvider(CoprtreeError):
    """The requested ecosystem/registry has no Provider registered."""


class UnsupportedDistribution(CoprtreeError):
    """The chroot's distribution is not registered (or is malformed)."""


class InvalidCoprProject(CoprtreeError):
    """The copr project isn't in 'OWNER/PROJECT' form."""


class MetadataNotFound(CoprtreeError):
    """ecosyste.ms has no fetchable package for a dependency name."""


class CircularDependency(CoprtreeError):
    """The dependency graph has a cycle, so it can't be topologically sorted."""
