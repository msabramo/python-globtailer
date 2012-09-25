import logging
import multiprocessing
import os
import shutil
import tempfile
import time
import unittest

from globtailer import TailMostRecentlyModifiedFileMatchingGlobPatternGenerator

logging.basicConfig(level=logging.WARNING)


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="python-globtailer-tests-")
        logging.info("Created temporary directory - %s" % self.tmpdir)
        self.tailer = TailMostRecentlyModifiedFileMatchingGlobPatternGenerator(self.get_path("log*"), max_duration=6)


    def tearDown(self):
        logging.info("Removing temporary directory - %s" % self.tmpdir)
        shutil.rmtree(self.tmpdir)
        logging.info("Removed temporary directory - %s" % self.tmpdir)


    def get_path(self, arg):
        return os.path.join(self.tmpdir, arg)


    def test_basic_use(self):
        with open(self.get_path("log.01.01"), "w") as f:
            f.write("line1\n")
            f.write("line2\n")
            f.write("line3\n")

        def write_to_log():
            time.sleep(1)

            with open(self.get_path("log.01.01"), "a") as f:
                f.write("line4\n")
                f.write("line5\n")
                f.write("line6\n")

            time.sleep(1)

            with open(self.get_path("log.01.02"), "a") as f:
                f.write("line7\n")
                f.write("line8\n")
                f.write("line9\n")

        self.assertEqual(self.tailer.glob_pattern, self.get_path("log*"))
        self.assertEqual(self.tailer.get_most_recent_filename(), self.get_path("log.01.01"))

        process = multiprocessing.Process(target=write_to_log)
        process.start()

        a_iter = iter(self.tailer)

        line = next(a_iter)
        self.assertEqual(line, "line4\n")
        line = next(a_iter)
        self.assertEqual(line, "line5\n")
        line = next(a_iter)
        self.assertEqual(line, "line6\n")
        line = next(a_iter)
        self.assertEqual(line, "line7\n")
        line = next(a_iter)
        self.assertEqual(line, "line8\n")
        line = next(a_iter)
        self.assertEqual(line, "line9\n")

        process.join()


    def test_no_matching_files(self):
        for line in self.tailer:
            print(line)

        print("*** DONE ***")
