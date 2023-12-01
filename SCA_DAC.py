from gbtsca_constants import CTRL
from gbtsca_constants import DAC as DAC_constants
from utils import from_8bit_to_32bit
from time import sleep

class SCA_DAC:
    def __init__(self, transactor):
        self.transactor = transactor
        self.dac = {'a': None, 'b': None, 'c': None, 'd': None}
        self.dac_block_disabled = True
        self.max_voltage = 1.25 # maximum voltage of the DACs in Volts
        self.min_voltage = 0. # maximum voltage of the DACs in Volts
        self.max_value = 0xFF # maximum value of the DACs
        self.min_value = 0x00 # maximum value of the DACs


    def __getitem__(self, dac_channel):
        if dac_channel == 0: dac_channel = 'a'
        if dac_channel == 1: dac_channel = 'b'
        if dac_channel == 2: dac_channel = 'c'
        if dac_channel == 3: dac_channel = 'd'

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

    def set_voltage_range(self, min_voltage, max_voltage):
        self.sca_dac.max_voltage = max_voltage
        self.sca_dac.min_voltage = min_voltage

    def set_value_range(self, min_value, max_value):
        self.sca_dac.max_value = max_value
        self.sca_dac.min_value = min_value

    def write(self, voltage=None, value=None):
        if value is None:
            if voltage is None:
                if not self.sca_dac.min_value <= value <= self.sca_dac.max_value:
                    raise Exception(f"Please provide a valid voltage or value")
            a = (self.sca_dac.max_value - self.sca_dac.min_value)/(self.sca_dac.max_voltage - self.sca_dac.min_voltage)
            b = self.sca_dac.min_value - a*self.sca_dac.min_voltage 
            value = int(voltage*a + b)
        else:
            a = (self.sca_dac.max_voltage - self.sca_dac.min_voltage)/(self.sca_dac.max_value - self.sca_dac.min_value)
            b = self.sca_dac.min_voltage - a*self.sca_dac.min_value
            voltage = round(value*a + b, 3)
        if not self.sca_dac.min_value <= value <= self.sca_dac.max_value:
            raise Exception(f"Voltage out of range of the DAC [{self.sca_dac.min_voltage}, {self.sca_dac.max_voltage}]")
        self.sca_dac._write(self.dac_channel, value)
        self.sca_dac.transactor.send()
        self.value = value
        self.voltage = voltage
        print('value: ', value, 'voltage', voltage)
 
    def read(self):
        self.sca_dac._read(self.dac_channel)
        self.sca_dac.transactor.send()

      


 
