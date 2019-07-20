#!/usr/bin/python3
# pylint: disable-msg=C0103,C0111,C0410,W0703
#
# Contact: fxia@yahoo.com (Fred Xia)
#
# Python3 packages required: pycrypto, tabulate
#
# Description:
#   A simple program using a master key to encrypt a collection of password
#   records. Each password record consists of a site, an account, and a
#   password.
#
#   The record collection is keyed by site. Use pickle library to serialize
#   and deserialize the collection.
#
#   It computes a 32-byte hash digest from master secrete password. The
#   digest is then used as the encryption key with AES256 encryption to
#   encrypt the serialized(pickled) binary value and decrypt the binary
#   before deserializing(un-pickle) to a record collection.
#
# Contact: fxia@yahoo.com
#
# usage: pwmg.py [-h] -k secrete [-f filename] [-n new_secrete] [-d]
#                [-i filename] [-x filename]
#                [site] [account] [password]
#
# optional arguments:
#   -h, --help      show this help message and exit
#   -k secrete      Secrete key
#   -f filename     Credential file.
#   -n new_secrete  New secrete key
#   -d              Delete site
#   -i filename     Import from a plain text file. Merge with existing.
#   -x filename     Export to a plain text file
#
# Note:
#
#     If -f is not specified the default is $PWMG_FILENAME if defined or
#     $HOME/.pwmg_db
#
#     Import/Export file format is lines of <site>, <account>, <password>
#     Each line is one site.
#
#     For option -i the merge will not overwrite credentials already exists
#     in the master records.
#
#
import os, sys, argparse, pickle, hashlib
from struct import pack, unpack, calcsize
from Crypto.Cipher import AES
from tabulate import tabulate

def normalizeSecrete(secrete):
    '''
    Create 32-byte hash from the master secrete. This hash is used as key
    for AES256 encryption.
    '''
    if secrete is None:
        raise Exception("Must provide secrete key")
    m = hashlib.shake_256()
    m.update(secrete.encode())
    # pylint: disable-msg=E1121
    return m.digest(32)
    # pylint: enable-msg=E1121

class Credentials:

    def __init__(self):
        self.records = {}
        self.filename = None

    def setCredential(self, site, account, password):
        self.records[site] = (account, password)

    def deleteCredential(self, site):
        if site in self.records:
            del self.records[site]

    def getCredentials(self, site):
        '''
        Return a list of tuples (site, account, password) for all records
        whose site contains 'site' substring.
        '''
        # Find matching sub string
        records = []
        for s in self.records:
            if site in s:
                records.append((s, self.records[s][0], self.records[s][1]))
        return records

    def saveCredentials(self, filename, secrete):
        data = pickle.dumps(self)
        dataLen = len(data)
        padding = dataLen % 16
        if padding > 0:
            data += b" " * (16 - padding)
        aes = AES.new(normalizeSecrete(secrete), AES.MODE_ECB)
        ciperText = aes.encrypt(data)
        fh = open(filename, "wb")
        if not fh:
            raise Exception("Cannot open file %s" % filename)
        fh.write(pack("i", dataLen))
        fh.write(ciperText)
        fh.close()

    def exportCredentials(self, filenameOrHandle, prettyPrint):
        '''
        Export credentials to either a file handle, or to a file.
        prettyPrint or comma-separated format (good for import).
        '''
        if isinstance(filenameOrHandle, str):
            fh = open(filenameOrHandle, "w")
            if not fh:
                raise Exception("Cannot open file %s" % filenameOrHandle)
        else:
            fh = filenameOrHandle
        if not prettyPrint:
            for site in sorted(self.records.keys()):
                fh.write("%s, %s, %s\n" % (site,
                                           self.records[site][0],
                                           self.records[site][1]))
        else:
            rows = []
            for site in sorted(self.records.keys()):
                rows.append((site,
                             self.records[site][0],
                             self.records[site][1]))
            print("\nMaster file: %s\n" % self.filename)
            print(tabulate(rows, headers=["Site", "Account", "Password"]),
                  file=filenameOrHandle)
        if isinstance(filenameOrHandle, str):
            fh.close()

    @staticmethod
    def loadCredentials(filename, secrete):
        if not os.path.isfile(filename):
            print("File %s does not exist" % filename)
            return None
        fh = open(filename, "rb")
        if not fh:
            raise Exception("Cannot read file %s" % filename)
        intSz = calcsize("i")
        dataLen, = unpack("i", fh.read(intSz))
        cipherText = fh.read()
        #print("cipher len: %d, %d" % (len(cipherText), dataLen))
        fh.close()
        aes = AES.new(normalizeSecrete(secrete), AES.MODE_ECB)
        data = aes.decrypt(cipherText)
        if not data:
            raise Exception("Decrypt failed")
        try:
            creds = pickle.loads(data[:dataLen])
            creds.filename = filename
            assert isinstance(creds, Credentials)
            return creds
        except Exception:
            print("Decryption failed. Either incorrect password or file")

    @staticmethod
    def importCredentials(inputFile, outputFile, secrete):
        '''
        Import credential from a plain text file. File must be in a format
        in which each line is <site>,<account>,<password>. Line starting
        with '#' is ignored.
        '''
        if not os.path.isfile(inputFile):
            raise Exception("File %s not found" % inputFile)
        fh = open(inputFile, "r")
        if not fh:
            raise Exception("Cannot open file %s" % inputFile)
        creds = Credentials()
        while True:
            line = fh.readline()
            if not line:
                break
            if line.startswith("#"):
                continue
            items = line.strip().split(",")
            if len(items) != 3:
                print("Skip line %s" % line)
                continue
            creds.setCredential(items[0].strip(),
                                items[1].strip(),
                                items[2].strip())
        fh.close()
        if not creds.records:
            raise Exception("Imported zero credentials")
        # Merge with existing credentials only if no site exists in
        # imported credentials
        existingCreds = Credentials.loadCredentials(outputFile, secrete)
        if existingCreds:
            for site in existingCreds.records:
                if not site in creds.records:
                    creds.setCredential(site,
                                        existingCreds.records[site][0],
                                        existingCreds.records[site][1])
        creds.saveCredentials(outputFile, secrete)

    @staticmethod
    def defaultCredsFile():
        if os.getenv("PWMG_FILENAME"):
            return os.getenv("PWMG_FILENAME")
        return "%s/.pwmg_db" % os.getenv("HOME")

def initParser():
    parser = argparse.ArgumentParser(description="pwmg command line")
    add_arg = parser.add_argument
    add_arg("-k", metavar="secrete", type=str, required=True,
            help="Secrete key")
    add_arg("-f", metavar="filename", type=str,
            default=Credentials.defaultCredsFile(),
            help="Credential file")
    add_arg("-n", metavar="new_secrete", type=str,
            help="New secrete key")
    add_arg("-d", action="store_true",
            help="Delete site")
    add_arg("-i", metavar="filename", type=str,
            help="Import from a plain text file. Merge with existing.")
    add_arg("-x", metavar="filename", type=str,
            help="Export to a plain text file")
    add_arg("site", metavar="site", type=str, nargs="?")
    add_arg("account", metavar="account", type=str, nargs="?")
    add_arg("password", metavar="password", type=str, nargs="?")
    return parser

def runCommand(args):
    # pylint: disable-msg=R0912
    if not args.k:
        raise Exception("Must provide secrete key")
    creds = Credentials.loadCredentials(args.f, args.k)
    if args.n:
        # Use new secrete key
        if creds and creds.records:
            creds.saveCredentials(args.f, args.n)
        else:
            print("Credential is empty")
        return
    if args.x:
        # Export credentials to plain text file
        if creds and creds.records:
            creds.exportCredentials(args.x, prettyPrint=False)
        else:
            print("Credential is empty")
        return
    if args.i:
        # Import credentials from a plain text file. Wipe out all existing
        # credentials. There is no merge.
        Credentials.importCredentials(args.i, args.f, args.k)
        return
    if not args.site:
        # Dump all credentials
        if creds and creds.records:
            creds.exportCredentials(sys.stdout, prettyPrint=True)
        else:
            print("Credential is empty")
        return

    # Has site argument
    if args.password is not None:
        # Set credential of the site
        if creds is None:
            creds = Credentials()
        creds.setCredential(args.site, args.account, args.password)
        creds.saveCredentials(args.f, args.k)
        print("Password saved")
    elif args.d:
        creds.deleteCredential(args.site)
        creds.saveCredentials(args.f, args.k)
    else:
        creds = creds.getCredentials(args.site)
        if creds:
            print(tabulate(creds, headers=["Site", "Account", "Password"]))
        else:
            print("Site note found")

    # pylint : enable-msg=R0912

def main():
    parser = initParser()
    args = parser.parse_args()
    runCommand(args)

if __name__ == "__main__":
    main()
