from crypt import *
import time
import sys

class PyShift():
    def __init__(self, method, key):
        self.crypt = crypt = Crypt()
        self.bufferSize = 1024

        # User config.
        self.method = method
        self.key = key

        # Prepare encryption tables - This speeds up encryption/decryption.
        if self.method == "e":
            direction = 1
        else:
            direction = -1

        self.tables = self.crypt.generateTables(direction)

        # Prepare key.
        self.keyOffsets = self.crypt.keyToOffsets(self.key)
        self.keyLength = len(self.keyOffsets)

        # For later statistics.
        self.totalDataLength = 0
        self.startTime = self.now()

    def doStdInOut(self):
        pos = 0

        dataIn = sys.stdin.buffer.read(self.bufferSize)
        while dataIn:
            encodedData = self.crypt.encode(dataIn, self.keyOffsets, self.keyLength, pos, self.tables)

            sys.stdout.buffer.write(encodedData)
            sys.stdout.flush()

            dataLength = len(dataIn)
            pos += dataLength
            dataIn = sys.stdin.buffer.read(self.bufferSize)

    def now(self):
        return time.time() * 1.0

    def out(self, line):
        print(line, file=sys.stderr)
