#!/usr/bin/python3

import bme280

(chip_id, chip_version) = bme280.readBME280ID()
print(f"Chip ID : {chip_id}")
print(f"Version : {chip_version}")

temperature,pressure,humidity = bme280.readBME280All()

print(f"Temperature : {temperature}°C")
print(f"Pressure : {pressure}hPa")
print(f"Humidity : {humidity}%")
