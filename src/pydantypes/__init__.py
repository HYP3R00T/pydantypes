"""pydantypes — The missing types for Pydantic."""

try:
    from pydantypes._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
