"""Test the Categorised Shopping List config flow."""

from unittest.mock import AsyncMock

from homeassistant import config_entries
from homeassistant.components.categorised_shopping_list.const import (
    CONF_SHOPPING_LIST_NAME,
    DOMAIN,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test the config form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_SHOPPING_LIST_NAME: "Test Shopping List"},
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Test Shopping List"
    assert len(mock_setup_entry.mock_calls) == 1
