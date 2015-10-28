#!/usr/bin/env python
try:
    from asyncio import JoinableQueue as Queue
except ImportError:
    # In Python 3.5, asyncio.JoinableQueue is
    # merged into Queue.
    from asyncio import Queue

class Fetcher(object):
    """
    Async Page fetcher, that c 

    """

    def __init__(self, max_tasks=20):
        self.max_tasks = max_tasks
        self.max_redirect = max_redirect
        self.q = Queue()

        # aiohttp's ClientSession does connection pooling and
        # HTTP keep-alives for us.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.fetch())
        self.session = aiohttp.ClientSession(loop=loop)


    @asyncio.coroutine
    def fetch(self):
        """
        Run the fetcher until all work is done.
        """
        # Create workers that fetch pages
        workers = [asyncio.Task(self.work())
                   for _ in range(self.max_tasks / 2)]

        # Create seeders that takes URLs from redis and adds it to own queue
        seeders = [asyncio.Task(self.get_seeds())
                   for _ in range(self.max_tasks / 2)]

        # When all work is done, exit.
        yield from self.q.join()
        for s in seeders:
            s.cancel()
        for w in workers:
            w.cancel()

    @asyncio.coroutine
    def work(self):
        while True:
            # Get URLs from own queue
            url = yield from self.q.get()

            # Download page
            yield from self.fetch_url(url)
            self.q.task_done()

    @asyncio.coroutine
    def fetch_url(self, url):
        # Handle redirects ourselves.
        response = yield from self.session.get(
            url, allow_redirects=True)

        try:
            # Handle the reponse
            pass
        finally:
            # Return connection to pool.
            yield from response.release()


    @asyncio.coroutine
    def get_seeds(self):
        while True:
            pass
