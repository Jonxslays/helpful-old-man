import typing as t


T = t.TypeVar("T")


class Injector:
    __injected = False

    @classmethod
    def initialize(
        cls, get: t.Callable[[t.Type[T]], T], set_: t.Callable[[t.Type[T], T], t.Any]
    ) -> None:
        cls.__get = get
        cls.__set = set_
        cls.__injected = True

    @classmethod
    def get(cls, type_: t.Type[T]) -> T:
        if not cls.__injected:
            raise RuntimeError("Injector was not initialized.")

        return cls.__get(type_)  # pyright: ignore

    @classmethod
    def set(cls, type_: t.Type[T], instance: T) -> None:
        if not cls.__injected:
            raise RuntimeError("Injector was not initialized.")

        cls.__set(type_, instance)  # pyright: ignore
        return None
