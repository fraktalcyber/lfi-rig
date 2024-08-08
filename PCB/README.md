# XY2-100 driver board

This file contains remarks, notes and various things regarding the driver board and its assembly.

## Bill of materials

- **R1 & R2** - 1k Ohm 0603 resistor
- **R3** - 0 Ohm 0603 jumper
- **R4-R7** - 120 Ohm 0603 terminating resistors for the XY2-100 channels
- **J1** - Terminal Block, Metz Connect Type059 RT06303HBWC 1x3
- **J2 & J3** - Terminal Block, Metz Connect  Type059 RT06302HBWC 1x2
- **J4** - DB15 connector
- **PSU** - Traco Power TEN60-2423N, embedded power supply
- **U1** - Raspberry Pi Pico
- **U2** - LTC487CSW, 4 channel RS422/485 differential driver

## Remarks

- DB15 connector should be mounted on the opposite side of the PCB.
- Raspberry Pi Pico should be mounted on a pin header to allow for more cleareance under the USB cable
