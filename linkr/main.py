#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
from sys import argv
from junitxml import TestCase, TestSuite
from collections import OrderedDict
from json import dump
from requests import post, auth, codes, exceptions
import re
from configs.config_manager import ConfigManger


class LinkR(ConfigManger):
    """
    LinkR class
    """
    def __init__(self, args_obj):
        super(LinkR, self).__init__()
        self.args = args_obj
        self.polarion_url = self.getkey("url")
        self.username = self.getkey("username")
        self.password = self.getkey("password")

    def gen_junit(self):
        """
        Generates junit xml file from arguments passed on the cli.
        :return: junit.xml
        """

        test_attrs = [
            "polarion-project-id", "polarion-custom-description",
            "polarion-custom-plannedin", "polarion-custom-isautomated",
            "polarion-custom-tags"
        ]

        test_attrs_values = [
            self.args.ts, self.args.desc,
            self.args.rel, True, self.args.tags
        ]

        # This block allows for a dynamic dictionary to be created
        # depending on arguments passed.
        props = {
            key: value for key, value in zip(test_attrs,
                                             test_attrs_values)
            if value is not None
        }

        self._gen_polarion_property_file(test_attrs, test_attrs_values,
                                         self.args.tr, self.args.tc,
                                         property_file=self.args.pf)

        test_case = [TestCase(self.args.tc.pop(0), '', self.args.et)]

        if len(self.args.tc) >= 1:
            for cases in self.args.tc:
                test_case.append(TestCase(cases, '', self.args.et))

        testsuite = [TestSuite(self.args.project, test_case, properties=props)]

        with open(self.args.output_f, 'w') as results:
            TestSuite.to_file(results, testsuite)
        if self.args.ur:
            self._upload(self.polarion_url, self.args.output_f,
                         self.username, self.password)

    @staticmethod
    def _gen_polarion_property_file(test_attrs, test_attrs_values,
                                    test_run, test_case_id,
                                    property_file=None):
        """
        Generate a json mapping file.
        :param: test_attrs: list of polarion test run attributes.
        :param: test_attrs_values: list of values for test run attributes.
        :param: test_run: id of polarion test run.
        :param: test_case_id: list of test case ids.
        :param: property_file: output name of json file, if none test_run will
        used for file name.
        :return: polarion properties filename.
        """
        test_keys = ["polarion-testcase-id"] * len(test_case_id)
        properties_mapping = OrderedDict()
        properties_mapping["properties"] = {key: value for key, value in
                                            zip(test_attrs, test_attrs_values)
                                            if value is not None
                                            }
        properties_mapping["casemap"] = {
            test_run: [
                {key: value} for key, value in zip(test_keys, test_case_id)
            ]
        }

        if property_file is None:
            property_file = "/tmp/{}.json".format(test_run)

        with open(property_file, 'w') as prop_file:
            dump(properties_mapping, prop_file, sort_keys=False, indent=1)

        return property_file

    @staticmethod
    def _upload(url, data_file, username, password):
        """
        Upload will submit a results file via polarion ReST interface.
        """
        url_match = '(http(s)?)\:\/\/localhost'
        if re.search(url_match, url):
            print("Please configure url settings.")
            exit(1)

        polarion_request = post(url,
                                data=data_file,
                                auth=auth.HTTPBasicAuth(username,
                                                        password))
        status_code = polarion_request.status_code
        if status_code == codes.ok:
            return status_code
        else:
            print("Results upload failed with the follow: {}".format(
                polarion_request.status_code))
            raise exceptions.RequestException


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="Example: linkr  -pn TestProject "
                    "-tr TestWorld -ts TestSuite_ID -tc TestCase-01 "
                    "TestCase-02 -et 4 -pf /tmp/foo.props -u -o results.xml")
    parser.add_argument("-pn", "--project_name", dest="project",
                        help="Name of project which testsuite "
                             "and testcase belong.")

    parser.add_argument("-ts", "--test_suite", dest="ts", required=True,
                        help="Test suite id.")

    parser.add_argument("-tc", "--test_case", nargs='+',
                        dest="tc", required=True,
                        help="Test Case id. ")

    parser.add_argument("-tr", "--test_run", dest="tr", required=True,
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

    parser.add_argument("-pf", "--props", metavar="<testrun file name>",
                        default="/tmp/polarion.props",
                        dest="pf",
                        help="Polarion properties filename with path:"
                             " ex: /tmp/polarion.props")
    parser.add_argument("-u", "--upload_results", dest="ur",
                        action='store_true', default=False,
                        help="Upload boolean will indicate the need to push "
                             "results to polarion.")
    parser.add_argument("-o", "--output_file", metavar="<results filename>",
                        dest="output_f", required=True,
                        help="Junit output filename")

    args = parser.parse_args()
    linkr = LinkR(args)

    if len(argv) < 2:
        parser.print_help()
        exit(1)
    else:
        linkr.gen_junit()


if __name__ == "__main__":
    main()
