##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2013-2016 Uwe Hermann <uwe@hermann-uwe.de>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd
from .lists import *

class SamplerateError(Exception):
    pass

class Decoder(srd.Decoder):
    api_version = 3
    id = 'ir_alpicair'
    name = 'IR ALPICAIR'
    longname = 'IR ALPICAIR'
    desc = 'Decode the protocol of IR remote controller of Alpic Air heat pumps'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = ['ir_alpicair']
    channels = (
        {'id': 'ir', 'name': 'IR', 'desc': 'Data line'},
    )
    annotations = (
        ('syncl', 'Sync L'),
        ('synch', 'Sync H'),
        ('clk', 'C'),
        ('bit', 'Bit'),
        ('pause', 'Pause'),
        ('stop', 'Stop'),    
    )
    
    annotation_rows = (
        ('bits', 'Bits', (0, 1, 2, 3, 4, 5)),
    )
    
    def putx(self, data):
        self.put(self.ss_edge, self.samplenum, self.out_ann, data)
        
    def __init__(self):
        self.ss_edge = None

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value    
        self.margin-bits = int(self.samplerate * 0.0001) - 1 # 0.1ms
        self.margin-start = int(self.samplerate * 0.001) - 1 # 1ms
        self.margin-pause = int(self.samplerate * 0.002) - 1 # 2ms
        self.bit-start-low = int(self.samplerate * 0.009) - 1 # 9ms
        self.bit-start-high = int(self.samplerate * 0.00045) - 1 # 0.45ms        
        self.bit-pause = int(self.samplerate * 0.02) - 1 # 20ms        
        self.bit-clock = int(self.samplerate * 0.0007) - 1 # 0.7ms
        self.bit-zero = int(self.samplerate * 0.0005) - 1 # 0.5ms
        self.bit-one = int(self.samplerate * 0.0016) - 1 # 1.6ms
         
    def decode(self):
        if not self.samplerate:
            raise SamplerateError('Cannot decode without samplerate.')

        # Get the first edge on the data line.
        
        while True:
            # wait for first falling edge
            (self.ir,) = self.wait({0: 'f'})
            self.ss_edge = self.samplenum

            # wait for first rising edge, check if start low pulse ok
            (self.ir,) = self.wait({0: 'r'})
            if (self.samplenum-self.ss_edge) in range(self.bit-start-low - self.margin-start, self.bit-start-low + self.margin-start):
				self.put(self.ss_edge, self.samplenum, self.out_ann, [1, ['AGC pulse', 'AGC', 'A']]) 
				#self.putx([0, ['Sinc L %d ms' % self.samplenum-self.ss_edge]])
            
            # wait for falling edge, check if start high ok
            self.ss_edge = self.samplenum
            (self.ir,) = self.wait({0: 'f'})
            if (self.samplenum-self.ss_edge) in range(self.bit-start-high - self.margin-bits, self.bit-start-high + self.margin-bits):
				self.put(self.ss_edge, self.samplenum, self.out_ann, [2, ['AGC pulse', 'AGC', 'A']]) 
                #self.putx([0, ['Sinc H %d ms' % self.samplenum-self.ss_edge]])
                
            # wait for rising edge of clock 
            self.ss_edge = self.samplenum    
            (self.ir,) = self.wait({0: 'r'})
            if (self.samplenum-self.ss_edge) in range(self.bit-clock - self.margin-bits, self.bit-clock + self.margin-bits):
                 self.putx([0, ['C %d ms' % self.samplenum-self.ss_edge]])
            
            # wait for falling edge after a bit
            self.ss_edge = self.samplenum
            (self.ir,) = self.wait({0: 'f'})
            if (self.samplenum-self.ss_edge) in range(self.bit-zero - self.margin-bits, self.bit-zero + self.margin-bits):
                 self.putx([0, ['0 %d ms' % self.samplenum-self.ss_edge]])
            elif (self.samplenum-self.ss_edge) in range(self.bit-one - self.margin-bits, self.bit-one + self.margin-bits):
                 self.putx([0, ['1 %d ms' % self.samplenum-self.ss_edge]])
        
            # wait for rising edge of clock 
            self.ss_edge = self.samplenum    
            (self.ir,) = self.wait({0: 'r'})
            if (self.samplenum-self.ss_edge) in range(self.bit-clock - self.margin-bits, self.bit-clock + self.margin-bits):
                 self.putx([0, ['C %d ms' % self.samplenum-self.ss_edge]])
            
            # wait for falling edge after a bit
            self.ss_edge = self.samplenum
            (self.ir,) = self.wait({0: 'f'})
            if (self.samplenum-self.ss_edge) in range(self.bit-zero - self.margin-bits, self.bit-zero + self.margin-bits):
                 self.putx([0, ['0 %d ms' % self.samplenum-self.ss_edge]])
            elif (self.samplenum-self.ss_edge) in range(self.bit-one - self.margin-bits, self.bit-one + self.margin-bits):
                 self.putx([0, ['1 %d ms' % self.samplenum-self.ss_edge]])

            # wait for rising edge of clock 
            self.ss_edge = self.samplenum    
            (self.ir,) = self.wait({0: 'r'})
            if (self.samplenum-self.ss_edge) in range(self.bit-clock - self.margin-bits, self.bit-clock + self.margin-bits):
                 self.putx([0, ['C %d ms' % self.samplenum-self.ss_edge]])
            
            # wait for falling edge after a bit
            self.ss_edge = self.samplenum
            (self.ir,) = self.wait({0: 'f'})
            if (self.samplenum-self.ss_edge) in range(self.bit-zero - self.margin-bits, self.bit-zero + self.margin-bits):
                 self.putx([0, ['0 %d ms' % self.samplenum-self.ss_edge]])
            elif (self.samplenum-self.ss_edge) in range(self.bit-one - self.margin-bits, self.bit-one + self.margin-bits):
                 self.putx([0, ['1 %d ms' % self.samplenum-self.ss_edge]])

            # wait for rising edge of clock 
            self.ss_edge = self.samplenum    
            (self.ir,) = self.wait({0: 'r'})
            if (self.samplenum-self.ss_edge) in range(self.bit-clock - self.margin-bits, self.bit-clock + self.margin-bits):
                 self.putx([0, ['C %d ms' % self.samplenum-self.ss_edge]])
            
            # wait for falling edge after a bit
            self.ss_edge = self.samplenum
            (self.ir,) = self.wait({0: 'f'})
            if (self.samplenum-self.ss_edge) in range(self.bit-zero - self.margin-bits, self.bit-zero + self.margin-bits):
                 self.putx([0, ['0 %d ms' % self.samplenum-self.ss_edge]])
            elif (self.samplenum-self.ss_edge) in range(self.bit-one - self.margin-bits, self.bit-one + self.margin-bits):
                 self.putx([0, ['1 %d ms' % self.samplenum-self.ss_edge]])
      