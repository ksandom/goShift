// Code for doing the encryption.

package main

func encode(dataIn []byte, length int, keyOffsets [32000]int, keyLength int, pos int, tables [8][256]byte) []byte {
    dataOut := make([]byte, length)

    for i := 0; i < length; i++ {
        charIn := dataIn[i]
        absPos := pos + i
        keyPos := absPos % keyLength

        offset := keyOffsets[keyPos]

        charOut := tables[offset][charIn]
        dataOut[i] = charOut
    }

    return dataOut
}


func generateTables(direction int) [8][256]byte {
    // There are only 7 possible offsets (1-7), because we mustn't leave the bits unchanged.
    var tables [8][256]byte

    for offset := 1; offset < 8; offset++ {
        effectiveOffset := offset * direction

        for value := 0; value<256; value++ {
            var bits [8]int = numberToBits(value)
            var shiftedBits [8]int = shiftBits(bits, effectiveOffset)
            var number byte = byte(bitsToNumber(shiftedBits))
            tables[offset][value] = number
        }
    }

    return tables
}

func keyToOffsets (key string) [32000]int {
    var output [32000]int
    var outPos int = 0
    var inKeyLength = len(key)

    for inPos := 0; inPos < inKeyLength; inPos++ {
        char := string(key[inPos])
        charBits := charToBits(char)

        output[outPos] = (bitsToNumber(subBits(charBits, 0, 2)) % 7) + 1
        outPos++

        output[outPos] = (bitsToNumber(subBits(charBits, 0, 2)) % 7) + 1
        outPos++
    }

    return output
}


