#!/usr/bin/env python

import argparse
import requests
from requests.auth import HTTPBasicAuth
from sys import argv
from junitxml import TestSuite, TestCase


def gen_junit(args):
    """
    Generates junit xml file from arguments passed on the cli.
    :return: junit.xml
    """
    # This block allows for a dynamic dictionary to be created
    # depending on arguments passed.
    keys = ["polarion-project-id", "polarion-custom-description",
            "polarion-custom-plannedin", "polarion-custom-isautomated",
            "polarion-custom-tags"]
    values = [args.ts, args.desc, args.rel, True, args.tags]
    props = {key: value for key, value in zip(keys, values)
             if value is not None}

    _gen_polarion_property_file(args)
    test_case = [TestCase(args.tc.pop(0), '', args.et)]

    if len(args.tc) >= 1:
        for cases in args.tc:
            test_case.append(TestCase(cases, '', args.et))

    testsuite = [TestSuite(args.project, test_case, properties=props)]

    with open(args.output_f, 'w') as results:
        TestSuite.to_file(results, testsuite)


def _gen_polarion_property_file(args):
    """
    Generate a simple mapping file.
    :return: polarion.properties
    """
    with open(args.props_file, 'w') as prop_file:
        prop_file.write("polarion.run={}\n".format(args.test_run))
        for tc_id in args.tc:
            prop_file.write("{}={}\n".format(tc_id, tc_id))
        prop_file.close()


def upload(polarion_url, results, username, password):
    """
    Upload will submit a results file via polarion ReST interface.
    """
    polarion_request = requests.post(polarion_url,
                                     data=results,
                                     auth=HTTPBasicAuth(username, password))

    try:
        polarion_request.status_code == requests.codes.ok
    except requests.exceptions.RequestException:
        print("Results upload failed with the follow: {}".format(
            polarion_request.status_code))


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="Example: python linkr.py  -pn TestProject "
                    "-tr TestWorld -ts TestSuite_ID -tc TestCase-01"
                    "TestCase-02 -et 4 -pf /tmp/foo.props -o results.xml")
    parser.add_argument("-pn", "--project_name", dest="project",
                        help="Name of project which testsuite "
                             "and testcase belong.")

    parser.add_argument("-ts", "--test_suite", dest="ts", required=True,
                        help="Test suite id.")

    parser.add_argument("-tc", "--test_case", nargs='+',
                        dest="tc", required=True,
                        help="Test Case id. ")

    parser.add_argument("-tr", "--test_run", dest="test_run", required=True,
                        help="Test run name: (str) ex: Test_Undercloud")

    parser.add_argument("-et", "--elapse_time", dest="et", type=int,
                        help="Total time elapsed to complete test.")

    parser.add_argument("-t", "--tags", default=None, dest="tags",
                        help="Tags to be included on all specified testcase.")

    parser.add_argument("-d", "--description", default=None, dest="desc",
                        help="Description of Test Run: "
                             "ex: This will rock the world.")

    parser.add_argument("-r", "--release", default=None, dest="rel",
                        help="Planned in release name: ex: RHOS9")

    parser.add_argument("-pf", "--props", default="/tmp/polarion.props",
                        dest="props_file",
                        help="Polarion properties filename with path:"
                             " ex: /tmp/polarion.props")

    parser.add_argument("-o", "--output_file", dest="output_f", required=True,
                        help="Junit output filename")

    args = parser.parse_args()

    if len(argv) < 2:
        parser.print_help()
        exit(1)
    else:
        gen_junit(args)


if __name__ == "__main__":
    main()
