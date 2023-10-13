from gbtsca_constants import CTRL
from utils import from_8bit_to_32bit


class SCA_DAC:
    def __init__(self, transactor):
        self.transactor = transactor
        self.number_of_dacs = 31
        self.dac = [None] * self.number_of_dacs
        self.dac_block_disabled = True

    def __getitem__(self, dac_number):
        if dac_number not in range(self.number_of_dacs):
            raise Exception("DAC number out of range")
        if self.dac_block_disabled:
            self._enable_dac()
            self.dac_block_disabled = False
        if self.dac[dac_number] is None:
            self.dac[dac_number] = DAC(dac_number)
        return self.dac[dac_number]

    def _enable_dac(self, enableDAC=1):
        m3, d3 = CTRL["MASK_CRD_DAC"], CTRL["MASK_CRD_DAC"] if enableDAC else 0
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        self.transactor.write(CTRL["CHANNEL_CTRL"],
                              CTRL["W_CRD"], mask=mask, data=data, comment='Enable all DACs')

    def write():
        pass

    def read():
        pass


class DAC:
    def __init__(self, dac_number) -> None:
        print(dac_number)
        pass
