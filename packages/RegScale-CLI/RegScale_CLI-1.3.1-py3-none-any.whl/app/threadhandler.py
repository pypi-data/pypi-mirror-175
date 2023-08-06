#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thread handler to create and start threads"""

from typing import Tuple
from concurrent.futures import ThreadPoolExecutor


def create_threads(process, args: Tuple, thread_count: int, max_threads: int):
    """
    function to create x threads using ThreadPoolExecutor
    """
    # check to see if we need to go over the max threads and
    # assign allowed variable threads accordingly
    threads = max_threads if thread_count > max_threads else thread_count
    # start the threads with the number of threads allowed
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # iterate and start the threads that were requested
        for thread in range(threads):
            # assign each thread the passed process and args along with the thread number
            executor.submit(process, args, thread)
