#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import threading
import sys
import time


class SearchingProgressBar(threading.Thread):
    __LEN__ = 10

    def __init__(self):
        super(SearchingProgressBar, self).__init__()
        self.daemon = True
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def __clear(self):
        sys.stdout.write("\r")
        sys.stdout.write("   " * self.__LEN__)
        sys.stdout.write("\r")
        sys.stdout.flush()

    def run(self):
        while True:
            progress = "searching "
            for i in range(self.__LEN__):
                if self.stopped():
                    self.__clear()
                    return
                time.sleep(0.1)
                sys.stdout.write("\r")
                progress += " ."
                sys.stdout.write(progress)
                sys.stdout.flush()
                sys.stdout.write("\r")
            sys.stdout.write("\r")
            sys.stdout.write("searching " + "  " * self.__LEN__)
            sys.stdout.write("\r")
            sys.stdout.flush()
