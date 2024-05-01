import typing as t


T = t.TypeVar("T")


class Injector:
    """Singleton dependency injector."""

    __injected = False

    def __init__(self) -> None:
        raise RuntimeError("Injector should not be instantiated.")

    @classmethod
    def initialize(
        cls, get: t.Callable[[t.Type[T]], T], set_: t.Callable[[t.Type[T], T], t.Any]
    ) -> t.Type["Injector"]:
        """Initializes the injector.

        Calling get or set before this method will raise a runtime error.

        Returns:
            The injector for chained calls.
        """
        cls.__get = get
        cls.__set = set_
        cls.__injected = True
        return cls

    @classmethod
    def get(cls, type_: t.Type[T]) -> T:
        """Gets the instance for the given type.

        Args:
            type_: The type to get.

        Returns:
            The requested instance.
        """
        if not cls.__injected:
            raise RuntimeError("Injector was not initialized.")

        return cls.__get(type_)  # pyright: ignore

    @classmethod
    def set(cls, type_: t.Type[T], instance: T) -> t.Type["Injector"]:
        """Sets the instance for the given type.

        Args:
            type_: The type to set.
            instance: The instance to set.

        Returns:
            The injector for chained calls.
        """
        if not cls.__injected:
            raise RuntimeError("Injector was not initialized.")

        cls.__set(type_, instance)  # pyright: ignore
        return cls
