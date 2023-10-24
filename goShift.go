package main

import (
    "os"
    "log"
    "io"
)

func main() {
    // Variables
    var dSize int = 0
    var command string = ""
    var key string = ""
    var keyOffsets [32000]int
    var keyLength int

    var tables [8][256]byte

    // Output is likely redirected to a file. So anything that we need to send to the user needs to go to stderr.
    l := log.New(os.Stderr, "", 0)

    // Check that we have enough parameters.
    if len(os.Args) < 3 {
        l.Println("Not enough parameters. Expected command and key. Eg:")
        l.Println("goShift e \"What a nice key\"")
        l.Println("\"e\" is encrypt. \"d\" is decrypt.")
        os.Exit(1)
    }

    // Assign user input.
    command = os.Args[1]
    key = os.Args[2]

    // Figure out the key.
    keyOffsets = keyToOffsets(key)
    keyLength = len(key) * 2

    // Display configuration.
    l.Printf("Command: %s", command)
    l.Printf("Key: %s", key)
    l.Printf("Virtual key length: %d", keyLength)

    // Build the map.
    if command  == "e" {
        tables = generateTables(1)
    } else {
        tables = generateTables(-1)
    }


    // Open streams.
    reader := io.Reader(os.Stdin)
    writer := io.Writer(os.Stdout)

    // Process the data.
    for {
        bufferIn := make([]byte, 1024)
        count, err := reader.Read(bufferIn)
        if count > 0 {
            bufferOut := encode(bufferIn, count, keyOffsets, keyLength, dSize, tables)
            l.Println(count, len(bufferOut))
            writer.Write(bufferOut)

            dSize += count
        }

        if err != nil {
            if err == io.EOF {
                break
            } else {
                l.Println(err)
            }
        }
    }
}


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



func subBits(bits [8]int, start int, stop int) [8]int {
    var output [8]int
    var pos = 0

    for i := start; i < stop; i++ {
        output[pos] = bits[i]
    }

    return output
}

func numberToBits(number int) [8]int {
    var pos int = 7
    var output [8]int

    for divider := 128; divider >= 1; divider=divider/2 {
        testNumber := number/divider

        if testNumber >= 1 {
            number = number - divider
            output[pos] = 1
        } else {
            output[pos] = 0
        }

        pos--
    }

    return output
}

func bitsToNumber(bits [8]int) int {
    var output int = 0
    var pos int = 0

    for multiplier := 1; multiplier < 256; multiplier *= 2 {
        if bits[pos] == 1 {
            output += multiplier
        }

        pos++
    }

    return output
}

func charToBits(char string) [8]int {
    return numberToBits(int(char[0]))
}

func shiftBits(bits [8]int, offset int) [8]int {
    var output [8]int

    for x := 0; x < 8; x++ {
        destination := x + offset
        if destination > 7 {
            destination -= 8
        }
        if destination < 0 {
            destination += 8
        }

        output[destination] = bits[x]
    }

    return output
}
