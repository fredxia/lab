#!/usr/bin/python3
# pylint: disable-msg=C0103,C0111,C0410
#
# Test pwmg.py, a password management script
#
# pylint: disable-msg=R0915
#
import os, re, shlex, subprocess

def runCommand(cmdStr):
    tokens = shlex.split(cmdStr)
    handle = subprocess.Popen(tokens, stdout=subprocess.PIPE)
    data, _ = handle.communicate()
    return data.decode("ascii").split("\n")

def verifyOutput(output, lookFor, negative=False):
    if isinstance(lookFor, str):
        for line in output:
            # Shrink multiple whitepsaces into one
            line = re.sub(" +", " ", line)
            if lookFor in line:
                if negative:
                    assert False, lookFor + " in output %s" % line
                return
        if not negative:
            assert False, lookFor + " not found in %s" % output
    else:
        count = 0
        for line in output:
            # Shrink multiple whitepsaces into one
            line = re.sub(" +", " ", line)
            for token in lookFor:
                if token in line:
                    if negative:
                        assert False, lookFor + " in output %s" % line
                    count += 1
                    break
        if not negative:
            assert count == len(lookFor), "%d items not found" % (
                len(lookFor) - count)

def runTests():
    prog = "./pwmg.py"

    tmpFile = "/tmp/test_%s" % os.getpid()
    os.putenv("PWMG_FILENAME", tmpFile)

    # basic test
    runCommand("%s -k 1234 site1 acc1 pass1" % prog)
    output = runCommand("%s -k 1234" % prog)
    verifyOutput(output, (tmpFile,
                          "Site Account Password",
                          "site1 acc1 pass1"))
    assert os.path.isfile(tmpFile)
    print("test1 passed")

    # test adding a credential
    runCommand("%s -k 1234 site2 acc2 pass2" % prog)
    output = runCommand("%s -k 1234" % prog)
    verifyOutput(output, ("site1 acc1 pass1",
                          "site2 acc2 pass2"))
    output = runCommand("%s -k 1234 site2" % prog)
    verifyOutput(output, ("Site Account Password",
                          "site2 acc2 pass2"))
    verifyOutput(output, "site1 acc1 pass1", negative=True)
    print("test2 passed")

    # Cleanup db file
    os.unlink(tmpFile)

    # Generate files to test import. Use two-digit siteXX str to make the
    # alphabetical order the same for import and export
    importFile = "/tmp/import_%d.txt" % os.getpid()
    fh = open(importFile, "w")
    for i in range(30):
        fh.write("site%02d, acc%d, pass%d\n" % (i, i, i))
    fh.close()
    runCommand("%s -k 1234 -i %s" % (prog, importFile))
    # test query single site
    output = runCommand("%s -k 1234 site00" % prog)
    verifyOutput(output, "site00 acc0 pass0")
    # test print all records
    output = runCommand("%s -k 1234" % prog)
    verifyOutput(output, ("acc19 pass19", "acc29 pass29"))
    print("test3 passed")

    # test export. Verify importFile and exportFile should be the same
    exportFile = "/tmp/export_%d.txt" % os.getpid()
    runCommand("%s -k 1234 -x %s" % (prog, exportFile))
    output = runCommand("diff %s %s" % (importFile, exportFile))
    assert output[0] == "", "%s:%s, output %s" % (
        importFile, exportFile, output)
    print("test4 passed")

    # test import and merge, second import file starting site name from 50
    importFile2 = "/tmp/import2_%d.txt" % os.getpid()
    fh = open(importFile2, "w")
    for i in range(50, 60):
        fh.write("site%02d, acc%d, pass%d\n" % (i, i, i))
    fh.close()
    runCommand("%s -k 1234 -i %s" % (prog, importFile2))
    runCommand("%s -k 1234 -x %s" % (prog, exportFile))
    os.system("cat %s >> %s" % (importFile2, importFile))
    output = runCommand("diff %s %s" % (importFile, exportFile))
    assert output[0] == "", "%s:%s:%s, output %s" % (
        importFile, importFile2, exportFile, output)
    print("test5 passed")

    # test delete option
    runCommand("%s -k 1234 -d site21" % prog)
    runCommand("%s -k 1234 -d site51" % prog)
    runCommand("%s -k 1234 -x %s" % (prog, exportFile))
    output = runCommand("grep site21 %s" % exportFile)
    assert output[0] == "", "%s" % exportFile
    output = runCommand("grep site51 %s" % exportFile)
    assert output[0] == "", "%s" % exportFile
    output = runCommand("grep site2 %s" % exportFile)
    # output has 9 items plus a ""
    assert len(output) == 10, "%s, %s" % (output, exportFile)
    print("test6 passed")

    # Cleanup db file
    os.unlink(tmpFile)

    # test quoted string
    runCommand("%s -k 1234 'my site' 'my account' 'my password'" % prog)
    output = runCommand("%s -k 1234" % prog)
    verifyOutput(output, "my site my account my password")
    print("test7 passed")

    # test new secrete
    runCommand("%s -k 1234 -n 4321" % prog)
    output = runCommand("%s -k 4321" % prog)
    verifyOutput(output, "my site my account my password")
    print("test8 passed")

    # test option -f
    tmpFile2 = tmpFile + "2"
    os.rename(tmpFile, tmpFile2)
    assert not os.path.isfile(tmpFile)
    runCommand("%s -k 4321 -f %s" % (prog, tmpFile2))
    runCommand("%s -k 4321 -f %s site5 acc5 pass5" % (prog, tmpFile2))
    output = runCommand("%s -k 4321 -f %s" % (prog, tmpFile2))
    verifyOutput(output, ("my site my account my password",
                          "site5 acc5 pass5"))
    print("test9 passed")

    # test -d with -f
    runCommand("%s -k 4321 -f %s -d site5" % (prog, tmpFile2))
    output = runCommand("%s -k 4321 -f %s" % (prog, tmpFile2))
    verifyOutput(output, "site5 acc5 pass5", negative=True)
    print("test10 passed")

    # test -i with -f, importFile2 has site50 - site59
    runCommand("%s -k 4321 -f %s -i %s" % (prog, tmpFile2, importFile2))
    output = runCommand("%s -k 4321 -f %s" % (prog, tmpFile2))
    verifyOutput(output, (tmpFile2,
                          "site50 acc50 pass50",
                          "site59 acc59 pass59"))
    print("test11 passed")

    # test -x with -f
    runCommand("%s -k 4321 -f %s -d 'my site'" % (prog, tmpFile2))
    runCommand("%s -k 4321 -f %s -x %s" % (prog, tmpFile2, exportFile))
    output = runCommand("diff %s %s" % (importFile2, exportFile))
    assert output[0] == "", "%s:%s, output %s" % (
        importFile2, exportFile, output)
    print("test12 passed")

    # test -n with -f
    runCommand("%s -k 4321 -n 1234 -f %s" % (prog, tmpFile2))
    runCommand("%s -k 1234 -x %s" % (prog, exportFile))
    output = runCommand("diff %s %s" % (importFile2, exportFile))
    assert output[0] == "", "%s:%s, output %s" % (
        importFile2, exportFile, output)
    print("test13 passed")

    for filename in (importFile, importFile2, exportFile, tmpFile2):
        os.unlink(filename)

runTests()
