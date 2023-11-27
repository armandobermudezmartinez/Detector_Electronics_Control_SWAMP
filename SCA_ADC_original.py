from gbtsca_constants import CTRL
from utils import from_8bit_to_32bit


class SCA_ADC:
    def __init__(self, transactor):
        self.transactor = transactor
        self.number_of_adcs = 31
        self.adc = [None] * self.number_of_adcs
        self.adc_block_disabled = True

    def __getitem__(self, adc_number):
        if adc_number not in range(self.number_of_adcs):
            raise Exception("ADC number out of range")
        if self.adc_block_disabled:
            self._enable_adc()
            self.adc_block_disabled = False
        if self.adc[adc_number] is None:
            self.adc[adc_number] = ADC(adc_number)
        return self.adc[adc_number]

    def _enable_adc(self, enableADC=1):
        m3, d3 = CTRL["MASK_CRD_ADC"], CTRL["MASK_CRD_ADC"] if enableADC else 0
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        self.transactor.write(CTRL["CHANNEL_CTRL"],
                              CTRL["W_CRD"], mask=mask, data=data, comment='Enable all ADCs')

    def write():
        pass

    def read():
        pass


class ADC:
    def __init__(self, adc_number) -> None:
        print(adc_number)
        pass
