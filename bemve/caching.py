import hashlib
from pathlib import Path


class CacheManager:
    """Handles hash-based caching for partial movie clips."""

    @staticmethod
    def compute_hash(*data_strings: str) -> str:
        """Generates an MD5 hash key from animation state data."""
        hasher = hashlib.md5()
        for string in data_strings:
            hasher.update(string.encode("utf-8"))
        return hasher.hexdigest()[:12]

    @staticmethod
    def is_cached(clip_path: Path) -> bool:
        """Checks if a valid cached partial clip file exists on disk."""
        return clip_path.exists() and clip_path.stat().st_size > 0
