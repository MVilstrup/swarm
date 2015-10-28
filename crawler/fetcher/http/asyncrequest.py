class AsynchronousRequest(object):
    def __init__(self, function, *args, **kwargs):
        """ Executes the function in the background.
            AsynchronousRequest.done is False as long as it is busy, but the program will not halt in the meantime.
            AsynchronousRequest.value contains the function's return value once done.
            AsynchronousRequest.error contains the Exception raised by an erronous function.
            For example, this is useful for running live web requests while keeping an animation running.
            For good reasons, there is no way to interrupt a background process (i.e. Python thread).
            You are responsible for ensuring that the given function doesn't hang.
        """
        self._response = None  # The return value of the given function.
        self._error = None  # The exception (if any) raised by the function.
        self._time = time.time()
        self._function = function
        self._thread = threading.Thread(target=self._fetch,
                                        args=(function, ) + args,
                                        kwargs=kwargs)
        self._thread.start()

    def _fetch(self, function, *args, **kwargs):
        """ Executes the function and sets AsynchronousRequest.response.
        """
        try:
            self._response = function(*args, **kwargs)
        except Exception as e:
            self._error = e

    def now(self):
        """ Waits for the function to finish and yields its return value.
        """
        self._thread.join()
        return self._response

    @property
    def elapsed(self):
        return time.time() - self._time

    @property
    def done(self):
        return not self._thread.isAlive()

    @property
    def value(self):
        return self._response

    @property
    def error(self):
        return self._error

    def __repr__(self):
        return "AsynchronousRequest(function='%s')" % self._function.__name__

def asynchronous(function, *args, **kwargs):
    """ Returns an AsynchronousRequest object for the given function.
    """
    return AsynchronousRequest(function, *args, **kwargs)
