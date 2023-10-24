# goShift

A basic inline bit shifter for pseudo encryption.

WARNING: This is not secure, and is easy to crack (entropy is very low). It's intended only as a proof of concept and an exercise for me to learn Go.

## How it works

* The provided key splits each character of the key into 2 3 bit offsets.
    * Offsets 0 and 8 are not allowed.
* As we iterate over the bytes of the input stream, we iterate over the offsets, and loop when we run out of offsets.
* The offsets represent how many places to shift the bits of each byte,
* The bits that fall off the end of the byte rotate back to the start.

## Using it

### Build

```
go build
```

### Running it

#### Syntax

```
cat fileIn.txt | ./goShift command key > fileOut.txt
```

`command` is one of

* `e` - Encrypt.
* `d` - Decrypt.

`key` is a quoted string. Here are some examples:

* `"OMG This is such a secure encryption key!1!111"`
* `"WHOOPS! I forgot to turn off the bath taps before leaving the house this morning."`
* `"Nah, it's totally fine. My goldfish will drink it all up."`
* `"Ummm... Dude, that's not how goldfish work."`
* `"Shut up"`

#### Example 1 - To the terminal

This will dump the encrypted data straight into the terminal. This is not useful.

```
echo "Hello" | ./goShift e "A really nice key."
```

#### Example 2 - To a file

Let's send the same data to a file.

```
echo "Hello" | ./goShift e "A really nice key." > encryted.txt
```

#### Example 3 - Decrypt text from a file

Let's decrypt what we encrypted.

```
cat encryted.txt | ./goShift d "A really nice key."
```

#### Example 4 - Decrypt text from a file to a file

Let's decrypt what we encrypted.

```
cat encryted.txt | ./goShift d "A really nice key." > decrypted.txt
```

## Performance

I originally prototyped the algorithm in PHP so that I had fewer things to debug in Go as I was learning it. This therefore created an interesting question: How does the performance compare between the two languages using almost identical implementations?

Here are the tests encrypting, and decrypting a 480MB video.

### Performance in PHP

```
$ ./test/testSpeedPHP /tmp/test.mkv
in=/tmp/test.mkv intermediate=/tmp/e decrypted=/tmp/d
9.0293164764576 MB/s (9467924.553618 B/s).
real    0m53.174s
user    0m52.728s
sys     0m0.891s
8.6207558922402 MB/s (9039517.7304616 B/s).
real    0m55.695s
user    0m55.125s
sys     0m1.033s
cac98da1464113f3e766a31b2dbcfc4b  /tmp/test.mkv
cac98da1464113f3e766a31b2dbcfc4b  /tmp/d
```

### Performance in Go

```
$ ./test/testSpeedGo /tmp/test.mkv
in=/tmp/test.mkv intermediate=/tmp/e decrypted=/tmp/d
Command: e
Key: A really SECURE key that no one will guess.
Virtual key length: 86
MB/s: 46.78053827639643

real    0m10.262s
user    0m8.872s
sys     0m2.140s
Command: d
Key: A really SECURE key that no one will guess.
Virtual key length: 86
MB/s: 45.9091558475526

real    0m10.457s
user    0m9.073s
sys     0m2.154s
cac98da1464113f3e766a31b2dbcfc4b  /tmp/test.mkv
cac98da1464113f3e766a31b2dbcfc4b  /tmp/d
```
