
function testSpeed
{
    key="$1"
    executable="$2"
    inFile="$3"
    if [ "$inFile" == '' ] ;then
        inFile="test/whatIsThis.jpg"
    fi

    intermediateFile="/tmp/e"
    decryptedFile="/tmp/d"

    echo "in=$inFile intermediate=$intermediateFile decrypted=$decryptedFile"

    time cat "$inFile" | "$executable" e "$key" > "$intermediateFile"
    time cat "$intermediateFile" | "$executable" d "$key" > "$decryptedFile"

    md5sum "$inFile" "$decryptedFile"

    rm "$intermediateFile" "$decryptedFile"
}
