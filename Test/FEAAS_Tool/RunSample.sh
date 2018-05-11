#!/bin/sh
cd ../../
python3 ParserThermostat.py "Test/SampleInput/Thermostat" "Test/SampleOutput"
python3 ParserCamera.py "Test/SampleInput/Camera" "Test/SampleOutput"
