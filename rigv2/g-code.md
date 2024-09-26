# WORK IN PROGRESS

We are working to get this published as soon as possible. In the meanwhile here is the high-level summary of the G-Code structure.

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

## TODO
- Figure out how the feedrate number can be turned into mm/s
- Figure out which G-Code commands and command combinations are responsible for the selection of laser blue or IR
- Figure out the additional commands and their meaning that are placed in the header and footer of the G-Code file
