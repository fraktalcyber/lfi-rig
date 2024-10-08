# Off-the-shelf Laser Fault Injection rig, lfi-rig v2
Don't want to start toying with soldering or getting PCBs manufactured, but have a bit more money to spend. For 1449eur (VAT incl) you can buy a very capable LFI rig that can be used to both decap chips and perform laser fault injection without any hardware modifications. 

**Some warnings:** You will be talking to the device directly, this may result in permanently breaking the device. This may happen by sending incorrect commands or badly formatted G-Code files. As you are directly controlling the device and its laser power, the same precautions apply as with our rig v1, namely cover your eyes and vent fumes. Thoroughly read this write-up, as well as, the information relating to the G-Code before attempting this.

![xTool F1, image (c) xTool](/Other/Images/xtool-f1.png)

## xTool F1
If the xTool marketing is to trust this device is Fastest Portable Laser Engraver with IR + Diode Laser. Or maybe to rephrase Fastest Portable Laser Fault Injection and Decapping rig. For a slight bit more money, this offers many improvements over our previously introduced DIY budget rig. 

- No hardware modifications necessary that would void warranty. Yes, lfi rig with 24 month warranty :D 
- Electronically adjustable, auto calibrating Z-axis focus
- 2 lasers, same spec 2W (1064nm) IR laser as in our rig v1 + a 10W (455nm) blue laser
- Control using G-Code files that can be easily shared
- Even faster and more precise newer tech galvanometer
- Enclosed design with outlet that can be attached to a fume extractor
- Laser safe (at least supposedly) enclosure

We pitted the xTool F1 against our rig v1 and here are the main differences:

**lfi-rig v1 vs xTool F1**
- **Price:** 500eur vs 1449eur
- **Laser Decapping accuracy with IR laser:** Very similar provided you have the focus nailed for v1. xTool makes the focus setting and repeatability much better.
- **Laser fault injection accuracy:** Very similar provided you have the focus nailed for v1. Again, xTool makes this much easier to get right.
- **Speed:** xTool is much faster. Hard to give absolute figures but 10x is probably not far off.
- **Ease of use and setup:** xTool requires absolutely nothing special, just install the drivers and you are good to go. You can use anything from curl to our Python scripts *(WIP)* to use it. You are up and running in less than 5 minutes
- **HW hacking scene credibility points:** v1 no questions asked. xTool is like turning up into a tuning car meetup in a grey VW Golf.

## The setup
xTool F1 has few ways of connecting to it, you can use the USB-C port on the side of the device, or Wi-Fi. In either case the device can be reached via HTTP API on port 8080. If using USB-C you will need to install the xTool USB-Ethernet driver (generic CH340 drivers might work too), after which the device is presented as USB-Ethernet interface on the host computer. xTool [support website](https://support.xtool.com/product/2) has all the necessary details. It is good idea to do a smoke test, pun intended, with the official software just to verify the device works as intended. As the setup process has a fair amount of parameters it is suggested that you do perform the initial machine setup using the XCS desktop or mobile application. This also verifies the device is running the most recent firmware version.


## Talking to xTool F1
To control the device there are four main commands you will need. Before you get started, verify the device responds. The easiest way to do this is via browser. Over plain HTTP, access this URL: ip:8080/system?action=version_v2 This should give you a JSON-formatted output showing various machine related information. If this works, you are good for the next steps.

**The main commands**
- **Focus control POST-request:** *ip:8080/focus/control* - This adjust the Z-axis and the focus point of the laser
- **Framing POST-request:** *ip:8080/processing/upload?gcodeType=frame&fileType=txt&autoStart=1&loopPrint=1* - This will run the device in framing mode scanning whatever G-Code you give it. This will only end with the Stop command
- **Lasering POST-request:** *ip:8080/processing/upload?gcodeType=processing&fileType=txt&taskId=1234* - This will run the device in lasering mode
- **Stop POST-request:** *ip:8080/processing/stop* - This command will stop whatever the device is doing, whether framing or lasering


## Autohoming or auto calibration
Autohoming of the device can be perfomed by sending a following HTTP post message:

```
URL: POST ip:8080/focus/control
Payload: {"action":"goTo", "autoHome":1, "z":23.5, "stopFirst":1, "F":300}
```

What this does is, it sets the Z-axis zero point to the surface of the bottom plate of the device. Z equals 23.5mm which is the height at which the base plate is sitting from the desk surface.

It is a good idea to always run this first to ensure Z-axis accuracy when performing the actual lasering. If using the baseplate the Z-height should be calculated 23.5mm + the height required by your chip or PCB.

## Z-axis focus
With the Z-axis zero point set to the bottom plate any further Z-axis adjustments can be made in reference to the zero point (23.5mm). The same command can be used to adjust the Z-axis focus. For example setting the focus point to 1.23mm would result in z-parameter to be (23.5mm+1.23mm = 24.73mm)

```
URL: POST ip:8080/focus/control
Payload: {"action":"goTo", "autoHome":1, "z":24.73, "stopFirst":1, "F":300}
```

## Framing Mode- This can be used for LFI
Framing is by default using the blue laser on the device with just lower power to show the outline of the shape you want. Now, as we are sending raw G-Code to the device it is possible to accidentally set the laser power high enough to actually start cutting/engraving whatever you have underneath. **So make sure the power is set to max 0.064 (so 6.4%). If you just want to do framing.** This is the default and safe setting used by xTools own XCS studio software.

**As we have complete control over the G-Code, this functionality can be used to run the device in a looping laser fault injection mode.** To achieve this change the laser to IR (using G-Code G22) and set the power and feedrate to your liking. The process will continue indefinitely until you run the stop command.

```
URL: POST ip:8080/processing/upload?gcodeType=frame&fileType=txt&autoStart=1&loopPrint=1
Payload: Text format G-Code file with some additions
```

Notes on the URL parameters. If you want the framing to start only when you press the rotary button on the side of the device **(this is a good idea if you use the IR laser)**, leave the autoStart-parameter off. loopPrint-parameter is controlling whether the device will keep on looping the same G-Code file or just run it once. 

**Important notes for the G-Code**:
xTool seems to use slightly varied [Marlin G-Code](https://marlinfw.org/meta/gcode/) for controlling the device. The G-Code files in framing mode that are sent to the device should be structured as follows. More details regarding the xTool G-Code structure can be found below and examples G-Code files can be found under the examples folder.

```
G0 F180000    - Set feedrate laser off to 3000mm/s (max)
M4 S0         - Laser power on, power level to 0
G1 F180000    - Set feedrate laser on to 3000mm/s (max)
M114 S1       - ?? Get current position or some kind of framing related setup parameter
G21           - Select which laser to use, G21 = blue, G22 = IR
G90           - Set absolute positioning

-- add here your actual G-Code coordinates --

G90           - Set absolute positioning
G0 S0         - Laser power to 0 ??
G0 F180000    - Set feedrate laser off to 3000mm/s (max)
G1 F180000    - Set feedrate laser on to 3000mm/s (max)
M6 P1         - Stop lasering process, clean-up and power off the galvo and lasers
```

## Laser Processing Mode - This can be used for laser decapping
This works largely in the same manner as the framing and uses the same HTTP endpoint. It just omits the autoStart and loopPrint parameters to add some safety in that you will need to trigger the process using the button on the side of the device and it only runs the sent G-Code once. TaskId just seems to be random string of letters and numbers that the device can use to keep track of the task and will use it when returning information on the progress.

```
URL: POST ip:8080/processing/upload?gcodeType=processing&fileType=txt&taskId=xxxxx 
Payload: Text format G-Code file with some additions
```

**Notes on the G-Code for this**
```
G90           - Set absolute positioning
G0 F3000      - Set feedrate laser off to 50mm/s
G0 F180000    - Set feedrate laser off to 3000mm/s (max)
M4 S0         - Laser power on, power level to 0
G1 F180000    - Set feedrate laser on to 3000mm/s (max)
G0 X0 Y0      - Set galvanometer to 0,0 point
G21 (or G22)  - Select which laser to use, G21 = blue, G22 = IR
G90           - Set absolute positioning

-- add here your actual G-Code coordinates --

G90           - Set absolute positioning
G0 S0         - Laser power to 0 ??
G0 F180000    - Set feedrate laser off to 3000mm/s (max)
G1 F180000    - Set feedrate laser on to 3000mm/s (max)
M6 P1         - Stop lasering process, clean-up and power off the galvo and lasers
```


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

- G0 F180000 - ?? Setting of the maximum feedrate? As this is only used in the init section
- G0 X0 Y0 - Position the galvanometer to its zero point


### G1 - Linear move, laser on
**Command structure - G0Xnn.nnnYnn.nnnSnnnnFnnnnn**

- X, X-coordinate in millimeters
- Y, Y-coordinate in millimeters
- S, laser power decimal number with single decimal, without decimal separator e.g 64 = 6.4 or 800 = 80.0
- F, Feedrate (movement speed). Calculated with the formula (speed in mm/s)*60 = feedrate e.g. 160mm/s => 160mm/s*60 = 9600

**Important Notes**
The first G1 command should always be used to set the feedrate. This can be done either by issuing a separate G1 command (see below). Or by setting it as part of the first G1 command such as G1X55.00Y55.00S800F6000 (Move the galvanometer head to point X55 Y55, turn the power to 80% and set the feedrate to 100mm/s.

**Special cases**

- G1FnnnnnSnnnn - Set the feedrate for the laser on move commands, S-parameter should be set to 0 in this command


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

# Suggestions/ideas for sharing LFI and decap files
The use of G-Code makes it possible to easily share chip specific LFI and decap files. Here are some ideas how to share these files. **What we are doing is splitting the setup into three separate G-Code files. Alignment framing file, decap file and LFI file.** As it is possible to add all the necessary parameters such as speed(feedrate) and power, along with the coordinates to these files, the only additional setup left for the person using these files is to setup the correct Z-height for the laser. Which is dependant on the breakout board and other variables.

**Alignment framing file**

To ensure the alignment of the chip underneath the laser, it is suggested to start with an alignment framing file (using blue laser, repeating indefinitely). This should be a file that has just the outline of the chip so that it can be accurately be aligned under the laser.

**Decap file**

Provided the alignement is good and the chip can be placed in the correct location the next file to share is to perform the decapping on the chip. This should make it easy to repeat the decapping process successfully for the chip in question.

**LFI file**

The last part, the LFI (laser fault injection) file is another framing file but using IR laser. This file should have the area where the possible fault injection should be performed.
