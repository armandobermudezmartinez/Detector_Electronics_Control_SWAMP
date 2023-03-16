from utils import from_8bit_to_32bit
from gbtsca_constants import CTRL, I2C, GPIO


class GBT_SCA:
    def __init__(self, transactor):  # , transactor):
        self.transactor = transactor

    #
    # Controlling I2C masters
    #

    def enable_i2c(self, index=0, i2c_bus_frequency=100):
        if index not in range(16):
            raise Exception("I2C-channel index out of range")
        if i2c_bus_frequency not in [100, 200, 400, 1000]:
            raise Exception("Bus frequency not among permissible values")

        index_bit = (1 << index)
        channel = I2C["CHANNEL_MAP"][index]

        INPUTMASK_CRB = 0x001f
        INPUTMASK_CRC = 0x1fe0
        INPUTMASK_CRD = 0xe000

        if (index_bit & INPUTMASK_CRB):
            d3 = 0
            if ((1 << 0) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C0"]
            if ((1 << 1) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C1"]
            if ((1 << 2) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C2"]
            if ((1 << 3) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C3"]
            if ((1 << 4) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C4"]

            m3 = CTRL["MASK_CRB_I2C0"] | CTRL["MASK_CRB_I2C1"] | CTRL[
                "MASK_CRB_I2C2"] | CTRL["MASK_CRB_I2C3"] | CTRL["MASK_CRB_I2C4"]

            mask = from_8bit_to_32bit(m3)
            data = from_8bit_to_32bit(d3)
            self.transactor.write(CTRL["CHANNEL_CTRL"], CTRL["R_CRB"])
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRB"], mask, data)

        if (index_bit & INPUTMASK_CRC):
            d3 = 0
            if ((1 << 5) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C5"]
            if ((1 << 6) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C6"]
            if ((1 << 7) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C7"]
            if ((1 << 8) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C8"]
            if ((1 << 9) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C9"]
            if ((1 << 10) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C10"]
            if ((1 << 11) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C11"]
            if ((1 << 12) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C12"]

            m3 = CTRL["MASK_CRC_I2C5"] | CTRL["MASK_CRC_I2C6"] | CTRL["MASK_CRC_I2C7"] | CTRL[
                "MASK_CRC_I2C8"] | CTRL["MASK_CRC_I2C9"] | CTRL["MASK_CRC_I2C10"] | CTRL[
                "MASK_CRC_I2C11"] | CTRL["MASK_CRC_I2C12"]

            mask = from_8bit_to_32bit(m3)
            data = from_8bit_to_32bit(d3)
            self.transactor.write(CTRL["CHANNEL_CTRL"], CTRL["R_CRC"])
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRC"], mask, data)

        if (index_bit & INPUTMASK_CRD):
            d3 = 0
            if ((1 << 13) & index_bit):
                d3 = d3 | CTRL["MASK_CRD_I2C13"]
            if ((1 << 14) & index_bit):
                d3 = d3 | CTRL["MASK_CRD_I2C14"]
            if ((1 << 15) & index_bit):
                d3 = d3 | CTRL["MASK_CRD_I2C15"]

            m3 = CTRL["MASK_CRD_I2C13"] | CTRL[
                "MASK_CRD_I2C14"] | CTRL["MASK_CRD_I2C15"]

            mask = from_8bit_to_32bit(m3)
            data = from_8bit_to_32bit(d3)
            self.transactor.write(CTRL["CHANNEL_CTRL"], CTRL["R_CRD"])
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRD"], mask, data)

        self._set_i2c_bus_frequency(channel, i2c_bus_frequency)

    def _set_i2c_bus_frequency(self, channel, frequency):
        frequencies = {
            100: 0b00,
            200: 0b01,
            400: 0b10,
            1000: 0b11
        }

        m3, d3 = I2C["MASK_CTRL_REG_SPEED"], frequencies[frequency]
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        self.transactor.write(channel, I2C["R_CTRL_REG"])
        self.transactor.write(channel, I2C["W_CTRL_REG"], mask, data)

    #
    # Controlling GPIOs
    #

    def enable_gpio(self, enableGPIO=1):
        m3, d3 = CTRL["MASK_CRB_PARAL"], CTRL["MASK_CRB_PARAL"] if enableGPIO else 0
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        self.transactor.write(CTRL["CHANNEL_CTRL"], CTRL["R_CRB"])
        self.transactor.write(CTRL["CHANNEL_CTRL"], CTRL["W_CRB"], mask, data)

    def set_gpio_direction(self, directions=0):
        mask = 0xFFFFFFFF
        data = directions
        self.transactor.write(GPIO["CHANNEL"], GPIO["W_DATAOUT"], mask, data)

    def gpio_write(self, mask=0, data=0):
        self.transactor.write(GPIO["CHANNEL"], GPIO["R_DATAOUT"])
        self.transactor.write(GPIO["CHANNEL"], GPIO["W_DATAOUT"], mask, data)
