---
title: Module Schematic
---

## Overview

This schematic is my inital version of the HMI system. It has dual joystick controlls, along with a OLED. This inital design is very simple at this stage and will likely have to get addjusted to better suit the teams final design. The board will utalize power either from the usb or the onboard barrewljack socket. A battery system will likely be added in the future. This system will talk to the controller board via LAN or Bluetooth. The onboard OLED and LEDs will provide status updates and will notify the user of what the sub is sensing. Through the menu navigation the user can also adjust settings while the sub is active. The user will simply engage one of the Joystiks center buttons and enable the other to navigate the menu system. 


![schematic](schematic.png){style width:"350" height:"300;"}
**Figure ##:** Showing the schematic.


## Resouces

The schematic as a PDF download is available [*here*](schematicSB.pdf), and the Zip folder of the project [*here*](egr314-subsystem-schematic-design-sbV2.zip).


## Final Notes

As stated in the componet selection, the power requlator was set up wrong. I also didn't end up utalizing any diodes due to not finding any in my footprint size. I didn't notice this before but I am very glad that I missed regulating one of the incoming power from one of the 8 pin connectors. That simple oversight allowed me to have a plug and play method of giving my self 3.3 V from an external power requlator. 