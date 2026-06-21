class CoprtreeError(Exception):
    """Base class for all coprtree errors."""


class UnsupportedProvider(CoprtreeError):
    """The requested ecosystem/registry has no Provider registered."""


class MetadataNotFound(CoprtreeError):
    """ecosyste.ms has no fetchable package for a dependency name."""


class CircularDependency(CoprtreeError):
    """The dependency graph has a cycle, so it can't be topologically sorted."""
