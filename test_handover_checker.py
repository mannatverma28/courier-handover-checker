import os
import unittest

import handover_checker


class TestHandoverChecker(unittest.TestCase):
    def test_task_example_ends_with_one_problem(self):
        lines = ["PKG1042,CHECKIN,08:15\n", "PKG1042,CHECKOUT,08:47\n", "PKG2077,CHECKOUT,09:10\n"]
        report = handover_checker.build_report(lines)
        self.assertEqual(report, [
            "PKG1042 IN=08:15 OUT=08:47 MINUTES=32",
            "PKG2077 IN=MISSING OUT=09:10 MINUTES=UNKNOWN",
            "PROBLEMS: 1",
        ])

    def test_missing_checkout(self):
        report = handover_checker.build_report(["PKG3150,CHECKIN,09:30\n"])
        self.assertEqual(report, ["PKG3150 IN=09:30 OUT=MISSING MINUTES=UNKNOWN", "PROBLEMS: 1"])

    def test_order_of_first_appearance(self):
        lines = ["B,CHECKIN,08:00", "A,CHECKIN,08:05", "B,CHECKOUT,08:10", "A,CHECKOUT,09:05"]
        report = handover_checker.build_report(lines)
        self.assertEqual(report[0], "B IN=08:00 OUT=08:10 MINUTES=10")
        self.assertEqual(report[1], "A IN=08:05 OUT=09:05 MINUTES=60")
        self.assertEqual(report[2], "PROBLEMS: 0")

    def test_minutes_across_the_hour(self):
        self.assertEqual(handover_checker.to_minutes("10:05"), 605)
        report = handover_checker.build_report(["P,CHECKIN,10:50", "P,CHECKOUT,12:05"])
        self.assertEqual(report[0], "P IN=10:50 OUT=12:05 MINUTES=75")

    def test_windows_line_endings_and_blank_lines(self):
        lines = ["PKG1,CHECKIN,07:00\r\n", "\r\n", "PKG1,CHECKOUT,07:45\r\n"]
        report = handover_checker.build_report(lines)
        self.assertEqual(report, ["PKG1 IN=07:00 OUT=07:45 MINUTES=45", "PROBLEMS: 0"])

    def test_empty_log(self):
        self.assertEqual(handover_checker.build_report([]), ["PROBLEMS: 0"])

    def test_reads_real_log_file(self):
        lines = handover_checker.read_log(handover_checker.LOG_FILE)
        self.assertEqual(os.path.basename(handover_checker.LOG_FILE), "handover_log.txt")
        report = handover_checker.build_report(lines)
        self.assertEqual(report[-1], "PROBLEMS: 2")


if __name__ == "__main__":
    unittest.main()