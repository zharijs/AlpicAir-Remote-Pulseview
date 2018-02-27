## 
## ALPIC AIR heat pump remote is similar to NEC infrared remote control protocol, but uses PDC (pulse distance coding).
## The initial high pulse is 9ms, followed by 445us low edge. 
## The clocking pulse is high 700us +/- 30us, followed by a data bit low edge (distance) of about 1600us +/- 50us for logic 1 and about 500us +/- 30 us for logic 0.
## The first 4 data bits are synchrogroup (0011)
## Next 2 bits denote the fan speed.
##
##
##
##
## Pause of about 20ms follows 
##
##
##
##
## Transmission ends with a low level after a final clock pulse. 
##

'''
ALPIC_AIR heat pump remote is similar to NEC infrared remote control protocol, but uses PDC (pulse distance coding).
'''

from .pd import Decoder
