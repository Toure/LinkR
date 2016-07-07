# LinkR
Wrapper for shell scripts to interface with jenkins through the generation
of junit status file.

### Usage:
```
usage: linkr.py [-h] [-s STATUS] [-ts TS] [-tc TC] [-tn TN] [-o OUTPUT_F]

optional arguments:
  -h, --help            show this help message and exit
  -s STATUS, --status STATUS
                        Test output result, `pass` | `fail` | `incomplete`.
  -ts TS, --test_suite TS
                        Test suite id.
  -tc TC, --test_case TC
                        Test Case id
  -tn TN, --test_name TN
                        Test Case name: (str) ex: Test_Undercloud
  -o OUTPUT_F, --output_file OUTPUT_F
                        Junit output filename
```

```
./linkr.py -s passed -ts test_deploy -tc test_1234 -tn deploy_node -o result.xml 
```

#### Output:
```
<?xml version="1.0" ?>
<testsuites errors="0" failures="0" tests="1" time="0.0">
        <testsuite errors="0" failures="0" name="rhos1234" skipped="0" tests="1" time="0">
                <testcase classname="pass" name="test_undercloud"/>
        </testsuite>
</testsuites>
```