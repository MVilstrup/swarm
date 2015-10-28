from watchdog.events import PatternMatchingEventHandler


class PageHandler(PatternMatchingEventHandler):
    patterns = ["*.html"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug

    def on_created(self, event):
        with open(event.src_path, 'r') as html_file:

