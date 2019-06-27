The Unified Robot
=================

This is all the code used to control the UPMars Robot as one unified repository

## Robot

The robot file acts as an API to interface with the robot at a higher level. Most of the code is ported from the Arduino Code that was formerly used to control the robot. This is the in-between the low-level direct component control and the high-level manual/autonomous control

---

## lib

The lib directory contains any libraries we created ourselves to interface with our various components. This deals with directly controlling our components and is thereby the lowest level. The list of components that we have a separate library for are as follows:

	1. Sabertooth Motor Controller: These run all the DC motors on the robot. The most notable are the motors which articulate and drive the wheels on the robot. All documentation can be found in the file. EE's have a note there too!

---

## Control

The control directory will contain the files used for manual control and autonomous control of the robot, separated appropriately. They will use the higher level Robot API to interface with the robot and is thus the highest level.
