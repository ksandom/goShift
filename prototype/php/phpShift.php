#!/usr/bin/php
<?php
/*
 A very basic prototype to solve:
 * Know what I want to achieve in go.
 * Compare performance of the end result.

 Usage:
 cat inputFile | ./phpShift.php method 'key' > outputFile

 Method
 * 'e' - Encrypt.
 * 'd' - Decrypt.

 Key can be a string. No length limit has been set, but there will be a limit somewhere. It's likely a long way past what is practical.

 */

### Get Args
$count=$argc;
if ($count < 3) die("Expected 2 parameters.\n");
$method=$argv[1];
$key=$argv[2];
$keyLength=strlen($key)*2;
$keyOffsets=keyToOffsets($key);

if ($method == "e") { // Encrypt (forwards).
    $tables=generateTables(1);
}
else { // Decrypt (backwards).
    $tables=generateTables(-1);
}

$start = microtime(true);

$stdIn = fopen('php://stdin', 'r');
$stdOut = fopen('php://stdout', 'w');
$pos=0;

$blockSize=4*1024;

while ($data=fread($stdIn, $blockSize)) {
    $encodedData=encode($data, $keyOffsets, $keyLength, $pos, $tables);
    $pos+=strlen($data);
    fwrite($stdOut, $encodedData);
}

fclose($stdIn);
fclose($stdOut);

$stop = microtime(true);
$elapsed = $stop - $start;
$bytesPerSecond = $pos / $elapsed;
$mBytesPerSecond = $bytesPerSecond / (1024 * 1024);

$stdError = fopen('php://stderr', 'w');
fwrite($stdError, "$mBytesPerSecond MB/s ($bytesPerSecond B/s).");
fclose($stdError);


function encode($dataIn, $key, $keyLength, $pos, $tables) {
    $dataLength=strlen($dataIn);
    $dataOut="";

    for ($i=0; $i<$dataLength; $i++) {
        $charIn=substr($dataIn, $i, 1);
        $absPos=$pos+$i;
        $keyPos=$absPos%$keyLength;

        $offset=$key[$keyPos];

        // Do the conversion.
        $charOut=$tables[$offset][ord($charIn)];
        $dataOut.=$charOut;
    }

    return $dataOut;
}

function charToBits($char) {
    return numberToBits(ord($char));
}

function numberToBits($inputValue) {
    $pos=7;
    $output=array();

    for ($dividor=128; $dividor>0.5; $dividor=$dividor/2) {
        $testNumber=$inputValue/$dividor;

        if ($testNumber >= 1) {
            $inputValue = $inputValue - $dividor;
            $output[$pos] = 1;
        } else $output[$pos] = 0;

        # echo "$pos: d=$dividor i=$inputValue t=$testNumber\n";

        $pos--;
    }

    return $output;
}

function bitsToNumber($bits) {
    $pos=0;
    $output=0;

    for ($multiplier=1; $multiplier<256; $multiplier=$multiplier*2) {
        if (!isset($bits[$pos])) break;

        if ($bits[$pos] == 1) {
            $output+=$multiplier;
        }

        $pos++;
    }

    return $output;
}

function bitsToChar($bits) {
    return chr(bitsToNumber($bits));
}

function shiftBits($bits, $shiftBy) {
    $output=array();

    for ($x=0; $x<8; $x++) {
        $destination=$x+$shiftBy;
        if ($destination>7) $destination-=8;
        if ($destination<0) $destination+=8;

        $output[$destination]=$bits[$x];
    }

    return $output;
}

function subBits($bits, $start, $stop) {
    $output=array();
    $pos=0;

    for ($i=$start; $i<=$stop; $i ++) {
        $output[$pos]=$bits[$i];
        $pos++;
    }

    return $output;
}

function keyToOffsets($key) {
    $output=array();
    $outPos=0;
    $inKeyLength=strlen($key);

    for ($inPos=0; $inPos<$inKeyLength; $inPos++) {
        $char=substr($key, $inPos, 1);
        $output[$outPos]=(bitsToNumber(subBits(charToBits($char), 0, 2)) % 7) + 1;

        $outPos++;
        $output[$outPos]=(bitsToNumber(subBits(charToBits($char), 2, 4)) % 7) + 1;
        $outPos++;
    }

    return $output;
}

function generateTables($direction) {
    /*
     There are only 7 possible offsets (1-7), because we mustn't leave the bits unchanged.
     */
    $tables=array();

    for ($offset=1; $offset<8; $offset++) {
        $table=array();
        $effectiveOffset=$offset*$direction;
        for ($value=0; $value<256; $value++) {
            $bits=numberToBits($value);
            $shiftedBits=shiftBits($bits, $effectiveOffset);
            $table[$value]=chr(bitsToNumber($shiftedBits));
        }

        $tables[$offset]=$table;
    }

    return $tables;
}


?>
