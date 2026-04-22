#
# morestd: More standard libraries for Python
#
# Copyright 2010-2026 Ferry Boender, released under the MIT license
#

"""
Retry calls to functions with configurable retries, delays, etc.

In the following example, we define a custom exception class and a Test class
which will raise that exception two times before succeeding. We use the Retry
class to retry calling the `call` method of the class with some parameters
until it succeeds. We only retry on the `ForcedError` exception.

    >>> class ForcedError(Exception):
    ...    pass

    >>> class Test:
    ...    def __init__(self, fail_times):
    ...        self.fail_times = fail_times
    ...        self.fail_cnt = 0
    ...
    ...    def call(self, text, optional=False):
    ...        self.fail_cnt += 1
    ...        print(f"Test.call: {text} ({optional}). "
    ...              f"Try {self.fail_cnt} of {self.fail_times}")
    ...        if self.fail_cnt < self.fail_times:
    ...            raise ForcedError("Failure")
    ...        return True

    >>> test = Test(fail_times=2)
    >>> r = Retry(exceptions=[ForcedError])
    >>> r.retry(test.call, "hello", optional=True)
    Test.call: hello (True). Try 1 of 2
    Test.call: hello (True). Try 2 of 2
    True

The output of which would be:

    Test.call: hello (True). Try 1 of 2
    Test.call: hello (True). Try 2 of 2
    True
"""

import time


class Retry:
    """
    Retry calls to a callback function.

    `max_tries` is the maximum nr of tries.

    `delay` is the amount of seconds to wait between each try.

    The `backoff_factor` determines by how much `delay` is increased each try
    by multiplying `delay` with this factor. E.g. `backoff_factor=1` will not
    increase the `delay`, `backoff_factor=2` will multiply the `delay` by two
    each time (1, 2, 4, 8).

    `max_delay` is a maximum value that `delay` may become due to
    `backoff_factor`. The default is `False`, meaning there is no maximum
    delay.

    `exceptions` is a list of exceptions you want to retry for. The default is
    `Exception`, which may be overly broad as it will also retry bugs in code
    such as TypeErrors.
    """
    def __init__(self, max_tries=3, delay=1, backoff_factor=1, max_delay=False,
                 exceptions=[Exception]):
        self.max_tries = max_tries
        self.delay = delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.exceptions = exceptions

    def retry(self, callback, *args, **kwargs):
        delay = self.delay
        tries = 0

        while True:
            tries += 1
            try:
                result = callback(*args, **kwargs)
                return result
            except Exception as err:
                # Check if the exception that occurred is an instance of any of
                # the exceptions we want to retry. If not, just raise it
                if not any(
                    [
                        isinstance(err, exception)
                        for exception
                        in self.exceptions
                    ]
                ):
                    raise

                # We tried max amount of times, just raise the error
                if tries >= self.max_tries:
                    raise

            time.sleep(delay)
            delay = delay * self.backoff_factor
            if self.max_delay is not False and delay > self.max_delay:
                delay = self.max_delay


if __name__ == '__main__':
    import doctest
    doctest.testmod()
