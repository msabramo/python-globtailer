python-globtailer
=================

A generator that yields lines from the most recently modified file matching a glob pattern

Example::

    tailer = TailMostRecentlyModifiedFileMatchingGlobPatternGenerator("/path/to/log*")

    for line in tailer:
        print(line)
