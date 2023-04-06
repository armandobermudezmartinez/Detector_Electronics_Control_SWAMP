from SCA_I2C import SCA_I2C
from SCA_GPIO import SCA_GPIO
from gbtsca_config import gbtsca_reset, gbtsca_connect, gbtsca_start


class GBT_SCA:
    def __init__(self, transactor):
        self.transactor = transactor
        self.i2c = SCA_I2C(transactor)
        self.pin = SCA_GPIO(transactor)

        self.configure()

    def configure(self):
        self.reset()
        self.connect()
        self.start()
        self.flush()

    def flush(self):
        self.transactor.flush()

    def reset(self):
        self.transactor.write(gbtsca_reset['ch_address'], gbtsca_reset['cmd'],
                              command_id=gbtsca_reset['cmd_id'], data=gbtsca_reset['payload'])

    def connect(self):
        self.transactor.write(gbtsca_connect['ch_address'], gbtsca_connect['cmd'],
                              command_id=gbtsca_connect['cmd_id'], data=gbtsca_connect['payload'])

    def start(self):
        self.transactor.write(gbtsca_start['ch_address'], gbtsca_start['cmd'],
                              command_id=gbtsca_start['cmd_id'], data=gbtsca_start['payload'])
