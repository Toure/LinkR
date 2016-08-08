# LinkR
Wrapper for shell scripts to interface with jenkins through the generation
of junit status file.

### Usage:
```
usage: linkr.py [-h] [-pn PROJECT] [-ts TS] [-tc TC [TC ...]] [-tr TEST_RUN]
                [-et ET] [-t TAGS] [-pf PROPS_FILE] -o OUTPUT_F

Example: python linkr.py -pn TestProject -ts TestSuite_ID -tc TestCase-01
TestCase-02 -et 4 -pf /tmp/foo.props -o results.xml

optional arguments:
  -h, --help            show this help message and exit
  -pn PROJECT, --project_name PROJECT
                        Name of project which testsuite and testcase belong.
  -ts TS, --test_suite TS
                        Test suite id.
  -tc TC [TC ...], --test_case TC [TC ...]
                        Test Case id.
  -tr TEST_RUN, --test_run TEST_RUN
                        Test run name: (str) ex: Test_Undercloud
  -et ET, --elapse_time ET
                        Total time elapsed to complete test.
  -t TAGS, --tags TAGS  Tags to be included on all specified testcase.
  -d DESC, --description DESC
                        Description of Test Run: ex: This will rock the world.
  -r REL, --release REL
                        Planned in release name: ex: RHOS9
  -pf PROPS_FILE, --props PROPS_FILE
                        Polarion properties filename with path: ex:
                        /tmp/polarion.props
  -o OUTPUT_F, --output_file OUTPUT_F
                        Junit output filename

```

#### Output: results.xml
```
<?xml version="1.0" ?>
<testsuites errors="0" failures="0" tests="2" time="8.0">
        <testsuite errors="0" failures="0" name="TestProject" skipped="0" tests="2" time="8">
                <properties>
                        <property name="polarion-project-id" value="TestSuite_ID"/>
                </properties>
                <testcase name="TestCase-01" time="4.000000"/>
                <testcase name="TestCase-02" time="4.000000"/>
        </testsuite>
</testsuites>



```

#### Output: foo.props
```
polarion.run=TestWorld
TestCase-01=TestCase-01
TestCase-02=TestCase-02
```