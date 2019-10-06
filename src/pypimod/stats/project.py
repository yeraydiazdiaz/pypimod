import logging
import statistics

import pendulum


logger = logging.getLogger(__name__)


def get_release_frequency_for_project(project_dict: dict) -> float:
    """Computes the release frequency of a project from a project dict.

    Defined as the median of the number of days between releases.
    """
    release_dates = {}
    for version, releases in project_dict["releases"].items():
        if releases:
            release_dates[version] = pendulum.parse(
                max(r["upload_time"] for r in releases)
            )
    dates = sorted(list(release_dates.values()))
    if len(dates) == 1:
        release_frequency = 0.0
    else:
        release_frequency = float(
            statistics.median(
                (dates[i] - dates[i - 1]).in_days() for i in range(1, len(dates))
            )
        )
    return release_frequency or 0.001  # apparently 0 is not strictly positive?
