# 4mm x 4mm square outline in the middle of the stage, framing mode
# Laser blue
# Laser power 6.4%  (S64) - The default framing laser power from XCS studio
# Feedrate 12000mm/s (F720000)

# Framing header
G0 F180000
M4 S0
G1 F180000
M114 S1

# Selecting Blue laser
G21
G90

# The actual lasering
G0X55.500Y55.500
G1X59.500Y55.500S64F720000
G1X59.500Y59.500
G1X55.500Y59.500
G1X55.500Y55.500

# End setup
G90
G0 S0
G0 F180000
G1 F180000
M6 P1
