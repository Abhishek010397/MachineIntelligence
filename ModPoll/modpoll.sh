#!/bin/bash

echo "Register Number: $1";
echo "IP Address : $2";
echo "Your Value: $3";

./modpoll -m tcp  -r $1 $2 $3

