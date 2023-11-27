from SCA_I2C import SCA_I2C
from SCA_GPIO import SCA_GPIO
from SCA_ADC import SCA_ADC
from SCA_DAC import SCA_DAC
from gbtsca_config import gbtsca_reset, gbtsca_connect, gbtsca_start
from gbtsca_constants import CTRL
from time import sleep

class GBT_SCA:
    def __init__(self, transactor):
        self.transactor = transactor
        self.i2c = SCA_I2C(transactor)
        self.pin = SCA_GPIO(transactor)
        self.adc = SCA_ADC(transactor)
        self.dac = SCA_DAC(transactor)

        self.configure()
        #self.transactor.send()

    def flush(self):
        self.transactor.flush()

    def configure(self):
        self.reset()
        self.connect()
        self.start()
        # self.flush()

    def reset(self):
        self.transactor.write(gbtsca_reset['ch_address'], gbtsca_reset['cmd'],
                              command_id=gbtsca_reset['cmd_id'], data=gbtsca_reset['payload'], comment='Resetting SCA')
        self.transactor.free_transaction_ids.append(
            self.transactor._transaction_id)
        self.transactor.send()
#        sleep(1)

    def connect(self):
        self.transactor.write(gbtsca_connect['ch_address'], gbtsca_connect['cmd'],
                              command_id=gbtsca_connect['cmd_id'], data=gbtsca_connect['payload'], comment='Connecting SCA')
        self.transactor.free_transaction_ids.append(
            self.transactor._transaction_id)
        self.transactor.send()
#        sleep(1)

    def start(self):
        self.transactor.write(gbtsca_start['ch_address'], gbtsca_start['cmd'],
                              command_id=gbtsca_start['cmd_id'], data=gbtsca_start['payload'], comment='Starting SCA')
        self.transactor.send()
#        sleep(1)      

    def read_enable_i2c(self):
        self.i2c._read_enable_i2c()

    def enable_gpio(self):
        self.pin._enable_gpio()

    def read_enable_gpio(self):
        self.pin._read_enable_gpio()

    def read_gpio_mode(self):
        self.pin._get_gpio_mode()

    def _read_device_id(self, version='v2'):
        if (version == 'v2'):
            self.transactor.write(CTRL["CHANNEL_ID"],
                                  CTRL["R_CHIP_ID_V2"], comment='read device ID V2')
        
        elif (version == 'v1'):
            self.transactor.write(CTRL["CHANNEL_ID"],
                             CTRL["R_CHIP_ID_V1"], comment='read device id V1')
        else: 
            raise Exception("Version not within available options: v1, v2")

        self.transactor.send()
