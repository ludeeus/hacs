"""Starting setup task: extra stores."""
from ..enums import HacsCategory, HacsStage
from .base import HacsTaskRuntimeBase


async def async_setup() -> None:
    """Set up this task."""
    return Task()


class Task(HacsTaskRuntimeBase):
    """Set up extra stores in HACS if enabled in Home Assistant."""

    stages = [HacsStage.SETUP, HacsStage.RUNNING]

    async def execute(self) -> None:
        self.hacs.common.categories = set()
        for category in (
            HacsCategory.INTEGRATION,
            HacsCategory.LOVELACE,
            HacsCategory.PLUGIN,
        ):
            self.hacs.enable_hacs_category(HacsCategory(category))

        if HacsCategory.PYTHON_SCRIPT in self.hacs.hass.config.components:
            self.hacs.enable_hacs_category(HacsCategory.PYTHON_SCRIPT)

        if self.hacs.hass.services.has_service("frontend", "reload_themes"):
            self.hacs.enable_hacs_category(HacsCategory.THEME)

        if self.hacs.configuration.appdaemon:
            self.hacs.enable_hacs_category(HacsCategory.APPDAEMON)
        if self.hacs.configuration.netdaemon:
            self.hacs.enable_hacs_category(HacsCategory.NETDAEMON)
