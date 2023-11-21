import numpy

class Bits():
    def __init__(self):
        pass

    def charToBits(self, char):
        return self.numberToBits(ord(char))

    def numberToBits(self, number):
        pos = 7
        output = numpy.array([0, 0, 0, 0, 0, 0, 0, 0])
        dividor = 128

        while dividor > 0.5:
            testNumber = number / dividor

            if testNumber >= 1:
                number -= dividor
                output[pos] = 1

            dividor /= 2
            pos -= 1

        return output

    def bitsToNumber(self, bits):
        pos = 0
        output = 0
        multiplier = 1
        inputLength = len(bits)

        while multiplier < 256:
            if not pos < inputLength:
                break

            if bits[pos] == 1:
                output += multiplier

            pos += 1
            multiplier *= 2


        return output

    def bitsToChar(self, bits):
        return chr(self.bitsToNumber(bits))

    def shiftBits(self, bits, shiftBy):
        output = numpy.array([0, 0, 0, 0, 0, 0, 0, 0])

        for pos in range(0, 8):
            outPos = pos + shiftBy

            if outPos > 7:
                outPos -= 8

            if outPos < 0:
                outPos += 8

            output[outPos] = bits[pos]

        return output

    def subBits(self, bits, start, stop):
        stopBoundary = stop + 1
        output = []
        numberOfBits = len(bits)


        for pos in range(start, stopBoundary):
            if pos >= numberOfBits:
                break

            output.append(bits[pos])

        return output
