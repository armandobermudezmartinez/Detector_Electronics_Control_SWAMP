from gbtsca_constants import CTRL, GPIO
from utils import from_8bit_to_32bit


class SCA_GPIO:
    def __init__(self, transactor):
        self.transactor = transactor
        self.pin = [None] * 32
        self.pin_block_disabled = True
        self._mode_mask = 0
        self._mode = 0
        self._outputs_cache = 0

    def __getitem__(self, pin_number):
        if pin_number not in range(32):
            raise Exception("Pin number out of range")
        if self.pin_block_disabled:
            self._enable_gpio()
            self.pin_block_disabled = False
        if self.pin[pin_number] is None:
            self.pin[pin_number] = Pin(self, pin_number)
        return self.pin[pin_number]


    def _enable_gpio(self, enableGPIO=1):
        m3, d3 = CTRL["MASK_CRB_PARAL"], CTRL["MASK_CRB_PARAL"] if enableGPIO else 0
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        self.transactor.write(CTRL["CHANNEL_CTRL"],
                              CTRL["W_CRB"], mask=mask, data=data, comment='Enable all Pins')

    def _read_enable_gpio(self):
        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRB"], comment='Read which Pins are Enabled')

    def _set_gpio_mode(self, pin, mode):
        self._mode |= mode << pin
        self.transactor.write(
            GPIO["CHANNEL"], GPIO["W_DIRECTION"], mask=self._mode, data=self._mode, comment=f'Set Mode of Pin {pin}')

    def _get_gpio_mode(self):
        self.transactor.write(GPIO["CHANNEL"], GPIO["R_DIRECTION"], comment='Reading the Mode of all Pins')

    def _gpio_write(self, pin, output):
        mask = 1 << pin
        data = output << pin
        if (self._outputs_cache & mask) != data:
            self.transactor.write(GPIO["CHANNEL"], GPIO["R_DATAOUT"])
            self.transactor.write(
                GPIO["CHANNEL"], GPIO["W_DATAOUT"], mask=mask, data=data)


class Pin:
    def __init__(self, sca_gpio, pin_number):
        self.sca_gpio = sca_gpio
        self.pin_number = pin_number
        self.mode = 0
        self.output = None

    def set_mode(self, mode):
        if mode == "in":
            self.mode = 0
        elif mode == "out":
            self.mode = 1
        else:
            raise Exception('Pin mode must be either "in" or "out"')
        self.sca_gpio._set_gpio_mode(self.pin_number, self.mode)

    def write(self, output):
        if self.mode == 1:
            self.sca_gpio._gpio_write(self.pin_number, output)
            self.output = output
