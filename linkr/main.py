#!/usr/bin/env python

import argparse
from requests import post, auth, codes, exceptions
from sys import argv
from junitxml import TestCase, TestSuite
from configs.config_manager import ConfigManger


class LinkR(ConfigManger):
    """
    LinkR
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
        # This block allows for a dynamic dictionary to be created
        # depending on arguments passed.
        keys = ["polarion-project-id", "polarion-custom-description",
                "polarion-custom-plannedin", "polarion-custom-isautomated",
                "polarion-custom-tags"]
        values = [self.args.ts, self.args.desc,
                  self.args.rel, True, self.args.tags]
        props = {key: value for key, value in zip(keys, values)
                 if value is not None}

        self._gen_polarion_property_file(self.args.tr, self.args.tc,
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
    def _gen_polarion_property_file(test_run, test_case, property_file=None):
        """
        Generate a simple mapping file.
        :return: polarion.properties
        """
        if property_file is None:
            property_file = "/tmp/props.json"

        with open(property_file, 'w') as prop_file:
            prop_file.write("polarion.run={}\n".format(test_run))
            for tc_id in test_case:
                prop_file.write("{}={}\n".format(tc_id, tc_id))
            prop_file.close()

        return property_file

    @staticmethod
    def _upload(url, data_file, username, password):
        """
        Upload will submit a results file via polarion ReST interface.
        """
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
        description="Example: python linkr  -pn TestProject "
                    "-tr TestWorld -ts TestSuite_ID -tc TestCase-01"
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

    parser.add_argument("-pf", "--props", metavar="polarion.props",
                        default="/tmp/polarion.props",
                        dest="pf",
                        help="Polarion properties filename with path:"
                             " ex: /tmp/polarion.props")
    parser.add_argument("-u", "--upload_results", dest="ur",
                        action='store_true', default=False,
                        help="Upload boolean will indicate the need to push "
                             "results to polarion.")
    parser.add_argument("-o", "--output_file", metavar="results.xml",
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
