import typing as t

import hikari
import miru

__all__ = ("blue_button", "green_button")

T = t.TypeVar("T", bound=miru.View)
ButtonCallback = t.Callable[[T, miru.ViewContext, miru.Button], t.Awaitable[None]]
ButtonDecorator = t.Callable[[ButtonCallback[T]], ButtonCallback[T]]
ButtonStyles = t.Literal[
    hikari.ButtonStyle.SUCCESS,
    hikari.ButtonStyle.DANGER,
    hikari.ButtonStyle.PRIMARY,
    hikari.ButtonStyle.SECONDARY,
]


def green_button(label: str, custom_id: str) -> ButtonDecorator[T]:
    return _button(label, custom_id, hikari.ButtonStyle.SUCCESS)


def blue_button(label: str, custom_id: str) -> ButtonDecorator[T]:
    return _button(label, custom_id, hikari.ButtonStyle.PRIMARY)


def _button(label: str, custom_id: str, style: ButtonStyles) -> ButtonDecorator[T]:
    def wrapper(func: ButtonCallback[T]) -> ButtonCallback[T]:
        @miru.button(label, custom_id=custom_id, style=style)
        def inner(view: T, ctx: miru.ViewContext, button: miru.Button) -> t.Awaitable[None]:
            return func(view, ctx, button)

        return inner

    return wrapper
