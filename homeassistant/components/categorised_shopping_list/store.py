"""Data store for Categorised Shopping List integration."""

from typing import Any

from homeassistant.components.todo import TodoItem, TodoItemStatus
from homeassistant.helpers.storage import Store

from .data import Category, ShoppingList

VERSION = 1


class CategorisedShoppingListStore(Store[dict[str, Any]]):
    """Data store for Categorised Shopping List integration."""

    async def async_load_shopping_list(self) -> ShoppingList:
        """Load shopping list stored to disk, if any.

        Returns an empty list if no data is found.
        """

        data = await self.async_load()

        if data is None:
            return ShoppingList(items=[], categories=[], known_items={})

        items = [
            TodoItem(
                summary=item.get("summary"),
                uid=item.get("uid"),
                status=TodoItemStatus(item.get("status")),
                description=item.get("description"),
            )
            for item in data.get("items", [])
        ]

        categories = [
            Category(
                uid=item.get("uid"),
                name=item.get("name"),
            )
            for item in data.get("categories", [])
        ]

        return ShoppingList(
            items=items,
            categories=categories,
            known_items=data.get("known_items", {}),
        )
