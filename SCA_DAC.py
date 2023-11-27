from gbtsca_constants import CTRL
from gbtsca_constants import DAC as DAC_constants
from utils import from_8bit_to_32bit
from time import sleep

class SCA_DAC:
    def __init__(self, transactor):
        self.transactor = transactor
        self.dac = {'a': None, 'b': None, 'c': None, 'd': None}
        self.dac_block_disabled = True

    def __getitem__(self, dac_channel):
        if dac_channel.lower() not in self.dac.keys():
            raise Exception("DAC channel not within defined values: a, b, c, d")
        if self.dac_block_disabled:
            self._enable()
            self.dac_block_disabled = False
        if self.dac[dac_channel] is None:
            self.dac[dac_channel] = DAC(self, dac_channel)
        return self.dac[dac_channel]

    def _enable(self, enableDAC=1):
        m3, d3 = CTRL["MASK_CRD_DAC"], CTRL["MASK_CRD_DAC"] if enableDAC else 0
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        cache = from_8bit_to_32bit(self.transactor.cache_CRD)
        self.transactor.write(CTRL["CHANNEL_CTRL"],
                              CTRL["W_CRD"], mask=mask, data=data, cache=cache, comment='Enable all DACs')
        self.transactor.cache_CRD |= d3
        self.transactor.send()


    def _write(self, channel, value):
        # Channel is A, B, C, or D. Value ranges from 0-1.0V, 0x00->0xFF.
        if(channel == 'a'):
            self.transactor.write(DAC_constants["CHANNEL"],
                             DAC_constants["W_A"], data=from_8bit_to_32bit(value), comment='Write to DAC channel A')
        elif(channel == 'b'):
            self.transactor.write(DAC_constants["CHANNEL"],
                             DAC_constants["W_B"], data=from_8bit_to_32bit(value), comment='Write to DAC channel B')
        elif(channel == 'c'):
            self.transactor.write(DAC_constants["CHANNEL"],
                             DAC_constants["W_C"], data=from_8bit_to_32bit(value), comment='Write to DAC channel C')
        elif(channel == 'd'):
            self.transactor.write(DAC_constants["CHANNEL"],
                             DAC_constants["W_D"], data=from_8bit_to_32bit(value), comment='Write to DAC channel D')


    def _read(self, channel):
        if(channel.lower() == 'a'):
            self.transactor.write(DAC_constants["CHANNEL"],DAC_constants["R_A"], comment='Read from DAC channel A')
        elif(channel.lower() == 'b'):
            self.transactor.write(DAC_constants["CHANNEL"],DAC_constants["R_B"], comment='Read from DAC channel B')
        elif(channel.lower() == 'c'):
            self.transactor.write(DAC_constants["CHANNEL"],DAC_constants["R_C"], comment='Read from DAC channel C')
        elif(channel.lower() == 'd'):
            self.transactor.write(DAC_constants["CHANNEL"],DAC_constants["R_D"], comment='Read from DAC channel D')



class DAC:
    def __init__(self, sca_dac, dac_channel):
        self.sca_dac = sca_dac
        self.dac_channel = dac_channel
        print(sca_dac.dac_block_disabled, dac_channel)
        self.sca_dac.transactor.send()

    def write(self, value):
        self.sca_dac._write(self.dac_channel, value)
        self.value = value
        print('=====value: ', value)
    def read(self):
        self.sca_dac._read(self.dac_channel)
        
      


 
