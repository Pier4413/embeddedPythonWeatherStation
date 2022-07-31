# Embedded part of the weather station

This part is in python and is intended to work with sensors

See : 
 - [Data Server (Node.js/Mongo.db)](https://github.com/Pier4413/dataServerWeatherStation)
 - [Web Interface (Vue.js)](https://github.com/Pier4413/webInterfaceWeatherStation.git)

## Config file

### Options 

There is seven options for this program :

 - --help : print the help
 - --settings : providing the path of the ini config file (default : ./conf/settings.ini)
 - --env : providing the path of a .env file (default : ./conf/.env)
 - --log_level : The log level. A lower level include the higher ones
   - DEBUG : 10
   - INFO : 20
   - WARN : 30
   - ERROR : 40
 - --log_info_file : To log all infos (default : None)
 - --log_crit_file : To log error infos (default : None)
 - --log_console : To log all infos in the console (default : 0)
  
## INI Config file

The ini config file can contains to parametrized the application, those values have default provided here :

```
[general]
delay = 300 # Used to delay the read of sensors
is_simulated = False # Used in dev to simulated the sensors

[bme280]
has_to_read=true

[gy271]
has_to_read=true

[hw477]
has_to_read=true
```

If you copy from here don't forget to delete the comments at the end of the lines

Each has to read is for the sensors. If has_to_read the default values of the sensors will be 0.
## .env file

The .env file is not necessary as values of this file are read has environment variables they can be provided by other means (like in the shell directly)

However whatever the mean this two variables have to be sets :

  - API_KEY : The api key to connect to data server
  - API_SERVER_URL : The fully qualified URL of the server (i.e with protocol (http or https) and port)
  - BME280_ADDRESS : The address of the BME280 for pressure, humidity and temperature
  - GY271_ADDRESS : The address of the GY271 for the compass
  - HW477_ADDRESS : The address of the HW477 hall effect sensor
  - MAGNETS_NUMBER : The number of magnets used in the anemometer