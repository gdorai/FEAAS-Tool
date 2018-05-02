#!/bin/sh
foo="$(idevicepair pair)"
#echo $foo
if [[ $foo == SUCCESS* ]];
then
	echo iOS Device Paired with Computer
    # read -p "Press enter to continue"

    # Permanent code. Uncomment Later.
    # idevicebackup2 backup Artifacts/

    # Not sure whether this encryption off is really working as expected.
    # idevicebackup2 -i encryption off backup .

    BACKUPPATH="$(pwd)/$(find Artifacts/ -maxdepth 1 -type d  | awk '{if(NR>1)print}')/"
    echo “$BACKUPPATH”

    #BACKUPPATH is temporarily replaced with my author's file path.
    BACKUPPATH="/Users/gokila/Library/Application Support/MobileSync/Backup/8c75768ed100ac467a83e7a8684a392e3b3b671a"
    echo “$BACKUPPATH”
    python3 ParserThermostat.py "${BACKUPPATH}"
    # python3 ParserCamera.py "${BACKUPPATH}"
else
	echo Connect the iOS device and hit trust
    read -p "Press enter to continue"
	./DevicePairing.sh
fi

