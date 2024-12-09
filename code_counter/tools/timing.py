#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import time


def timing_decorator(func):
    """
    Decorator to measure the execution time of a function.

    Parameters
    ----------
    func : callable
        The function to be measured.

    Returns
    -------
    callable
        The decorated function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"The '{func.__name__}' operation took a total of {elapsed_time:.5f} seconds.")
        return result

    return wrapper
