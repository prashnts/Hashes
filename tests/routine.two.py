#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
#!encoding: UTF-8

import json, sys

if __name__ == "__main__":
    for i in sys.argv[1:]:
        with open(i, "r") as minion:
            a = json.loads(minion.read())
            time = 0
            out = ""
            for j in a:
                print(j)

                for value in j:
                    out += str(value) + ","

                out += "\n"

            print(i)

            with open(i + ".out.csv", "w") as banana:
                banana.write(out)