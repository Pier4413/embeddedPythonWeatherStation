#!/bin/bash

git submodule update --recursive --init
cp -r elements/*/*.py dist/opt/weather_station
cp -r modules/*/*.py dist/opt/weather_station
cp -r workers/*.py dist/opt/weather_station
cp -r main.py dist/opt/weather_station
cp requirements.txt dist/DEBIAN 
dpkg-deb -b dist weather_station.deb