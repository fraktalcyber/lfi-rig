from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio
import time
import array
import random

#---------------------------
#Configuration parameters

#How much to sleep between mirror movements
SLEEPTIME = 0

#Value from 0 to 65535, for Sculpfun IR-2 values around 8000 start to produce faults on most ICs
LASERPOWER = 8000 



#---------------------------
#Setup parameters

laser = PWM(Pin(4))
laser.freq(1000) #1khz drive signal when using Sculpfun IR-2 laser
laser.duty_u16(0) #disable laser initially

#PSU Control
psu = Pin(5, Pin.OUT)
psu.low() #disable PSU initially


#Interleave bits using Z Curve a1 b1 a2 b2...
def interleaveBits(a, b):
    result = 0
    for i in range(32):  # Loop through each bit position
        # Mask and shift the bit from 'a' into the correct position in 'result'
        a_bit = (a >> i) & 1
        result |= a_bit << (2 * i)
        
        # Mask and shift the bit from 'b' into the correct position in 'result'
        b_bit = (b >> i) & 1
        result |= b_bit << (2 * i + 1)
    
    return result

#Calculate parity bit for XY2-100
def parity(int_type):
    parity = 0
    while (int_type):
        parity = ~parity
        int_type = int_type & (int_type - 1)
    return parity

#Make the actual XY2-100 dataframe
def makeFrame(val):
    global cmdCount
    frame = 0b1 << 16
    frame = frame | val
    if parity(frame) == 0:
        frame = frame << 1 | 1
    else:
        frame = frame << 1
    return int(frame)


#Hacky PIO Bitbanging implementation of XY2-100 protocol
@rp2.asm_pio(sideset_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW), out_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW), set_init=rp2.PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT)
def XYWrite(): 
    pull()
    out(y,24)
    set(x,3)                 .side(0b00)
    label("hiloop")
    out(pins, 2)             .side(0b11)    [3]
    jmp(x_dec, "hiloop")     .side(0b10)	[3]
    pull()
    set(x,14)
    label("loloop")
    out(pins, 2)             .side(0b11)    [3]
    jmp(x_dec, "loloop")     .side(0b10)    [3]
    out(pins, 2)			 .side(0b01)	[3]
    nop()					 .side(0b00)	[3]

#Main function that controls the XY2-100 for mirror position this should be called when mirrors need to be moved
def drive(x,y):
    sm = rp2.StateMachine(0, XYWrite, freq=8*2000000, sideset_base=Pin(2), out_base=Pin(0))
    sm.active(1)
    xFrame = makeFrame(x)
    yFrame = makeFrame(y)
    
    #Make frames for x and y positions and interleave them using Z Curve x1 y1 x2 y2...
    #Turn the resulting 64bit xyFrame and split it into two 32bit words to send to PIO
    xyFrame = interleaveBits(xFrame,yFrame)
    a = array.array('I', [int((xyFrame>> 32) & 0xFFFFFFFF), int(xyFrame & 0xFFFFFFFF)])
    sm.put(a)
    time.sleep(SLEEPTIME)


#Helper function if using Sculpfun IR-2 module. This will move the mirrors very fast to make the adjusting beam
#to form a square that shows the scan area. Use this to adjust the xs,ys (x-start, y-start) and xe,ye (x-end, y-end)
#to be correct for the die you are working with
def findPerimeter(xs,xe,ys,ye,slp):
    psu.high()
    time.sleep(1)
    print("FIND PERIMETER MODE")
    while True:
        drive(xs,ys)
        time.sleep(slp)
        drive(xs,ye)
        time.sleep(slp)
        drive(xe,ye)
        time.sleep(slp)
        drive(xe,ys)
        time.sleep(slp)
    psu.low()


#This is the main function that is used with the REAL LASER!
#MAKE SURE YOU ARE WEARING LASER GOGGLES WHEN USING THIS!
#Parameters:
#xs,xe define the start and end for X-axis
#ys,ye define the start and end for Y-axis
#hop defines how much the mirror moves at a time
#shoot True/False defines if the laser is turned on/off
def scanChip(xs,xe,ys,ye, hop, shoot=False):
    psu.high()
    time.sleep(0.3) #This is an extra delay to compensate IR-2 startup time
    if shoot:
        laser.duty_u16(LASERPOWER)
    for y in range(ys, ye, hop):
        if(y == 0):
            start = time.ticks_ms()
        for x in range(xs, xe, hop):
            drive(x, y)
        if(y == 0):    
            end = time.ticks_ms()
            d = (((end-start)/1000)*(ye-y/hop))
            if shoot:
                print("SHOOT MODE ENABLED! Cover your EYES!")
                print("Laser power is", (LASERPOWER/65535)*100)
            print("One line in (s)", (end-start)/1000)
            print("Estimated completion (min) (hour):", d/60, d/60/60)
        if(y % 100 == 0):
            print("Completion (%):", (y/ye)*100)
    laser.duty_u16(0)
    psu.low()


#EXAMPLES HOW TO USE THE FUNCTIONS

print("WAITING FOR 5s, time to CANCEL")
time.sleep(5)


#Perform 300 iterations of whole chip scan with various hop-sizes to see how precise you need to be
#for i in range(0,300):
#    scanChip(0,3500,0,3500,random.randint(50,100),True)

#Example of using perimeter finding mode
#findPerimeter(2500,3500,0,3500,0)


