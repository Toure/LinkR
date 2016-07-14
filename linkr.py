#!/usr/bin/env python
import argparse
from junit_xml import TestSuite, TestCase
from sys import argv, exit
import time
parser = argparse.ArgumentParser(description="Example: python linkr.py -s rhos-203004 -n 2 -ts rhos-23888 -tc 'rhos-1234"
                                             ", rhos-24050' -tn undercloud_test -o /tmp/results.xml")

parser.add_argument("-s", "--skip_test_name", dest="skip_test", help="Name of test(s) to mark skipped.")
parser.add_argument("-n", "--number_of_test", default= 1, dest="number_test", metavar="2",
                    help="Number of test to include in output file, this option will take a number and require a list"
                         " of test_cases for the `--test_case` option.")
parser.add_argument("-ts", "--test_suite", dest="ts", help="Test suite id.")
parser.add_argument("-tc", "--test_case", dest="tc", help="Test Case id, if number of test cases is `1`, else provide a"
                                                          " list seperated by commas: rhos-1234, rhos-2345")
parser.add_argument("-tn", "--test_name", dest="tn", help="Test Case name: (str) ex: Test_Undercloud")
parser.add_argument("-o", "--output_file", dest="output_f", help="Junit output filename")
# parser.add_argument("-r", "--requirements.txt", dest="req", help="Test case requirements.txt: "
#                                                            "`test foo will test this blah functionality`")

args = parser.parse_args()


class Linkr(object):
    def __init__(self):
        self.skip = args.skip_test
        self.number_test = args.number_test
        self.tc = args.tc
        self.tn = args.tn
        self.ts = args.ts
        self.et = time.clock()
        self.output_f = args.output_f
        # TODO work on requirement upload.
        #self.req = args.req

    def gen_junit(self):
        """
        Generates junit xml file from arguments passed on the cli.
        :return: junit.xml
        """
        if self.number_test == 1:
            #test_case = [TestCase(self.tn, None, self.tc, self.et)]
            #test_case.append(TestCase())
            test_case = [TestCase('Deployment_Test: Undercloud_Test', '', 0.000, '', '')]
            test_case.append(TestCase('Deployment_Test: Undercloud_Properties', '', 0.01, '', ''))

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
