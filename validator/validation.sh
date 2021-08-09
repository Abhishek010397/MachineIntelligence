#!/bin/bash

check_python=$(python3 -V)
if [ $check_python == "3.8.10" ]
then
  echo "Python Version is $check_python"
else
  echo "Installing Latest Python"
  sudo apt install python3 idle3
  
check_pip=$(pip3 --version | awk '{print $2}')
if [ $check_pip == "21.1.3" ]
then
  echo "Pip Version is $check_pip"
else 
  echo "Installing Latest Pip"
  sudo apt-get install python3-pip