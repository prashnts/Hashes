#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
#!encoding: UTF-8

from Hashes import cityhash
#from subprocess import call
import json, re, os, subprocess, time

# Load the Random String file, and call the subroutine.
Tests = []
_command = "python3 main.py "

_hashes = {}

_dumpvar = []

def populateTest():
    global Tests
    for file in os.listdir('dat'):
        if "str-20-10000-" in file:
            with open('dat/' + file) as minion:
                for testStr in minion:
                    Tests.append(testStr)
                #break


if __name__ == "__main__":
    print("Begining File Caching")

    populateTest()

    print("Begining Test")

    for test in Tests:
        process = subprocess.Popen(["time", "python3", "main.py", test[0:-1]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate()
        userTime = re.findall("\d+.\d+", str(err))[1]
        
        length = len(test[0:-1])

        hash_ = str(out)[2:-3]

        _hashes[test[0:-1]] = hash_

        out = (test[0:-1], len(test) - 1, hash_, userTime)

        _dumpvar.append((test[0:-1], hash_, length, userTime))

        print(out)

    print("Begining Verification of Hash Quality")

    # Flip the Test-Hash as Hash-Test.
    # 
    print("Preprocessing the Test-Hash")
    rev_multidict = {}
    for key, value in _hashes.items():
        rev_multidict.setdefault(value, set()).add(key)

    collisions = [key for key, values in rev_multidict.items() if len(values) > 1]

    print("Printing collisions:")
    print(collisions)

    print("REPORT:")
    print("Total Tests Carried Out:", len(Tests))
    print("Total Collisions:", len(collisions))

    print("Dumping the Data in file.")

    with open("report/" + str(int(time.time()/10)) + ".dump.json", "w") as minion:
        minion.write(json.dumps(_dumpvar, indent=4))

    with open("report/" + str(int(time.time()/10)) + ".collision.json", "w") as minion:
        minion.write(json.dumps(collisions, indent=4))

    print("OK")


    #for test in _hashes:
        