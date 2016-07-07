#!/usr/bin/env python
import argparse
from junit_xml import TestSuite, TestCase
from sys import argv, exit
import time
parser = argparse.ArgumentParser()

parser.add_argument("-s", "--status", dest="status", help="Test output result, `pass` | `fail` | `incomplete`.")
parser.add_argument("-ts", "--test_suite", dest="ts", help="Test suite id.")
parser.add_argument("-tc", "--test_case", dest="tc", help="Test Case id")
parser.add_argument("-tn", "--test_name", dest="tn", help="Test Case name: (str) ex: Test_Undercloud")
parser.add_argument("-o", "--output_file", dest="output_f", help="Junit output filename")
# parser.add_argument("-r", "--requirements.txt", dest="req", help="Test case requirements.txt: "
#                                                            "`test foo will test this blah functionality`")

args = parser.parse_args()


class Linkr(object):
    def __init__(self):
        self.status = args.status
        self.tc = args.tc
        self.tn = args.tn
        self.ts = args.ts
        self.et = time.clock()
        self.output_f = args.output_f
        #self.req = args.req

    def gen_junit(self):
        """
        Generates junit xml file from arguments passed on the cli.
        :return: junit.xml
        """
        test_case = [TestCase(self.tn, self.tc, self.et, self.status)]
        ts = TestSuite(self.ts, test_case)

        with open(self.output_f, 'w') as results:
            TestSuite.to_file(results, [ts])


def main():
    """
    CLI interface.
    :return: None
    """
    if len(argv) < 2:
        parser.print_help()
        exit(1)

    link_testr = Linkr()
    link_testr.gen_junit()

if __name__ == "__main__":
    main()
