# LinkR
Wrapper for shell scripts to interface with jenkins through the generation
of junit status file.

### Usage:
```
usage: linkr.py [-h] [-s SKIP_TEST] [-ts TS] [-tc TC [TC ...]] [-tn TN]
                [-et ET] [-jl JOB_URL] [-t TAGS] [-o OUTPUT_F]

Example: python linkr.py -s rhos-203004 -n 2 -ts rhos-23888 -tc 'rhos-1234,
rhos-24050' -tn undercloud_test -o /tmp/results.xml

optional arguments:
  -h, --help            show this help message and exit
  -s SKIP_TEST, --skip_test_name SKIP_TEST
                        Name of test(s) to mark skipped.
  -ts TS, --test_suite TS
                        Test suite id.
  -tc TC [TC ...], --test_case TC [TC ...]
                        Test Case id.
  -tn TN, --test_name TN
                        Test Case name: (str) ex: Test_Undercloud
  -et ET, --elapse_time ET
                        Total time to run test.
  -jl JOB_URL, --job_link JOB_URL
                        Job link provides a means of including job url in test
                        update.
  -t TAGS, --tags TAGS  Tags for testcase.
  -o OUTPUT_F, --output_file OUTPUT_F
                        Junit output filename

```

```
python ./linkr.py -tn "Undercloud Deployment" -jl http://localhost -t director 
        -tc rhos-1020203 rhos-120203030 rhos-3040301 -ts "RHOS_9_DEPLOYMENT_TEST" -et 0.23 -o test_results.xml 
```

#### Output:
```
<?xml version="1.0" ?>
<testsuites errors="0" failures="0" tests="3" time="0.69">
        <testsuite errors="0" failures="0" name="RHOS_9_DEPLOYMENT_TEST" skipped="0" tests="3" time="0.69">
                <properties>
                        <property name="polarion-custom-isautomated" value="True"/>
                        <property name="polarion-custom-tags" value="director"/>
                        <property name="polarion-custom-jenkinsjobs" value="http://localhost"/>
                </properties>
                <testcase name="Undercloud Deployment: rhos-1020203" time="0.230000"/>
                <testcase name="Undercloud Deployment: rhos-120203030" time="0.230000"/>
                <testcase name="Undercloud Deployment: rhos-3040301" time="0.230000"/>
        </testsuite>
</testsuites>


```