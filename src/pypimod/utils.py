import json
from pathlib import Path

from pypimod.config import settings

HERE = Path(__file__).absolute()
DEV_PATH = HERE.parents[2] / "dev"
CACHED_RESULTS_PATH = DEV_PATH / "cached_bq_results.json"


def cache_results(func):
    """A very simple decorator to store and return cached results
    of generic functions based on arguments."""

    def wrapper(*args, **kwargs):
        filename = "_".join(
            [
                "cached_result_" + func.__name__,
                "_".join((str(arg) for arg in args)) if args else "",
                "_".join((f"{k}-{v}" for k, v in kwargs.items())) if kwargs else "",
            ]
        )
        path = settings.CACHED_RESULTS_PATH.absolute().parent / filename
        if path.exists():
            with open(path, "r") as fd:
                return json.loads(fd.read())
        else:
            results = func(*args, **kwargs)
            try:
                with open(path, "w") as fd:
                    fd.write(json.dumps(results))
            except Exception:
                path.unlink()
                raise

            return results

    return wrapper
