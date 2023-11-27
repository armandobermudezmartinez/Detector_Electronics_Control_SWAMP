from gbtsca_constants import CTRL, GPIO
from utils import from_8bit_to_32bit


class SCA_GPIO:
    def __init__(self, transactor):
        self.transactor = transactor
        self.number_of_pins = 32
        self.pin = [None] * self.number_of_pins
        self.pin_block_disabled = True
        self._mode_mask = 0
        self._mode = 0
        self._outputs_cache = 0
        self.cache_output = 0
        self.cache_mask = 0
        # print(CTRL["CHANNEL_CTRL"], GPIO["CHANNEL"])

    def __getitem__(self, pin_number):
        if pin_number not in range(self.number_of_pins):
            raise Exception("Pin number out of range")
        if self.pin_block_disabled:
            self._enable()
            self.pin_block_disabled = False
        if self.pin[pin_number] is None:
            self.pin[pin_number] = Pin(self, pin_number)
        return self.pin[pin_number]

    def _enable(self, enableGPIO=1):
        m3, d3 = CTRL["MASK_CRB_PARAL"], CTRL["MASK_CRB_PARAL"] if enableGPIO else 0
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        # print('dataaa', data)
        cache = from_8bit_to_32bit(self.transactor.cache_CRB)
        self.transactor.write(CTRL["CHANNEL_CTRL"],
                              CTRL["W_CRB"], mask=mask, data=data, cache=cache, comment='Enable all Pins')
        # print('i2c mask', bin(m3))
        # print('gpio data', bin(d3), 'cache CRB', bin(self.transactor.cache_CRB))
        self.transactor.cache_CRB |= d3
        # print('enable CRB', self.transactor.cache_CRB)
        self.transactor.send()

    def _read_enable(self):
        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRB"], comment='Read which Pins are Enabled')
        self.transactor.send()

    def _set_mode(self, pin, mode):
        self._mode |= mode << pin
        self.transactor.write(
            GPIO["CHANNEL"], GPIO["W_DIRECTION"], mask=self._mode, data=self._mode, comment=f'Set Mode of Pin {pin}')
        self.transactor.send()

    def _get_mode(self):
        self.transactor.write(
            GPIO["CHANNEL"], GPIO["R_DIRECTION"], comment='Reading the Mode of all Pins')
        self.transactor.send()

    def _get_output(self):
        self.transactor.write(GPIO["CHANNEL"],
                              GPIO["R_DATAOUT"], comment='Get gpio output')
        self.transactor.send()

    def _write(self, pin, output):
        mask = 1 << pin
        output = output << pin
        self.cache_output = self.cache_output | output
        self.transactor.write(
            GPIO["CHANNEL"], GPIO["W_DATAOUT"], mask=mask, data=self.cache_output, comment=f'Write {output >> pin} to pin {pin}')
        self.transactor.send()

    def _read(self):
        self.transactor.write(GPIO["CHANNEL"],
                              GPIO["R_DATAIN"], comment='Read gpio')
        self.transactor.send()


class Pin:
    def __init__(self, sca_gpio, pin_number):
        self.sca_gpio = sca_gpio
        self.pin_number = pin_number
        self._mode = 0
        self.output = None

    def mode(self, mode):
        if mode == "in":
            self._mode = 0
        elif mode == "out":
            self._mode = 1
        else:
            raise Exception('Pin mode must be either "in" or "out"')
        self.sca_gpio._set_mode(self.pin_number, self._mode)

    def write(self, output):
        if self._mode == 1:
            self.sca_gpio._write(self.pin_number, output)
            self.output = output
