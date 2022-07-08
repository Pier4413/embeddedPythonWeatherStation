#!/bin/bash

git submodule update --recursive --init
cp -r classes/ dist/opt/weather-station
cp -r elements/ dist/opt/weather-station
cp -r modules/ dist/opt/weather-station
cp -r workers/ dist/opt/weather-station
cp -r main.py dist/opt/weather-station
cp requirements.txt dist/opt/weather-station
cp embedded.txt dist/opt/weather-station
dpkg-deb -b dist weather-station.deb
