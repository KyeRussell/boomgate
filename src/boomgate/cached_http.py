from pathlib import Path
import pickle
import httpx

import logging
from datetime import timedelta, datetime

logger = logging.getLogger(__name__)


def _load_cache(path: Path, default=None):
    if not default:
        default = {}
    if path.exists():
        with path.open("rb") as f:
            return pickle.load(f)
    return default


def _save_cache(path: Path, data):
    with path.open("wb") as f:
        pickle.dump(data, f)


class local_cache:
    """Context processor for loading and saving cache."""

    def __init__(self, path: Path, default):
        self.path = path
        self.default = default

    def __enter__(self):
        self.data = _load_cache(self.path, self.default)
        return self.data

    def __exit__(self, exc_type, exc_value, traceback):
        _save_cache(self.path, self.data)
        return False  # raise exception if any


def get(*args, **kwargs):
    logger.debug("Making HTTP request (%s, %s).", args, kwargs)
    with local_cache(Path(".request_cache"), {}) as cache:
        # cache key = args / kwargs passed to httpx
        cache_key = (args, tuple(kwargs.items()))

        if cache_key in cache:
            logger.debug("We have a cached response for this request.")

            # Is this recent enough to go straight to using our cached response
            # without even checking if there's a newer response available?
            if "cached_at" in cache[cache_key] and cache[cache_key][
                "cached_at"
            ] > datetime.now() - timedelta(hours=1):
                logger.debug(
                    "This cached response is recent enough to use without checking for "
                    "a newer response."
                )
                return cache[cache_key]["response"]
            else:
                logger.debug(
                    "This cached response is not recent enough to use without checking "
                    "for a newer response."
                )

            kwargs["headers"] = {"If-None-Match": cache[cache_key]["etag"]}

        response = httpx.get(*args, **kwargs)

        if response.status_code == 304:
            # Our local cached version is still valid.
            logger.debug("Our local cached version is still valid. Using it.")
            cache[cache_key] = {
                "etag": response.headers["ETag"]
                if "ETag" in response.headers
                else None,
                "response": cache[cache_key]["response"],
                "cached_at": datetime.now(),
            }
            return cache[cache_key]["response"]
        else:
            logger.debug("We have a fresh response. Saving it in the cache.")
            # Save the response in the cache.
            if "ETag" in response.headers:
                cache[cache_key] = {
                    "etag": response.headers["ETag"],
                    "response": response,
                    "cached_at": datetime.now(),
                }

        return response
