from bits import *
import sys

class Crypt():
    def __init__(self):
        """
        TODO
        * encode
        * generateTables
        """

        self.bits = Bits()

    def encode(self, dataIn, key, keyLength, pos, tables):
        dataLength = len(dataIn)
        dataOut = bytearray()

        for i in range(0, dataLength):
            charIn = dataIn[i:i+1]
            absPos = pos + i
            keyPos = absPos % keyLength

            offset = key[keyPos]

            # Do the conversion.
            charValue=ord(charIn)
            charOut = tables[offset][charValue]
            #dataOut[i] = charOut
            dataOut.append(charOut)

        return dataOut

    def keyToOffsets(self, key):
        output = []
        inKeyLength = len(key)

        for pos in range(0, inKeyLength):
            char = key[pos:pos+1]

            output.append(self.charToOffset(char, 0, 2))
            output.append(self.charToOffset(char, 2, 4))

        return output

    def charToOffset(self, char, start, stop):
        bits = self.bits.charToBits(char)
        subBits = self.bits.subBits(bits, start, stop)
        number = self.bits.bitsToNumber(subBits)

        return (number % 7) +1

    def generateTables(self, direction):
        tables = []
        tables.append([])

        for offset in range(1, 8):
            table = []
            effectiveOffset = offset * direction
            for value in range(0, 256):
                bits = self.bits.numberToBits(value)
                shiftedBits = self.bits.shiftBits(bits, effectiveOffset)
                number = self.bits.bitsToNumber(shiftedBits)
                #table.append(chr(number))
                #table.append(number.to_bytes(1))
                table.append(number)

            tables.append(table)

        return tables
