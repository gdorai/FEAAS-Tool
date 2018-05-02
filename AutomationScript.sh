#!/bin/sh
# This is a shell script to automate the iOS backup process
mkdir Artifacts

# Install the utilities and backup services
brew unlink libimobiledevice
brew install --HEAD libimobiledevice
brew link libimobiledevice
brew install carthage	
pip3 install biplist
pip3 install reportlab

pwd
./DevicePairing.sh
