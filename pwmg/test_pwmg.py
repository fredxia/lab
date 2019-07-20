#!/usr/bin/python3
# pylint: disable-msg=C0103,C0111,C0410
#
# Test pwmg.py, a password management script
#
# pylint: disable-msg=R0915
#
import os, re, shlex, subprocess, time
from datetime import datetime
import pdb

def runCommand(cmdStr, cmdInput=None, isPwmg=True):
    if cmdStr:
        tokens = shlex.split(cmdStr)
    else:
        tokens = []
    if isPwmg:
        tokens.insert(0, "./pwmg.py")
    if not cmdInput:
        handle = subprocess.Popen(tokens, stdout=subprocess.PIPE)
        data, _ = handle.communicate()
    elif not isinstance(cmdInput, list):
        handle = subprocess.Popen(tokens, stdout=subprocess.PIPE,
                                  stdin=subprocess.PIPE)
        data, _ = handle.communicate(input=cmdInput)
    else:
        handle = subprocess.Popen(tokens, stdout=subprocess.PIPE,
                                  stdin=subprocess.PIPE)
        output = []
        for s in cmdInput:
            # read prompt and write input.
            data = handle.stdout.readline()
            output.extend(data.decode("ascii").split("\n"))
            handle.stdin.write(s)
            handle.stdin.write(b"\n")
            handle.stdin.flush()
        data = handle.stdout.readline()
        output.extend(data.decode("ascii").split("\n"))
        handle.stdin.close()
        handle.stdout.close()
        handle.terminate()
        return output
    return data.decode("ascii").split("\n")

def verifyOutput(output, lookFor, negative=False):
    '''Output is a list of lines. lookFor is either one str token or a list
       of tokens. negative means token(s) should not exist in output'''
    if isinstance(lookFor, str):
        lookFor = [lookFor]
    count = 0
    for line in output:
        line = re.sub(" +", " ", line)
        for token in lookFor:
            if token in line:
                if negative:
                    assert False, lookFor + " is in output %s" % line
                count += 1
                break
    if not negative:
        assert count == len(lookFor), "%d items not found" % (
            len(lookFor) - count)

class PwmgTest:

    def __init__(self):
        # Use tmp file to save credentials
        self.tmpFile = "/tmp/pwmg_test_%s" % os.getpid()
        os.putenv("PWMG_FILENAME", self.tmpFile)
        self.today = datetime.fromtimestamp(time.time()).strftime("%y/%m/%d")
        self.tmpFiles = set([self.tmpFile])

    def __del__(self):
        for f in self.tmpFiles:
            if os.path.exists(f):
                os.remove(f)

    def makeTmpFileName(self):
        name = "/tmp/pwmg_test_%s_%s" % (os.getpid(), len(self.tmpFiles))
        self.tmpFiles.add(name)
        return name
        
    def test1(self):
        output = runCommand("-k 1234 abcd")
        verifyOutput(output, "No credentials loaded")
        runCommand("-k 1234 site1 acc1 pass1")
        output = runCommand("-k 1234")
        verifyOutput(output, (self.tmpFile,
                              "Site Account Password",
                              "site1 acc1 pass1 %s" % self.today))
        assert os.path.isfile(self.tmpFile)
        output = runCommand("-k 1234 abcd")
        verifyOutput(output, "Site not found")
        print("test1 passed")

    def test2(self):
        # test adding a credential
        runCommand("-k 1234 site2 acc2 pass2")
        output = runCommand("-k 1234")
        verifyOutput(output, ("site1 acc1 pass1 %s" % self.today,
                              "site2 acc2 pass2 %s" % self.today))
        # Verify showing one credential
        output = runCommand("-k 1234 site2")
        verifyOutput(output, ("Site Account Password",
                              "site2 acc2 pass2 %s" % self.today))
        verifyOutput(output, "site1 acc1 pass1", negative=True)
        print("test2 passed")

    def test3(self):
        # test matching substring in query
        output = runCommand("-k 1234 site")
        verifyOutput(output, ("Site Account Password",
                              "site1 acc1 pass1 %s" % self.today,
                              "site2 acc2 pass2 %s" % self.today))
        print("test3 passed")

    def test4(self):
        # test import
        os.remove(self.tmpFile)

        # Generate v0 import (no timestamp)
        importFile = self.makeTmpFileName()
        fh = open(importFile, "w")
        for i in range(30):
            fh.write("site%02d, acc%d, pass%d\n" % (i, i, i))
        fh.close()
        self.tmpFiles.add(importFile)

        runCommand("-k 1234 -i %s" % importFile)

        # test query single site
        output = runCommand("-k 1234 site00")
        verifyOutput(output, "site00 acc0 pass0 %s" % self.today)
        # test print all records
        output = runCommand("-k 1234")
        verifyOutput(output, ("acc19 pass19 %s" % self.today,
                              "acc29 pass29 %s" % self.today))

        os.remove(self.tmpFile)
        os.remove(importFile)

        # Generate v1 import. timestamp can be one of two formats
        tms = ["19/03/05", "18/12/22", "20/08/11", "21/07/01"]
        fh = open(importFile, "w")
        for i in range(30):
            tm = tms[i % 4]
            if i % 4 > 2:
                tm = int(time.mktime(time.strptime(tm, "%y/%m/%d")))
            fh.write("site%02d, acc%d, pass%d, %s\n" % (i, i, i, tm))
        fh.close()

        runCommand("-k 1234 -i %s" % importFile)
        output = runCommand("-k 1234 site00")
        verifyOutput(output, "site00 acc0 pass0 %s" % tms[0])

        output = runCommand("-k 1234")
        verifyOutput(output, ("acc19 pass19 %s" % tms[19 % 4],
                              "acc29 pass29 %s" % tms[29 % 4]))

        # test export
        exportFile = self.makeTmpFileName()
        runCommand("-k 1234 -x %s" % exportFile)
        output = runCommand("cat %s" % exportFile, isPwmg=False)
        verifyOutput(output, "site00, acc0, pass0, %s" % tms[0])
        verifyOutput(output, ("site19, acc19, pass19, %s" % tms[19 % 4],
                              "site29, acc29, pass29, %s" % tms[29 % 4]))
        self.tmpFiles.add(exportFile)

        # test merge from another file
        importFile2 = self.makeTmpFileName()
        fh = open(importFile2, "w")
        for i in range(50, 60):
            fh.write("site%02d, acc%d, pass%d, %s\n" % (i, i, i, tms[i % 4]))
        fh.close()
        self.tmpFiles.add(importFile2)

        runCommand("-k 1234 -i %s" % importFile2)
        runCommand("-k 1234 -x %s" % exportFile)

        output = runCommand("cat %s" % exportFile, isPwmg=False)
        verifyOutput(output, ("site00, acc0, pass0, %s" % tms[0],
                              "site19, acc19, pass19, %s" % tms[19 % 4],
                              "site29, acc29, pass29, %s" % tms[29 % 4],
                              "site50, acc50, pass50, %s" % tms[50 % 4],
                              "site59, acc59, pass59, %s" % tms[59 % 4]))

        os.remove(importFile)
        os.remove(importFile2)
        os.remove(exportFile)
        print("test4 passed")

    def test5(self):
        # test delete single credential
        runCommand("-k 1234 -d site21")
        runCommand("-k 1234 -d site51")

        exportFile = self.makeTmpFileName()
        runCommand("-k 1234 -x %s" % exportFile)
        self.tmpFiles.add(exportFile)
        output = runCommand("grep site21 %s" % exportFile, isPwmg=False)
        assert output[0] == ""
        output = runCommand("grep site51 %s" % exportFile, isPwmg=False)
        assert output[0] == ""
        output = runCommand("grep site2 %s" % exportFile, isPwmg=False)
        # output has 9 items plus a ""
        assert len(output) == 10

        output = runCommand("-k 1234 site21")
        verifyOutput(output, "Site not found")
        print("test5 passed")

    def test6(self):
        # test interactive password. input must be a binary string
        output = runCommand("site2", cmdInput=b"1234")
        verifyOutput(output, ("site20 acc20 pass20",
                              "site25 acc25 pass25",
                              "site26 acc26 pass26"))
        output = runCommand("site100 acc100 pass100", cmdInput=b"1234")
        verifyOutput(output, "Password saved")
        output = runCommand("site100", cmdInput=b"1234")
        verifyOutput(output, ("site100 acc100 pass100"))
        print("test6 passed")

    def test7(self):
        # test quoted string
        runCommand("'my site' 'my account' 'my password'", cmdInput=b"1234")
        output = runCommand("-k 1234")
        verifyOutput(output, "my site my account my password")
        output = runCommand("'my si'", cmdInput=b"1234")
        verifyOutput(output, "my site my account my password")
        print("test7 passed")

    def test8(self):
        # test change secrete
        output = runCommand("-k 1234 -n 4321")
        verifyOutput(output, ("Encrypted with new secrete key"))
        output = runCommand("-k 4321")
        verifyOutput(output, ("site20 acc20 pass20",
                              "site25 acc25 pass25",
                              "site26 acc26 pass26",
                              "site100 acc100 pass100"))
        # interactive change of secrete key
        output = runCommand("-c", cmdInput=[b"4321", b"abcd"])
        verifyOutput(output, ("Encrypted with new secrete key"))
        output = runCommand(None, cmdInput=b"abcd")
        verifyOutput(output, ("site20 acc20 pass20",
                              "site25 acc25 pass25",
                              "site26 acc26 pass26",
                              "site100 acc100 pass100"))
        print("test8 passed")

    def test9(self):
        # test -f option
        tmpFile2 = self.tmpFile + "2"
        os.rename(self.tmpFile, tmpFile2)
        self.tmpFiles.add(tmpFile2)
        output = runCommand("-k abcd -f %s" % tmpFile2)
        verifyOutput(output, ("site20 acc20 pass20",
                              "site25 acc25 pass25",
                              "site26 acc26 pass26",
                              "site100 acc100 pass100"))
        output = runCommand("-c -f %s" % tmpFile2, cmdInput=[b"abcd", b"1234"])
        verifyOutput(output, ("Encrypted with new secrete key"))
        output = runCommand("-k 1234 -n 4321 -f %s" % tmpFile2)
        verifyOutput(output, ("Encrypted with new secrete key"))
        output = runCommand("-k 4321 -f %s site20" % tmpFile2)
        verifyOutput(output, ("site20 acc20 pass20"))
        runCommand("-k 4321 -f %s site200 acc200 pass200" % tmpFile2)
        output = runCommand("-k 4321 -f %s site200" % tmpFile2)
        verifyOutput(output, ("site200 acc200 pass200"))
        output = runCommand("-k 4321 -f %s site2" % tmpFile2)
        verifyOutput(output, ("site20 acc20 pass20",
                              "site25 acc25 pass25",
                              "site26 acc26 pass26"))
        verifyOutput(output, ("site100 acc100 pass100"), negative=True)
        runCommand("-k 4321 -f %s -d site26" % tmpFile2)
        output = runCommand("-k 4321 -f %s" % tmpFile2)
        verifyOutput(output, ("site26 acc26 pass26"), negative=True)
        print("test9 passed")

    def test10(self):
        # test import/export and secrete change with -f option
        importFile = self.makeTmpFileName()
        fh = open(importFile, "w")
        for i in range(30):
            fh.write("xyz%02d, acc%d, pass%d\n" % (i, i, i))
        fh.close()
        self.tmpFiles.add(importFile)

        tmpFile2 = self.tmpFile + "2"
        runCommand("-k 4321 -f %s -i %s" % (tmpFile2, importFile))
        output = runCommand("-k 4321 -f %s" % tmpFile2)
        verifyOutput(output, (tmpFile2,
                              "xyz10 acc10 pass10",
                              "xyz29 acc29 pass29"))
        self.tmpFiles.add(tmpFile2)
        # test -x with -f
        exportFile = self.makeTmpFileName()
        output = runCommand("-k 4321 -f %s -x %s" % (tmpFile2, exportFile))
        verifyOutput(output, ("Credentials exported to %s" % exportFile))
        output = runCommand("grep xyz29 %s" % exportFile, isPwmg=False)
        verifyOutput(output, ("xyz29, acc29, pass29, %s" % self.today))
        self.tmpFiles.add(exportFile)
        print("test10 passed")

    def run(self):
        self.test1()
        self.test2()
        self.test3()
        self.test4()
        self.test5()
        self.test6()
        self.test7()
        self.test8()
        self.test9()
        self.test10()
        print("Test complete")

if __name__ == "__main__":
    test = PwmgTest()
    test.run()

