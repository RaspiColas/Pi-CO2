# Pi-CO2

This is a program to monitor CO2 level in a room via a Raspberry Pi.

It retrieves CO2 value from a sensor MH-Z19 connected to the Raspberry Pi, displays its value on an LCD screen, and records all data collected to files for further analysis and retrieval from other SBC.

It requires:
- A pi (zero)
- A Z19 CO2 sensor connected to the Pi
- An LCD display connected to the Pi
- Optional: a housing (eg, 3D printed)

Other Py scripts required:
- co2_lib.py : to read the CO2 level and save it in a file
- lcd_display_lib.py: to display a value on an LCD display screen
- Optional: send_sms_lib.py to send an alert by SMS if the data exceeds a given value
- co2.conf: configration data in Parser format

The script has to be put in a crontab for being activated regularly (eg, every 1 hour) to monitor the data.

Source: https://monitorserviceatelierueda.blogspot.com/2018/11/how-to-measure-room-co2-concentration.html
