"""Module with custom descriptors for class attributes."""


class NonNegative:
    """Descriptor to enforce non-negative values for class attributes.

    Example:
        >>> class TestClass:
        ...     value = NonNegative()
        ...
        >>> obj = TestClass()
        >>> obj.value = 10
        >>> obj.value
        10
        >>> obj.value = -1
        Traceback (most recent call last):
            ...
        ValueError: value value must be non-negative
    """

    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name[2:]} value must be non-negative")
        setattr(instance, self.name, value)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
