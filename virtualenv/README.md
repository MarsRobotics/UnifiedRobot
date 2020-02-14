![ScreenShot dcmotor](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/RF310T11400.jpg)
![ScreenShot Nema](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/nema11.jpg)
![ScreenShot L298N](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/L298N.jpg)
![ScreenShot A4988](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/A4988.jpg)

Overview
--------------------------------------------
* Name: RpiMotorLib
* Title: Raspberry pi motor library.
* Description: A python 3 library for various motors and servos
to connect to a raspberry pi.
There are three categories in library.
Stepper motors , Dc Motors and Servos. The following is a list of tested parts

1. Stepper motor
    * Unipolar 28BYJ-48 Stepper motor controlled by ULN2003 driver module
    * Bipolar Nema 11 Stepper motor controlled by L298N H-Bridge Motor controller module.
    * Bipolar Nema 11 Stepper motor controlled by A4988 Stepper Motor Driver Carrier
    * Bipolar Nema 11 Stepper motor controlled by DRV8825 Stepper Motor Driver Carrier
    * Bipolar Nema 11 Stepper motor controlled by A3967 Stepper Motor Driver aka "easy driver v4.4"
    * Bipolar Nema 11 Stepper motor controlled by TB6612FNG Dual Motor Driver Carrier
    
2. DC motors
    * DC brushed motor controlled by L298N Motor controller module.
    * DC brushed motor controlled by a transistor.
    * DC brushed motor controlled by L9110S Motor controller module.
    * DC brushed motor controlled by DV8833 Motor controller module.
    * DC brushed motor controlled by TB6612FNG Dual Motor Driver Carrier
    
3. Servo 
    * Servo controlled by RPi.GPIO module PWM.
    * Servo controlled by pigpio library module PWM.
    
The end user can import this library into their projects
and then control the components with short snippets of code.
The library is modular so user can just import/use the section they need.


* Author: Gavin Lyons
* URL: https://github.com/gavinlyonsrepo/RpiMotorLib

Table of contents
---------------------------

  * [Overview](#overview)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Files](#files)
  * [Dependencies](#dependencies)
  * [Features](#features)
  * [Software Matrix](#software-matrix)
  * [See Also](#see-also)
  * [To Do](#to-do)
  * [Communication](#communication)
  * [History](#history)
  * [Copyright](#copyright)
  * [Contributers](#contributers)

Installation
-----------------------------------------------

The library was initially tested and built on a raspberry pi 3 model b,
Raspbian jessie 8.0 and python 3.4.2.
It was also tested for Python (3.5.3) and Raspbian stretch 9.9 .
Also for Windows 10 users See issue number 2 at project Github URL.

Make sure that python 3.5.3 and pip have been installed on your machine, then:

```sh
sudo pip install rpimotorlib
```

Usage
-------------------------------------------

In addition to library files a small script is installed
to display version and help information.

Run the information script by typing (for Linux systems)
RpiMotorScriptLib.py -[options]

Options list :

| Option          | Description     |
| --------------- | --------------- |
| -h  | Print help information and exit |
| -v  | Print version information and exit |

To learn how to use the Library in programs.
Go to features section below

Files
-----------------------------------------
rpiMotorLib files are listed below:

| File Path | Description |
| ------ | ------ |
| RPiMotorLib/RpiMotorLib.py |  stepper motor python library file |
| RPiMotorLib/rpiservolib.py | servo python library RPi.GPIO  PWM file |
| RPiMotorLib/rpi_pservo_lib.py | servo python library pigpio PWM file |
| RPiMotorLib/rpi_dc_lib.py  |    DC python motor library  file |
| RPiMotorLib/RpiMotorScriptLib.py | small script with meta data about library |
| documentation/*.md | 14 markdown library documentation files |
| test/*Test.py | 12 python test files |
| /usr/share/doc/RpiMotorLib/README.md | This help file |

Dependencies
-----------

1. RPi.GPIO 0.6.3

A module to control Raspberry Pi GPIO channels

This package provides a class to control the GPIO on a Raspberry Pi.

This should already be installed on most Raspberry Pis.

[Rpi.GPIO pypi page](https://pypi.python.org/pypi/RPi.GPIO)


2. pigpio 1.60-1

This Dependency is *Optional*, it is currently 
only used in one of the two servo control options.
See Features section below for details on why you would chose this.
pigpio is a library for the Raspberry which allows 
control of the General Purpose Input Outputs (GPIO).
See homepage for installation and setup instructions.

[Homepage](http://abyz.co.uk/rpi/pigpio/)


Features
----------------------

I have created separate help files in documentation folder to learn how to use library :


1. Servos:

NOTE: There are two different options for controlling the servo.
When using Rpi_GPIO option you may notice twitching at certain
delays and stepsizes. This is the result of the 
implementation of the RPIO PWM software timing. If the application requires
precise control the user can pick the pigpio library
which uses hardware based timing. The disadvantage being they must install 
another dependency.

[Servo RPi.GPIO PWM](Documentation/Servo_RPI_GPIO.md)

[Servo pigpio PWM](Documentation/Servo_pigpio.md)


2. Stepper Motors:

[28BYJ stepper motor ULN2003 ](Documentation/28BYJ.md)

[Nema 11 stepper motor L298N ](Documentation/Nema11L298N.md)

[Nema 11 stepper motor A4988 ](Documentation/Nema11A4988.md)

[Nema 11 stepper motor DRV8825 ](Documentation/Nema11DRV8825.md)

[Nema 11 stepper motor A3967](Documentation/Nema11A3967Easy.md)

[Nema 11 stepper motor TB6612FNG](Documentation/Nema11TB6612FNG.md)



3. DC Motors:

[L298N DC Motor](Documentation/L298N_DC.md)

[Transistor DC Motor](Documentation/Transistor_DC.md)

[L9110S DC Motor](Documentation/L9110S_DC.md)

[DRV8833 DC Motor](Documentation/DRV8833_DC.md)

[TB6612FNG DC Motor](Documentation/TB6612FNG_DC.md)

Test files used during development are in test folder of repo.
Example snippets are also available in some of the documentation files.


Software Matrix
--------------------------

There is a ODS file in the Documentation folder called Matrix,
which shows which class is used for which controller,
or consult the docstring of the appropriate python file. 


See Also
---------------------------

A lot of this code will work on similar components/modules but has not
been tested due to parts lacking.

For example:

The A4988/DRV8825 code **may** work with other *pololu* modules.
See this link for list of alternatives and drop-in replacements for this module.
[pololu product 1182](https://www.pololu.com/product/1182).

The Servo code should on most standard servos.

Most 4 pin bipolar stepper motors should work in place of Nema 11.


To Do
-----------------------
Add and test more components.
DRV8833 stepper motor test.

Communication
-----------------------
If you should find a bug or you have any other query,
please send a report.
Pull requests, components, suggestions for improvements
and new features welcome.
* Contact: Upstream repo at github site below or glyons66@hotmail.com
* Upstream repository: https://github.com/gavinlyonsrepo/RpiMotorLib


History
------------------
CHANGELOG.md is at repository in documentation section.

Copyright
-------------
Copyright (C) 2018 Gavin Lyons
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public license published by
the Free Software Foundation, see LICENSE.md in documentation section
for more details.


Contributers
--------------------
[Erez Levanon](https://github.com/erezlevanon)
