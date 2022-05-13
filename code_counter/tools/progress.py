#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import threading
import sys
import time

from code_counter.tools import singleton


class SearchingProgressBar(threading.Thread, metaclass=singleton.SingletonMeta):
    __LEN__ = 10

    def __init__(self):
        super(SearchingProgressBar, self).__init__()
        self.daemon = True
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

    def stop(self):
        if not self.is_stopped():
            self._stop_event.set()
            self.join()

    def pause(self):
        if not self.is_stopped():
            self._pause_event.set()

    def resume(self):
        if self.is_paused():
            self._pause_event.clear()

    def is_paused(self):
        return self._pause_event.is_set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def __clear(self):
        sys.stdout.write("\r")
        sys.stdout.write("   " * self.__LEN__)
        sys.stdout.write("\r")
        sys.stdout.flush()

    def run(self):
        self._stop_event.clear()
        while True:
            if self.is_paused():
                self.__clear()
                continue
            progress = "searching "
            for i in range(self.__LEN__):
                if self.is_stopped():
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
