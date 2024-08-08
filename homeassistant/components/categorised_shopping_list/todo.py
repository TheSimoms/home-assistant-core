"""A categorised shopping list todo platform."""

from homeassistant.components.shopping_list import NoMatchingShoppingListItem
from homeassistant.components.todo import (
    TodoItem,
    TodoListEntity,
    TodoListEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import uuid

from . import CategorisedShoppingListConfigEntry
from .const import CONF_SHOPPING_LIST_NAME
from .data import ShoppingList
from .store import CategorisedShoppingListStore


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: CategorisedShoppingListConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the categorised_shopping_list todo platform."""

    store = config_entry.runtime_data
    shopping_list = await store.async_load_shopping_list()

    if shopping_list is None:
        shopping_list = ShoppingList(items=[], categories=[], known_items={})

    name = config_entry.data[CONF_SHOPPING_LIST_NAME]
    entity = CategorisedShoppingListEntity(
        store, shopping_list, name, unique_id=config_entry.entry_id
    )

    async_add_entities([entity], True)


class CategorisedShoppingListEntity(TodoListEntity):
    """A To-do List representation of the Categorised Shopping List."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_supported_features = (
        TodoListEntityFeature.CREATE_TODO_ITEM
        | TodoListEntityFeature.DELETE_TODO_ITEM
        | TodoListEntityFeature.UPDATE_TODO_ITEM
        | TodoListEntityFeature.MOVE_TODO_ITEM
        | TodoListEntityFeature.SET_DESCRIPTION_ON_ITEM
    )
    _attr_icon = "mdi:cart"

    def __init__(
        self,
        store: CategorisedShoppingListStore,
        shopping_list: ShoppingList,
        name: str,
        unique_id: str,
    ) -> None:
        """Initialize CategorisedShoppingListEntity."""

        self._store = store
        self._shopping_list = shopping_list
        self._attr_name = name.capitalize()
        self._attr_unique_id = unique_id

    async def async_update(self) -> None:
        """Update the _attr_todo_items property."""

        self._attr_todo_items = self._shopping_list["items"]

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """Add an item to the To-do list."""

        if item.uid is None:
            item.uid = uuid.random_uuid_hex()

        self._shopping_list["items"].append(item)

        await self.async_save()

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update an item to the To-do list."""

        if not item.uid:
            return

        index = self._find_index_by_uid(item.uid)

        self._shopping_list["items"][index] = item

        await self.async_save()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        """Remove an item from the To-do list."""

        for uid in uids:
            index = self._find_index_by_uid(uid)

            self._shopping_list["items"].pop(index)

        await self.async_save()

    async def async_move_todo_item(
        self, uid: str, previous_uid: str | None = None
    ) -> None:
        """Re-order an item to the To-do list."""

        if uid == previous_uid:
            return

        src_index = self._find_index_by_uid(uid)
        item = self._shopping_list["items"].pop(src_index)

        if previous_uid is None:
            dst_index = 0
        else:
            dst_index = self._find_index_by_uid(previous_uid) + 1

        self._shopping_list["items"].insert(dst_index, item)

        await self.async_save()

    def _find_index_by_uid(self, uid: str) -> int:
        """Find the shopping list item with the given uid."""

        for i, item in enumerate(self._shopping_list["items"]):
            if item.uid == uid:
                return i

        raise NoMatchingShoppingListItem(
            f"Item '{uid}' not found in shopping list '{self.entity_id}'"
        )

    async def async_save(self):
        """Store shopping list to disk and update HA state."""
        await self._store.async_save(self._shopping_list)
        await self.async_update_ha_state(force_refresh=True)
