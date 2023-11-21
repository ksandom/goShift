import pytest

from bits import Bits
import numpy

def getNumBits():
    thingsToTest = {}
    thingsToTest[0] = numpy.array([0, 0, 0, 0, 0, 0, 0, 0])
    thingsToTest[1] = numpy.array([1, 0, 0, 0, 0, 0, 0, 0])
    thingsToTest[2] = numpy.array([0, 1, 0, 0, 0, 0, 0, 0])
    thingsToTest[4] = numpy.array([0, 0, 1, 0, 0, 0, 0, 0])
    thingsToTest[8] = numpy.array([0, 0, 0, 1, 0, 0, 0, 0])
    thingsToTest[16] = numpy.array([0, 0, 0, 0, 1, 0, 0, 0])
    thingsToTest[32] = numpy.array([0, 0, 0, 0, 0, 1, 0, 0])
    thingsToTest[64] = numpy.array([0, 0, 0, 0, 0, 0, 1, 0])
    thingsToTest[128] = numpy.array([0, 0, 0, 0, 0, 0, 0, 1])
    thingsToTest[7] = numpy.array([1, 1, 1, 0, 0, 0, 0, 0])

    return thingsToTest

def getCharBits():
    thingsToTest = {}

    thingsToTest["a"] = numpy.array([1, 0, 0, 0, 0, 1, 1, 0])
    thingsToTest["b"] = numpy.array([0, 1, 0, 0, 0, 1, 1, 0])
    thingsToTest["c"] = numpy.array([1, 1, 0, 0, 0, 1, 1, 0])
    thingsToTest["A"] = numpy.array([1, 0, 0, 0, 0, 0, 1, 0])
    thingsToTest["B"] = numpy.array([0, 1, 0, 0, 0, 0, 1, 0])
    thingsToTest["C"] = numpy.array([1, 1, 0, 0, 0, 0, 1, 0])

    return thingsToTest

def test_numberToBits():
    bits = Bits()

    thingsToTest = getNumBits()

    for inputValue, expectedResult in thingsToTest.items():
        data = bits.numberToBits(inputValue)
        assert (data == expectedResult).all()
        assert len(data) == 8

def test_bitsToNumber():
    bits = Bits()

    thingsToTest = getNumBits()

    for expectedResult, inputValue in thingsToTest.items():
        data = bits.bitsToNumber(inputValue)
        assert data == expectedResult

def test_charToBits():
    bits = Bits()

    thingsToTest = getCharBits()
    for dataChar, dataBits in thingsToTest.items():
        dataReturned = bits.charToBits(dataChar)
        assert (dataReturned == dataBits).all()
        assert len(dataReturned) == 8

def test_bitsToChar():
    bits = Bits()

    thingsToTest = getCharBits()
    for dataChar, dataBits in thingsToTest.items():
        dataReturned = bits.bitsToChar(dataBits)
        assert dataReturned == dataChar

def test_subBits():
    bits = Bits()

    originalBits = numpy.array([1, 1, 0, 0, 0, 1, 1, 0])

    expectedBits = numpy.array([1, 1, 0, 0])
    actualBits = bits.subBits(originalBits, 0, 3)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([1, 0, 0, 0])
    actualBits = bits.subBits(originalBits, 1, 4)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([0, 0, 0, 1])
    actualBits = bits.subBits(originalBits, 2, 5)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([0, 0, 1, 1])
    actualBits = bits.subBits(originalBits, 3, 6)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([0, 1, 1, 0])
    actualBits = bits.subBits(originalBits, 4, 7)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([1, 1, 0])
    actualBits = bits.subBits(originalBits, 5, 8)
    assert (actualBits == expectedBits).all()

def test_shiftBits():
    bits = Bits()

    originalBits = numpy.array([1, 1, 0, 0, 0, 1, 1, 0])

    expectedBits = numpy.array([1, 1, 0, 0, 0, 1, 1, 0])
    actualBits = bits.shiftBits(originalBits, 0)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([0, 1, 1, 0, 0, 0, 1, 1])
    actualBits = bits.shiftBits(originalBits, 1)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([1, 0, 1, 1, 0, 0, 0, 1])
    actualBits = bits.shiftBits(originalBits, 2)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([1, 0, 0, 0, 1, 1, 0, 1])
    actualBits = bits.shiftBits(originalBits, -1)
    assert (actualBits == expectedBits).all()

    expectedBits = numpy.array([0, 0, 0, 1, 1, 0, 1, 1])
    actualBits = bits.shiftBits(originalBits, -2)
    assert (actualBits == expectedBits).all()
