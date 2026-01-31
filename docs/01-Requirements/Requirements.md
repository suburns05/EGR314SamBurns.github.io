---
title: Module's Requirements
---

## Module Requirements
My subsystem is the Human Machine Interface (HMI). While this is critical to our product, being a mini submarine, we don't expect the user to be in the water with it. Thats where my subsystem is implimented. Fundimentally its the controller to any traditional RC vechicle. It will cominicate with the onboard controller board and possibly cominicate with any portable device that is also connected to the submarine.See the table below for more detail. 

| **Requirement Description** | **Measure of<br> Threshold** | **Target<br>Measure** |**Stretch<br>Requirement<br>(Y-N)**|
|-----------------------------| ----------------- | ----------------- | :-----: |
| Surface mounted, 3.3V switching power regulatore | 3.2 Volts | 3.3 Volts | No |
| Surface mounted microcontroller | 1 PIC or ESP | 8-bit PIC | No |
| Wireless Communication | Able to send or receive a Wi-Fi data | Send and receive Wi-Fi Data to MQTT | Yes |
|*Rest are items your modules needs to support the task you are covering for the team's device.* | --- | --- | **NO** |


<!-- The objective of this assignment is to start to critically think and break down what your module will be required to do before moving too far forward in the development.

In your Individual Datasheet web-report, in the Project Requirements section, add/modify the following report components:

Edit the text provided in the template so that it includes some written context related to your objective on why this table is here and what it is about. 

-done

PENDING

Edit the table listings to include each requirement as a description, along with the minimum measure level to not be a complete failure, the target measurement, and whether it is a stretch requirement. (See the Individual datasheet template for an example.) 
This table should cover the major design-concept constraints for your module. Things like:
How are you powering the microcontroller?
What microcontroller?
Do you need a serial sensor?
Do you need a motor? What type?
If you have a motor, do you need a motor driver or a different power regulator?
Should cover every feature you are supporting in the overall team design.
Submit your datasheet URL to the Product Requirement page, along with a PDF for ease of grading/backup. -->