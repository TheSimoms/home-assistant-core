"""Data classes for Categorised Shopping List integration."""

from typing import TypedDict

from homeassistant.components.todo import TodoItem


class Category(TypedDict):
    """Shopping List category."""

    uid: str
    name: str


class ShoppingList(TypedDict):
    """Shopping List."""

    items: list[TodoItem]
    categories: list[Category]
    known_items: dict[str, str | None]
