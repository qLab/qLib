#!/bin/bash

RANGE=`git log --date-order --tags --simplify-by-decoration --format="%d" | grep -o -E "v[0-9]+\.[0-9]+\.[0-9]+" | head -2 | tac`
RANGE=${RANGE//$'\n'/...}

echo -e "\nCHANGES: qLib -- $RANGE\n---"

#git log --pretty=format:"%ci: %s" $RANGE | grep "#" | grep -vi "merged"
git log --pretty=format:"%ci: %s" $RANGE | grep -vi "merged"

echo "---"
