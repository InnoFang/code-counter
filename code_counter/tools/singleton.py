#!/usr/bin/env python3
# -*- coding: utf-8  -*-

from typing import Type, Any, Dict


class SingletonMeta(type):
    """
    A metaclass for implementing the Singleton design pattern.

    This metaclass ensures that a class has only one instance and provides a global point of
    access to that instance.

    Usage
    -----
    ```
    class MyClass(metaclass=SingletonMeta):
        pass
    ```

    Now, `MyClass` will have only one instance, and subsequent calls to `MyClass()` will return
    the existing instance.
    """
    _instance: Dict[Type, Any] = {}

    def __call__(cls, *args, **kwargs):
        """
        Call method for creating an instance of the class.

        Parameter
        ---------
        cls: Type
            The class to create an instance of.

        *args
            Positional arguments to be passed to the class constructor.

        **kwargs
            Keyword arguments to be passed to the class constructor.

        Returns
        -------
        Any
            The instance of the class.
        """
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]
