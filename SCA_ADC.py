from gbtsca_constants import CTRL
from gbtsca_constants import ADC as ADC_constants
from utils import from_8bit_to_32bit
import gbtsca_exception
from time import sleep

class SCA_ADC:
    def __init__(self, transactor):
        self.transactor = transactor
        self.number_of_adcs = 32
        self.adc = [None] * self.number_of_adcs
        self.adc_block_disabled = True

    def __getitem__(self, adc_number):
        if adc_number not in range(self.number_of_adcs):
            raise Exception("ADC number out of range")
        if self.adc_block_disabled:
            self._enable() 
            self.adc_block_disabled = False
        if self.adc[adc_number] is None:
            self.adc[adc_number] = ADC(self, adc_number)
        return self.adc[adc_number]

    def _enable(self, enableADC=1):
        #m3, d3 = CTRL["MASK_CRD_ADC"], CTRL["MASK_CRD_ADC"] if enableADC else 0
        #mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        #self.transactor.write(CTRL["CHANNEL_CTRL"],
        #                      CTRL["W_CRD"], mask=mask, data=data, comment='Enable all ADCs')
        
        m3, d3 = CTRL["MASK_CRD_ADC"], CTRL["MASK_CRD_ADC"] if enableADC else 0
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        cache = from_8bit_to_32bit(self.transactor.cache_CRD)
        self.transactor.write(CTRL["CHANNEL_CTRL"],
                              CTRL["W_CRD"], mask=mask, data=data, cache=cache, comment='Enable all ADCs')
        self.transactor.cache_CRD |= d3
        #print('adc d3', d3, cache>>24)
        self.transactor.send()

    def _read(self, adc_number):
        self.transactor.write(ADC_constants["CHANNEL"], ADC_constants["W_MUX_REG"], data=adc_number, comment=f'write to SCA ADC {adc_number} register')
        self.transactor.send()

        sleep(0.1)
        self.transactor.write(ADC_constants["CHANNEL"], ADC_constants["GO_REG"], data=1, comment='ADC go')
        self.transactor.send()

        sleep(0.1)
        #self.transactor.write(ADC_constants["CHANNEL"], ADC_constants["R_MUX_REG"], comment=f'read from SCA ADC {adc_number} register')
        #self.transactor.send()



class ADC:
    def __init__(self, sca_adc, adc_number):
        self.sca_adc = sca_adc
        self.adc_number = adc_number       

    def read(self):
        self.sca_adc._read(self.adc_number)
    

