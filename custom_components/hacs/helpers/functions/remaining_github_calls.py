"""Helper to calculate the remaining calls to github."""
from custom_components.hacs.helpers.functions.logger import getLogger
import math


async def remaining(github):
    """Helper to calculate the remaining calls to github."""
    logger = getLogger("custom_components.hacs.remaining_github_calls")
    try:
        ratelimits = await github.get_rate_limit()
    except (BaseException, Exception) as exception:  # pylint: disable=broad-except
        logger.error(exception)
        return 0
    if ratelimits.get("remaining") is not None:
        return int(ratelimits["remaining"])
    return 0


async def get_fetch_updates_for(github):
    """Helper to calculate the number of repositories we can fetch data for."""
    margin = 100
    limit = await remaining(github)
    pr_repo = 10

    if limit - margin <= pr_repo:
        return 0
    return math.floor((limit - margin) / pr_repo)
