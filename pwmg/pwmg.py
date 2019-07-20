#!/usr/bin/python3
# pylint: disable-msg=C0103,C0111,C0410,W0703
#
# Contact: fxia@yahoo.com (Fred Xia)
#
# Python3 packages required: pycrypto, tabulate
#
# A very simple password management program. Please see README.org for more
# information.
#
import os, sys, argparse, pickle, hashlib, time
from datetime import datetime
from struct import pack, unpack, calcsize
from Crypto.Cipher import AES
from tabulate import tabulate

version = 1

def normalizeSecrete(secrete):
    '''
    Create 32-byte hash from the master secrete. This hash is used as key
    for AES256 encryption.
    '''
    assert secrete, "Must provide secrete key"
    m = hashlib.shake_256()
    m.update(secrete.encode())
    # pylint: disable-msg=E1121
    return m.digest(32)
    # pylint: enable-msg=E1121

def readSecreteInput(prompt):
    s = input(prompt + "\n")
    return s

def printTabulate(records, fh=None):
    rows = []
    for site in sorted(records.keys()):
        rec = records[site]
        tm = "" if len(rec) == 2 else \
            datetime.fromtimestamp(rec[2]).strftime("%y/%m/%d")
        rows.append((site, rec[0], rec[1], tm))
    print(tabulate(rows, headers=["Site", "Account", "Password", "Timestamp"]),
          file=fh if fh else sys.stdout)

class Credentials:

    def __init__(self):
        self.records = {}
        self.filename = None

    def setCredential(self, site, account, password, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())
        self.records[site] = (account, password, timestamp)

    def deleteCredential(self, site):
        if site in self.records:
            del self.records[site]

    def getCredentials(self, siteStr):
        creds = {}
        for s, rec in self.records.items():
            if siteStr in s: # match substring
                creds[s] = rec
        return creds

    def saveCredentials(self, filename, secrete):
        '''Encrypt using secrete and save credential records to a file. File
           format is a length of pickled but pre-encrypt data, followed by
           the cyper text.
        '''
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
        fh.write(pack("i", version))
        fh.write(pack("i", dataLen))
        fh.write(ciperText)
        fh.close()

    def exportCredentials(self, filenameOrHandle, prettyPrint):
        '''Export credentials to either a file handle, or to a file.
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
                rec = self.records[site]
                if len(rec) == 2:
                    # Use today's date for timestamp
                    tm = time.strftime("%y/%m/%d")
                else:
                    tm = datetime.fromtimestamp(rec[2]).strftime("%y/%m/%d")
                fh.write("%s, %s, %s, %s\n" % (site, rec[0], rec[1], tm))
        else:
            print("\nMaster file: %s\n" % self.filename)
            printTabulate(self.records, filenameOrHandle)
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
        ver, = unpack("i", fh.read(intSz))
        assert version == ver
        dataLen, = unpack("i", fh.read(intSz))
        cipherText = fh.read()
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
        '''Import credential from a plain text file. File must be in a format
           in which each line is <site>,<account>,<password>. Line starting
           with '#' is ignored.
        '''
        assert os.path.isfile(inputFile), "File %s not found" % inputFile
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
            if len(items) >= 3:
                timestamp = None
                if len(items) == 4:
                    if '/' in items[3]:
                        timestamp = int(time.mktime(time.strptime(
                            items[3].strip(), "%y/%m/%d")))
                    else:
                        timestamp = int(items[3].strip())
                creds.setCredential(items[0].strip(),
                                    items[1].strip(),
                                    items[2].strip(),
                                    timestamp)
            else:
                print("Skip line %s" % line)
        fh.close()
        assert creds.records, "Imported zero credentials"

        # Merge with existing credentials for sites not in imported credentials
        existingCreds = Credentials.loadCredentials(outputFile, secrete)
        if existingCreds:
            for site, rec in existingCreds.records.items():
                if not site in creds.records:
                    creds.setCredential(site, *rec)
        creds.saveCredentials(outputFile, secrete)

    @staticmethod
    def defaultCredsFile():
        if os.getenv("PWMG_FILENAME"):
            return os.getenv("PWMG_FILENAME")
        return "%s/.pwmg_db" % os.getenv("HOME")

def initParser():
    parser = argparse.ArgumentParser(description="pwmg command line")
    add_arg = parser.add_argument
    add_arg("-k", metavar="secrete", type=str, required=False,
            help="Secrete key")
    add_arg("-f", metavar="filename", type=str,
            default=Credentials.defaultCredsFile(),
            help="Credential file")
    add_arg("-n", metavar="new_secrete", type=str,
            help="New secrete key")
    add_arg("-c", action="store_true",
            help="New secrete key (interactively)")
    add_arg("-d", action="store_true",
            help="Delete credential of a site")
    add_arg("-i", metavar="filename", type=str,
            help="Import from a file. Merge with existing.")
    add_arg("-x", metavar="filename", type=str,
            help="Export to a plain text file")
    add_arg("site", metavar="site", type=str, nargs="?")
    add_arg("account", metavar="account", type=str, nargs="?")
    add_arg("password", metavar="password", type=str, nargs="?")
    return parser

def runCommand(args):
    # pylint: disable-msg=R0912
    if not args.k:
        s = readSecreteInput("Please input secrete key: ")
        if not s:
            raise Exception("Must provide secrete key")
        args.k = s
    creds = Credentials.loadCredentials(args.f, args.k)
    if args.c:
        if not creds or not creds.records:
            print("No credentials in store")
            return
        s = readSecreteInput("New secrete key: ")
        if not s:
            raise Exception("Must provide secrete key")
        creds.saveCredentials(args.f, s)
        print("Encrypted with new secrete key")
        return
    if args.n:
        # Use new secrete key
        if creds and creds.records:
            creds.saveCredentials(args.f, args.n)
            print("Encrypted with new secrete key")
        else:
            print("Credential is empty")
        return
    if args.x:
        # Export credentials to plain text file
        if creds and creds.records:
            creds.exportCredentials(args.x, prettyPrint=False)
            print("Credentials exported to %s" % args.x)
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
        if not creds:
            print("No credentials loaded")
        else:
            creds = creds.getCredentials(args.site)
            if creds:
                printTabulate(creds)
            else:
                print("Site not found")

    # pylint : enable-msg=R0912

def main():
    parser = initParser()
    args = parser.parse_args()
    runCommand(args)

if __name__ == "__main__":
    main()
