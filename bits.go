// Functions for doing various bit conversions/manipulations.

package main

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
