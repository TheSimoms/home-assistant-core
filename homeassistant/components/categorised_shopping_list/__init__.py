"""The Categorised Shopping List integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_STORAGE_KEY
from .store import VERSION, CategorisedShoppingListStore

PLATFORMS: list[Platform] = [Platform.TODO]

type CategorisedShoppingListConfigEntry = ConfigEntry[CategorisedShoppingListStore]


async def async_setup_entry(
    hass: HomeAssistant, entry: CategorisedShoppingListConfigEntry
) -> bool:
    """Set up Categorised Shopping List from a config entry."""

    storage_key = entry.data[CONF_STORAGE_KEY]
    store = CategorisedShoppingListStore(hass, VERSION, storage_key)

    try:
        await store.async_load()
    except OSError as exception:
        raise ConfigEntryNotReady("Failed to load file {path}: {err}") from exception

    entry.runtime_data = store

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: CategorisedShoppingListConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_entry(
    hass: HomeAssistant, entry: CategorisedShoppingListConfigEntry
) -> None:
    """Remove a config entry."""

    storage_key = entry.data[CONF_STORAGE_KEY]
    store = CategorisedShoppingListStore(hass, VERSION, storage_key)
    path = Path(store.path)

    await hass.async_add_executor_job(
        lambda path: path.unlink(missing_ok=True),
        path,
    )
