package main

import (
    "os"
    "log"
    "io"
    "time"
)

func main() {
    // Variables
    var dSize int = 0
    var command string = ""
    var key string = ""
    var keyOffsets [32000]int
    var keyLength int

    parallelCount := 24

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

    start := time.Now()

    // Process the data.
    for {
        // Load up data to be worked on.
        finished := false
        results := make([]chan []byte, parallelCount)
        setLimit := 0

        for blockNumber := 0; blockNumber < parallelCount; blockNumber++ {
            results[blockNumber] = make(chan []byte)
            bufferIn := make([]byte, 1024)
            count, err := reader.Read(bufferIn)
            if count > 0 {
                //bufferOut :=
                go encode(bufferIn, count, keyOffsets, keyLength, dSize, tables, results[blockNumber])
                //l.Println(count, len(bufferOut))

                dSize += count
            }

            if err != nil {
                if err == io.EOF {
                    finished = true
                    break
                } else {
                    l.Println(err)
                }
            }
            setLimit++
        }

        // Wait for data, and write it out in order.
        for blockNumber := 0; blockNumber < setLimit; blockNumber++ {
            data := <- results[blockNumber]
            writer.Write(data)
        }

        // Make sure we cascade out.
        if finished {
            break
        }
    }

    // Calculate metrics.
    stop := time.Now()
    duration := stop.Sub(start)
    seconds := duration.Seconds()

    bytesPerSecond := float64(dSize) / seconds
    mBytesPerSecond := bytesPerSecond / (1024*1024)

    l.Printf("MB/s: %g", mBytesPerSecond)
}
