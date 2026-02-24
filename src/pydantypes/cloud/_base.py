"""Base class for cloud storage URI types."""

from __future__ import annotations

from pathlib import PurePosixPath


class CloudStorageUri(str):
    """Base for cloud storage URI types with unified bucket/key and path helpers.

    Subclasses must set ``bucket`` and ``key`` as instance attributes in
    ``__new__``.  All path helper properties delegate to
    :class:`~pathlib.PurePosixPath` operating on ``self.key``.
    """

    bucket: str
    key: str

    # -- Core path helpers ---------------------------------------------------

    @property
    def name(self) -> str:
        """Filename component of the key (e.g. ``'file.csv'``)."""
        return PurePosixPath(self.key).name if self.key else ""

    @property
    def suffix(self) -> str:
        """Last file extension of the key (e.g. ``'.csv'``)."""
        return PurePosixPath(self.key).suffix if self.key else ""

    @property
    def stem(self) -> str:
        """Filename without the last extension (e.g. ``'file'``)."""
        return PurePosixPath(self.key).stem if self.key else ""

    @property
    def parent_key(self) -> str:
        """Parent directory of the key (e.g. ``'path/to'``).

        Returns an empty string when the key has no parent component.
        """
        if not self.key:
            return ""
        p = str(PurePosixPath(self.key).parent)
        return "" if p == "." else p

    # -- Extended path helpers -----------------------------------------------

    @property
    def suffixes(self) -> list[str]:
        """All file extensions (e.g. ``['.tar', '.gz']``)."""
        return list(PurePosixPath(self.key).suffixes) if self.key else []

    @property
    def parts(self) -> tuple[str, ...]:
        """Key split into path components (e.g. ``('path', 'to', 'file.csv')``)."""
        return PurePosixPath(self.key).parts if self.key else ()

    # -- Heuristic helpers ---------------------------------------------------
    # Object storage has no true folder concept; these are name-based hints.

    @property
    def is_file(self) -> bool:
        """Heuristic: ``True`` when the key is non-empty and does not end with ``/``."""
        return bool(self.key) and not self.key.endswith("/")

    @property
    def is_folder(self) -> bool:
        """Heuristic: ``True`` when the key is empty or ends with ``/``."""
        return not self.key or self.key.endswith("/")
