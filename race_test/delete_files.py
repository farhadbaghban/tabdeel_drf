import glob
import os

for filename in glob.glob("./race_test/statuscodes/*.txt"):
    os.remove(filename)
