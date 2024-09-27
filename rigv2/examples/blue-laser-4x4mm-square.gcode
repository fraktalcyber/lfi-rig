# 4mm x 4mm square outline in the middle of the stage
# Laser Blue
# Laser power 10%  (S100)
# Feedrate 100mm/s (F6000)

# Processing header
G90
G0 F3000
G0 F180000
M4 S0
G1 F180000
G0 X0 Y0

# Selecting IR laser
G21
G90

# The actual lasering
G0X55.500Y55.500
G1X59.500Y55.500S100F6000
G1X59.500Y59.500
G1X55.500Y59.500
G1X55.500Y55.500

# End setup
G90
G0 S0
G0 F180000
G1 F180000
M6 P1
