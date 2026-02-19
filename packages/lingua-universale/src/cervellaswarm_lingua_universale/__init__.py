"""CervellaSwarm Lingua Universale - Session types for AI agent protocols."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cervellaswarm-lingua-universale")
except PackageNotFoundError:
    __version__ = "0.1.0"
