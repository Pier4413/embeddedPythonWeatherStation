# Embedded part of the weather station

This part is in python and is intended to work with sensors

See : 
 - https://github.com/Pier4413/dataServerWeatherStation
 - https://github.com/Pier4413/webInterfaceWeatherStation.git

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

[anemometer]
magnets = 4 # The number of magnets on one turn of the anemometer
step_time = 0.1 # A time to pause the read of the sensor to avoid reading multiple times the same passage
delay = 10 # The given time to read the anemometer
sensor_radius = 0.1 # The radius on which the sensor is placed from the center of the anemometer
```

If you copy from here don't forget to delete the comments at the end of the lines

## .env file

The .env file is not necessary as values of this file are read has environment variables they can be provided by other means (like in the shell directly)

However whatever the mean this two variables have to be sets :

  - API_KEY : The api key to connect to data server
  - API_SERVER_URL : The fully qualified URL of the server (i.e with protocol (http or https) and port)