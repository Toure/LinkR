import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", dest="filename", help="Output junit filename.")
parser.add_argument("-s", "--status", dest="status", help="Test output result, `pass` | `fail` | `incomplete`.")
parser.add_argument("-id", "--gen-id", dest="id", help="Creates a unique id for test cases.")
parser.add_argument("-r", "--requirements", dest="req", help="Test case requirements: "
                                                             "`test foo will test this blah functionality`")

args = parser.parse_args()

def test_me():
    print("testing the arguments")
    print("These were given: {}, {}, {}, {}".format(args.filename, args.status, args.id,
                                                    args.req))

test_me()
