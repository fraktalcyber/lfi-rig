# xTool F1 G-Code

## High-level summary of the G-Code structure.

```
G0X55.500Y55.500
G1X59.500Y55.500S64F720000
G1X59.500Y59.500
G1X55.500Y59.500
G1X55.500Y55.500
```

The main G-commands the device uses are **G0** - galvo head movement with laser off and **G1** - galvo head movement with laser on. G0 and G1 move commands take the co-ordinates in millimeters with the 0,0 point being the top left corner of the stage. The G-Code should be done in a way that it is as center of the stage as possible or around coordinates X50.00Y50.00. This means the least deflection of the laser through the optical path and consequently more power and less optical distortions.

The first G1 command should append to the command additional parameters, namely **S** and **F**. Where S controls the laser power and F is the feedrate or the movement speed.

The laser power is given in percentages without decimal point, with the last digit being the decimal. 1000 being equal to 100% and numbers such as 64 being 6.4%

## G-Code file header

**Header in "processing"-mode**
```
G90           - Set absolute positioning
G0 F3000      - Set feedrate laser off to 50mm/s
G0 F180000    - Set feedrate laser off to 3000mm/s (max)
M4 S0         - Laser power on, power level to 0
G1 F180000    - Set feedrate laser on to 3000mm/s (max)
G0 X0 Y0      - Set galvanometer to 0,0 point
G21 (or G22)  - Select which laser to use, G21 = blue, G22 = IR
G90           - Set absolute positioning
```

**Header in "framing"-mode**
```
G0 F180000    - Set feedrate laser off to 3000mm/s (max)
M4 S0         - Laser power on, power level to 0
G1 F180000    - Set feedrate laser on to 3000mm/s (max)
M114 S1       - ?? Get current position or some kind of framing related setup parameter
G21           - Select which laser to use, G21 = blue, G22 = IR
G90           - Set absolute positioning
```

The G-Code files sent to the device always begin with the following header. These are used to setup the basic parameters for the galvanometer and lasers. Until there is better information, it is better to append this **as it is** to any G-Code files sent to the device. This is to ensure the device works as intended.



## G-Code file end

```
G90           - Set absolute positioning
G0 S0         - Laser power to 0 ??
G0 F180000    - Set feedrate laser off to 3000mm/s (max)
G1 F180000    - Set feedrate laser on to 3000mm/s (max)
M6 P1         - Stop lasering process, clean-up and power off the galvo and lasers
```

The G-Code files sent to the device always end with the following G-Code commands. Until there is better information, it is better to append this **as it is** to any G-Code files sent to the device. This is to ensure the device works as intended.

## xTool F1 G-Code commands

### G0 - Linear move, laser off
**Command structure - G0Xnn.nnnYnn.nnnSnnnnFnnnnn**

- X, X-coordinate in millimeters
- Y, Y-coordinate in millimeters
- S, laser power decimal number with single decimal, without decimal separator e.g 64 = 6.4 or 800 = 80.0
- F, Feedrate (movement speed). Calculated with the formula (speed in mm/s)*60 = feedrate e.g. 160mm/s => 160mm/s*60 = 9600

**Special cases**
G0 F180000 - ?? Setting of the maximum feedrate? As this is only used in the init section
G0 X0 Y0 - Position the galvanometer to its zero point


### G1 - Linear move, laser on
**Command structure - G0Xnn.nnnYnn.nnnSnnnnFnnnnn**

- X, X-coordinate in millimeters
- Y, Y-coordinate in millimeters
- S, laser power decimal number with single decimal, without decimal separator e.g 64 = 6.4 or 800 = 80.0
- F, Feedrate (movement speed). Calculated with the formula (speed in mm/s)*60 = feedrate e.g. 160mm/s => 160mm/s*60 = 9600

**Important Notes**
The first G1 command should always be used to set the feedrate. This can be done either by issuing a separate G1 command (see below). Or by setting it as part of the first G1 command such as G1X55.00Y55.00S800F6000 (Move the galvanometer head to point X55 Y55, turn the power to 80% and set the feedrate to 100mm/s.

**Special cases**
G1FnnnnnSnnnn - Set the feedrate for the laser on move commands, S-parameter should be set to 0 in this command


### G21 - Select Blue (455nm) laser
**Command structure - G21**

No parameters

### G22 - Select IR (1064nm) laser
**Command structure - G22**

No parameters

### G90 - Set absolute positioning
**Comand structure - G90**

No parameters

### M4 - Laser power on
**Command structure - M4 Snnnn**

- S, laser power decimal number with single decimal, without decimal separator e.g 64 = 6.4 or 800 = 80.0. **Suggested setting here 0**


### M6 - Stop the lasering process, power off everything
**Command structure - M6 P1**

- P, ?? Not sure what this means better to just send it as P1 until there is better understanding

### M114 - Some framing related setup command
**Command structure - M114 S1**

- S, ?? No clear understanding what this means
