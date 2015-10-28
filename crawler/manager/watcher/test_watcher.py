from watchdog.observers import Observer
from watcher import MyHandler
import sys
import time

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(PageHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
