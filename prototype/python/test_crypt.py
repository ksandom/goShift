from crypt import Crypt
import numpy

def getKeyOffsets():
    thingsToTest = {}
    thingsToTest["a"] = numpy.array([2, 1])
    thingsToTest["abc"] = numpy.array([2, 1, 3, 1, 4, 1])
    thingsToTest["blah"] = numpy.array([3, 1, 5, 4, 2, 1, 1, 3])

    return thingsToTest

def getText():
    thingsToTest = []
    thingsToTest.append("blah")
    thingsToTest.append("A longer piece of text.")
    thingsToTest.append("A piece of text\nwith new lines and\rcarriage returns.")

    return thingsToTest

def test_keyToOffsets():
    crypt = Crypt()

    thingsToTest = getKeyOffsets()

    for key, offsets in thingsToTest.items():
        data = crypt.keyToOffsets(key)
        assert (data == offsets).all()

def test_generateTables():
    crypt = Crypt()

    encryptTables = crypt.generateTables(1)
    assert len(encryptTables) == 8

    decryptTables = crypt.generateTables(-1)
    assert len(decryptTables) == 8

def test_encode():
    crypt = Crypt()

    textToTest = getText()

    for stringKey in textToTest:
        for originalText in textToTest:
            keyOffsets = crypt.keyToOffsets(stringKey)
            encryptTables = crypt.generateTables(1)
            decryptTables = crypt.generateTables(-1)

            encrypted = crypt.encode(originalText, keyOffsets, len(keyOffsets), 0, encryptTables)
            decrypted = crypt.encode(encrypted, keyOffsets, len(keyOffsets), 0, decryptTables)

            assert decrypted.decode() == originalText
            assert len(decrypted) == len(originalText)
