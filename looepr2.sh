#!/bin/bash

posters=$(ls -A "/home/steven/documents/programming/orindi/1_reference/emails")

for p in $posters;do
    #echo "$p"
    cat "/home/steven/documents/programming/orindi/1_reference/emails/$p" | python3 ./orindi_parse.py 
done



