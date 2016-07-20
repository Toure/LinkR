#!/usr/bin/env python
import argparse
from junitxml import TestSuite, TestCase
from sys import argv, exit

parser = argparse.ArgumentParser(
    description="Example: python linkr.py -s rhos-203004 -n 2 -ts rhos-23888 -tc 'rhos-1234, "
                "rhos-24050' -tn undercloud_test -o /tmp/results.xml")

parser.add_argument("-s", "--skip_test_name", nargs='+', dest="skip_test",
                    help="Name of test(s) to mark skipped.")
parser.add_argument("-m", "--skip_message", dest="message",
                    help="Detailing in regards to skipping test, ex: bz1234")
parser.add_argument("-pn", "--project_name", dest="project",
                    help="Name of project which testsuite and testcase belong.")
parser.add_argument("-ts", "--test_suite", dest="ts",
                    help="Test suite id.")

parser.add_argument("-tc", "--test_case", nargs='+', dest="tc",
                    help="Test Case id. ")

parser.add_argument("-tn", "--test_name", dest="tn",
                    help="Test Case name: (str) ex: Test_Undercloud")

parser.add_argument("-et", "--elapse_time", dest="et", type=int,
                    help="Total time elapsed to complete test.")

parser.add_argument("-jl", "--job_link", default=None, dest="job_url",
                    help="Job link provides a means of including job url in test update.")

parser.add_argument("-t", "--tags", default=None, dest="tags",
                    help="Tags to be included on all specified testcase.")

parser.add_argument("-o", "--output_file", dest="output_f",
                    help="Junit output filename")

args = parser.parse_args()


def gen_junit():
    """
    Generates junit xml file from arguments passed on the cli.
    :return: junit.xml
    """

    if len(args.tc) == 1:
        test_case = [TestCase(args.tc.pop(0), '', args.et, '', '')]
        ts = [TestSuite(args.ts, test_case, properties={'polarion-custom-jenkinsjobs': args.job_url,
                                                        'polarion-project-id': args.project,
                                                        'polarion-custom-isautomated': True,
                                                        'polarion-custom-tags': args.tags})]
    else:
        test_case = [TestCase(args.tc.pop(0), '', args.et, '', '')]
        for cases in args.tc:
            test_case.append(TestCase(cases, '', args.et, '', ''))

        ts = [TestSuite(args.ts, test_case, properties={'polarion-project-id': args.project,
                                                        'polarion-custom-jenkinsjobs': args.job_url,
                                                        'polarion-custom-isautomated': True,
                                                        'polarion-custom-tags': args.tags})]

    with open(args.output_f, 'w') as results:
        TestSuite.to_file(results, ts)


def main():
    """
    CLI interface.
    :return: None
    """
    if len(argv) < 2:
        parser.print_help()
        exit(1)
    else:
        gen_junit()


if __name__ == "__main__":
    main()
