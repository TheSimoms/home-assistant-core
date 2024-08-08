"""Config flow for Categorised Shopping List integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.util import slugify

from .const import CONF_SHOPPING_LIST_NAME, CONF_STORAGE_KEY, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SHOPPING_LIST_NAME): str,
    }
)


class CategorisedShoppingListConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Categorised Shopping List."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            name = user_input[CONF_SHOPPING_LIST_NAME]
            storage_key = slugify(name)

            self._async_abort_entries_match({CONF_STORAGE_KEY: storage_key})

            user_input[CONF_STORAGE_KEY] = storage_key

            return self.async_create_entry(title=name, data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)
