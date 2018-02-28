# AlpicAir-Remote-Pulseview
Pulseview plugin for AlpicAir heat pump IR remote control [partial decode]

# Hardware
Tested on YB1F2 contproller.

![Transmitter Front](https://raw.githubusercontent.com/zharijs/AlpicAir-Remote-Pulseview/master/pics/aa-front.jpg "Transmitter Front")
![Transmitter Back](https://raw.githubusercontent.com/zharijs/AlpicAir-Remote-Pulseview/master/pics/aa-back.jpg "Transmitter Back")

# Protocol
The protocol is similar to NEC with different timing and data fields. Low level decode is implemented. High level protocol decode shows about hald of data fields. Other half is missing. It seems that there might be a block with checksum that has to be decoded.

# Usage
Add to your Sigrok/PulseView install directory.

Example:
C:\Program Files (x86)\sigrok\PulseView\share\libsigrokdecode\decoders\
