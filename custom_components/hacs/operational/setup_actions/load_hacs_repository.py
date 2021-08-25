"""Starting setup task: load HACS repository."""
from custom_components.hacs.exceptions import HacsException
from custom_components.hacs.helpers.functions.information import get_repository
from custom_components.hacs.helpers.functions.register_repository import (
    register_repository,
)
from custom_components.hacs.share import get_hacs

from ...enums import HacsSetupTask


async def async_load_hacs_repository():
    """Load HACS repositroy."""
    hacs = get_hacs()
    hacs.log.info("Setup task %s", HacsSetupTask.HACS_REPO)

    try:
        repository = hacs.get_by_name("hacs/integration")
        if repository is None:
            await register_repository("hacs/integration", "integration")
            repository = hacs.get_by_name("hacs/integration")
        if repository is None:
            raise HacsException("Unknown error")
        repository.data.installed = True
        repository.data.installed_version = hacs.integration.version
        repository.data.new = False
        hacs.repository = repository.repository_object
        hacs.data_repo, _ = await get_repository(
            hacs.session, hacs.configuration.token, "hacs/default", None
        )
    except HacsException as exception:
        if "403" in f"{exception}":
            hacs.log.critical("GitHub API is ratelimited, or the token is wrong.")
        else:
            hacs.log.critical(f"[{exception}] - Could not load HACS!")
        return False
    return True
