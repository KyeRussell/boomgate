from . import cached_http


def test_load_save_cache(tmp_path):
    """Cache saving and loading."""

    cache_dir = tmp_path / ".test_cache"

    # Load a non-existent cache.
    cache = cached_http._load_cache(path=cache_dir)
    assert cache == {}

    # Make changes and re-asve the cache.
    cache["test"] = 1
    cached_http._save_cache(path=cache_dir, data=cache)

    # Load the cache again.
    cache = cached_http._load_cache(path=cache_dir)
    assert cache == {"test": 1}
