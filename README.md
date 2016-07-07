# LinkR
Wrapper for shell scripts to interface with pylarion library which is a
python based project. This project will service as a bridge to 
allow engineers to port existing test to python.

### Usage:

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