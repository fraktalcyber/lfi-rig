# Fraktal - Laser Fault Injection (LFI) RIG

This project is Fraktal's take in building an affordable Laser Fault Injection that allows anyone to get started with performing laser fault injection attacks, previously left only for laboratories and research institutes with expensive equipment. With this breakthrough, we hope to inspire a new wave of research and development in hardware security.

The series of blog posts related to this repository can be read from [Fraktal Blog](https://blog.fraktal.fi)

**This page is under active update and will be updated multiple times over the coming weeks**

## Contents of the repository

- **PCB** - KiCAD project, schematic and board files for the XY2-100 driver board
- **src** - Micropython script including the XY2-100 software driver and control for the laser PWM
- **Decapping** - Instructions, guidance and methodologies for decapping chips **TO BE RELEASED**
- **LFI** - Instructions, guidance and methodologies for Laser Fault Injection and how to get the best out of the rig **TO BE RELEASED**
- **Other** - Various other things and source material we have created and come across **TO BE UPDATED**


## WARNING

**Before attempting to build and use this rig, please be aware that the 1064nm IR laser is invisible to the eye and extremely dangerous. As the rig is running high powered lasers even a reflected beam can cause immediate severe eye damage.** 

It is imperative to wear laser safety goggles that filter out 1064nm light and to operate the rig in a secure, enclosed box. Line the box with aluminum foil or similar materials to ensure the IR light cannot penetrate. Safety should always be your top priority as any damage to your sight is likely going to be permanent. Also be aware of the potential fire hazards as a powerful IR laser will easily burn through even thin metal.

When buying goggles, get them from reputable sources that provide some certification or other documentation so you can be sure the glasses actually filter the wavelengths. [Example from Farnell](https://fi.farnell.com/imatronic/1900-08-000/laser-safety-glasses-870-1085nm/dp/2334333)

## Shopping list

This details the main components needed to build the rig. The bill of materials for the XY2-100 driver board is listed in the README.md under the PCB folder.

- **Galvanometer (Galvo scanner):** Any that uses XY2–100 protocol and has 1064nm IR coating on the mirrors will do.  These can be had from AliExpress from various sellers for around 130 €, prices seem to vary wildly between sellers and days. If it has a DB-25 connector it likely works with our driver board directly
- **1064nm F-Theta lens:** The smaller the scan area / focus length, the higher the precision. Around 50 €.
- **1064nm IR Laser light source:** Any with at least 200 mW of optical power. The more powerful laser you have the faster you can run the rig. We started with a 200mW module which we were able to haggle to around 50 € from Alibaba but eventually settled for an off-the-shelf Sculpfun IR-2, 2W IR laser module which has integrated driver and enough power to run the rig as fast as the mirrors can move. We managed to get the IR-2 module from a campaign in Alibaba for 220 €. IR-2 is also nice because it has a red alignment laser which makes it possible to see where the laser is pointing.
- **Raspberry Pi Pico:** 5 €.
- **4 channel RS-422/485 driver:** To drive X, Y, Sync and CLK channels in XY2–100 protocol. We used Analog Devices LTC487CSW, 10 € .
- **Power supply:** Capable of providing +-15V @ 2A, we initially used a multi-channel bench power supply. For the final version we used embedded Tracopower TEN60–2423N supply which is 97 € but makes it possible to have everything in a single PCB.

## Assembly and setup

After obtaining all of the required items from the shopping list (and optionally built the driver board all you have left is to assemble the thing. If you went with the Sculpfun IR-2 laser this step is pretty straight forward.

### Mounting the laser to the Galvanometer

Mount the laser to the hole in the galvanometer. You can build proper brackets or just duct tape it together like we have. Both work equally well. Whatever you do, leave things a bit loose for now so that it is possible to align the beam to the center of the hole when you power the rig on.

![Laser Mount](/Other/Images/laser-mount.png)

### Attaching the lens

Screw in the F-Theta lens. Before attaching the lens, make sure the mirrors and the lens are clean and don't have any dust particles or other dirt as that will be likely burnt to the mirror surface when you first time power on the laser.

### Holding the rig in place

We are holding the rig in place in our lab simply with a monitor mount that can be height adjusted and which has VESA mount that can be tilted 90 degrees. The VESA mount has two L-Brackets attached to it that hold the rig in place.

![Rig Mount](/Other/Images/rig-mount.png)

### Assembling the driver PCB

The driver PCB has very few parts and is pretty straight forward to assemble. There are only few things that should be considered.

- Although the Raspberry Pi Pico can be mounted flush on the PCB we suggest mounting a pin header to the holes and then pressing the Pico in. This has benefits, it leaves a bit more clearance under the Pico and fits even the bulkiest Micro USB cables, it allows to use the pads to mount wires and additional headers for monitoring etc. We are for example driving the target chip power often straight from the Pico as this makes wiring a bit simpler. For this we have added few extra headers for select pins.
- **DB-15 Header should be mounted to the backside of the PCB**, with the rest of the components on the frontside where the Raspberry Pi Pico is.
- The PCB BOM is listed with more detail underneath the PCB folder

### Connecting all the cables and wiring pinouts

Most of the available galvanometers seem to be using similar structure and come with DB-25 connector in the galvanometer itself. It is still worth to check that the one you are planning on buying has same or similar pinout to what we used if you are planning on running our driver board.

![Galvo Pinout](/Other/Images/galvanometer-cable-pinout.png)

These galvanometers come with wiring harness that has DB-25 that goes to the galvanometer with the other end having DB-15 and four loose cables. The DB-15 connector is used for the XY2-100 four channels and you can verify the pinout by beeping the cable with a multimeter in continuity mode. DB-15 should work directly with our driver and can be connected straight to the PCB.

*As we didn't want to run the rig from mains with insufficient protections, We ditched the power supply that came with the galvanometer as that connects straight to mains and doesn't offer same amount of protections as a lab power supply can provide.*

The four loose cables we had in our harness were coloured blue (-15VDC), black (GND), red (+15VDC) and yellow (Mains Earth **DO NOT CONNECT THIS UNLESS YOU KNOW WHAT YOU ARE DOING**). Blue, black and red wires can be connected to the Galvo OUT header on the driver PCB.

If you are running the Sculpfun IR-2 laser, the laser probably came with this type of connector.

![Sculpfun Pinout](/Other/Images/sculpfun-connector.png)

The pinout for the connector is from left to right, 1kHZ PWM signal @ 3V3, GND, +24VDC

When connecting the PWM signal to the respective header on the driver PCB, it is **highly recommended to add a mechanical switch on the signal wire** this allows you to have a mechanical safety switch and prevent accidental running of the laser main beam. Only toggle the switch when everything is enclosed and you are wearing your goggles.

With everything connected it is time for test run!

### Testing the rig works and aligning the laser

With everything connected and setup the first thing you should do is to align the laser. If you went with Sculpfun IR-2, you can power the laser **with PWM signal disconnected**. This should give you a red laser spot that is the alignment beam that is firing **when the main beam is not firing**. The alignment beam spotsize is much larger than the actual IR laser spot but it can be used to align the laser horizontally and vertically to make the spot as small as possible. We haven't felt a need to do anything but an alignment visually when it looks the smallest. That has been sufficient as the rest can be compensated with software parameters.

In order to get the laser pointing through the F-Theta lens, you also need to power on the galvanometer. When giving the galvanometer -15VDC and +15VDC it centers the mirrors into zero position and makes sure that your laser spot actually goes through the lens. 

Move the laser in its mount so that it is roughly in the center of the input hole, and the laser comes through as middle of the lens as possible. Once the laser is centered, tighten all of the screws or duct tape the laser in place.

Then adjust the horizontal alignment of the whole rig by moving it up and down in the rig mount and try to get as small beam as possible.

We are running IR-2 without the collimator lens that came with the laser as we have found that it makes it easier to mount the laser flush with the galvanometer. You should try it with and without and move the laser horizontally as well to find what works best for your setup and the selected F-Theta lens. Each setup is slightly different so there are no direct guides how to get the smallest spot size on your specific setup.

After the laser is aligned and as small as possible it is time to test the mirrors move and can be controlled. To do this, **still with the PWM signal disconnect** run the findPerimeter function with parameters (x-axis start position, x-axis end position, y-axis start position, y-axis end position, time to sleep before running the perimeter) so for example

	findPerimeter(0,3500,0,3500,0)

This should draw a square with the scanning laser on whatever surface you have underneath the laser. If you can't see a uniform sized square, the mirrors don't move fluently, if you see laser points outside of the square or anything else. You need to do some debugging and figure out what is wrong.

If you on the other hand see a square, now you can use the square to align the laser rig and check that it is not tilted. We have found best to have some uniform known sized square that you use as a reference such as graph paper. Align the x and y axis in the function to get the right size and then align the rig with the graph paper on a flat surface to get the rig to be level. This is important especially if you are running the rig at full speed as slight misalignment here will mean different laser power hitting different parts of the chip. Ideally you'd want to have as uniform and flat plane as possible.

If everything works and you have everything setup now its time to try on some actual samples.

## Running the rig in fault injection mode

Provided that you managed to get everything working and setup, and have a decapped IC using our method or any other method. It is time to run the rig in fault injection mode.

You should start with mounting the sample underneath the rig as center as possible and adjusting the perimeter size using the findPerimeter function. When adjusting the perimeter, it is a good idea to go slightly over the actual die, that way you will not be missing the edges of the die which may or may not have something that causes faults. Having the sample as center as possible makes the lens work the best and keeps the spot as uniform as possible.

With the perimeter setup and parameters found it is time to put the rig inside a box, enclosure and shield your eyes with the glasses. What we have done is to add a webcam or some camera inside the box to be able to see what is happening. With most webcams it is also possible to see a faint violet tint when the IR laser main beam is firing, similar to what you can see when you view your TV remote using your phone camera.

The main function to be used for scanning the die to produce faults is scanChip.

	scanChip(0,3500,0,3500,40,True)
	
The function takes as parameters the chip perimeter and the "hop" or how much the mirrors are to be moved with a single drive cycle, the last value is True/False if the laser should be firing or not. For a test run we suggest running the scanChip with laser turned off and only the alignment beam lit, this allows you to see the scanning is working properly and that you are scanning the entire die area.

If the dry run works it is time to run with the main beam. If using the IR-2 laser a suggested starting point value for power is 8000 for the duty cycle. This has in our experiments been a nice baseline as (depending on the hopsize, thus the mirror speed) it has been enough power to cause faults to appear in most of the chips we have tried.

It is always best to start with a chip where you have full control, via a debugger or running a software loop that you know what it is doing.. We did initial tests with having a same chip as our target chip was, and run a sample firmware that runs in while true loop and just prints incrementing number into UART. Then we adjusted first the power level to something where we start seeing faults happen. Then we played around with the hop parameter and adjusting the power so that we can run the rig as fast as possible while still producing same or similar faults as initially observed.

Now the rig and parameter should be setup for trying the rig with an actual target chip and to try and for example bypass code readout protections or secure boot verifications. 

**ENJOY!**
