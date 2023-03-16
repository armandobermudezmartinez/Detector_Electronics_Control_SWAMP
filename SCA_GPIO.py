from Transactor import Transactor
from GBT_SCA import GBT_SCA


class SCA_GPIO:
    def __init__(self, gbt_sca=0, number_of_pins=0):
        if number_of_pins > 32:
            raise Exception("Number of pins exceeds GBT_SCA GPIO block")
        self.gbt_sca = gbt_sca
        self.number_of_pins = number_of_pins
        self._number_of_used_pins = 0
        self.directions = 0
        self.output = 0
        self.output_mask = 0

    def _set_mode(self, pin, mode):
        self.directions |= mode < pin
        if mode == 1:
            self.output_mask = 1 << pin

    def _enable(self):
        self.gbt_sca.enable_gpio()
        self.gbt_sca.set_gpio_direction(self.directions)

    def _write(self, output_mask, output):
        self.gbt_sca.gpio_write(output_mask, output)


class GPIO:
    def __init__(self, sca_gpio, pin, mode):
        sca_gpio._number_of_used_pins += 1
        if sca_gpio._number_of_used_pins > sca_gpio.number_of_pins:
            raise Exception("Number of pins exceeds number of available pins")
        self.sca_gpio = sca_gpio
        self.pin = pin
        self.mode = mode
        self.sca_gpio._set_mode(self.pin, self.mode)
        if self.sca_gpio._number_of_used_pins == self.sca_gpio.number_of_pins:
            self.sca_gpio._enable()
        self.value = 1 if mode == 1 else None

    def write(self, value):
        if self.mode == 1:
            self.sca_gpio._write(1 << self.pin, value << self.pin)
            self.value = value


# transactor = Transactor()
# sca = GBT_SCA(transactor=transactor)
# sca_gpio = SCA_GPIO(gbt_sca=sca, target_number_of_used_pins=2)
# reset_pin = GPIO(sca_gpio=sca_gpio, pin=0, mode=1)
# test_pin = GPIO(sca_gpio=sca_gpio, pin=5, mode=0)
# reset_pin.write(1)

# roc = ROCv3(transport=sca_i2c[0],
#             base_address=0,
#             name='roc',
#             reset_pin=gbt_sca.reset_pin,
#             path_to_file=virtual_roc.path_to_registers_map)


# test_pin = GPIO(sca_gpio=sca_gpio, pin=0, mode=0)
# reset_pin.write(1)
# sca_gpio.write()

# print(bin(sca_gpio.output))

# roc_reset_pin.


# gpio = SCA_GPIO()
# gpio.

# print(bin(gpio.pins))
